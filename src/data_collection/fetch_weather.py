import requests
import pandas as pd
from datetime import datetime, timedelta
from urllib.parse import quote
import holidays

# ==============================
# 설정
# ==============================
SERVICE_KEY = "5c0964a3a13033d49d842bf1e8bfdb0875bcb82588cf3d9324d4d94c7adfad0b"
ENCODED_KEY = quote(SERVICE_KEY, safe='')  # URL 인코딩
STATION_ID = "232"  # 천안 ASOS 관측소 ID
START_DATE = "20241102"
END_DATE   = "20251101"

# 한국 공휴일
kr_holidays = holidays.KR(years=[2024, 2025])

# ==============================
# 날짜 반복 함수 (1일 단위)
# ==============================
def daterange_days(start_date, end_date):
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=1)

# ==============================
# ASOS 1시간 단위 데이터 요청 함수
# ==============================
def fetch_asos_hourly_for_day(date):
    url = "https://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList"
    
    params = {
        "serviceKey": ENCODED_KEY,
        "pageNo": "1",
        "numOfRows": "24",       # 하루 24시간
        "dataType": "JSON",
        "dataCd": "ASOS",
        "dateCd": "HR",
        "startDt": date.strftime("%Y%m%d"),
        "startHh": "00",
        "endDt": date.strftime("%Y%m%d"),
        "endHh": "23",
        "stnIds": STATION_ID,
    }

    print(f"➡ 요청: {params['startDt']}")
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(" ❌ HTTP 오류:", response.status_code)
        return None

    data = response.json()
    items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])

    if not items:
        print(" ❌ 데이터 없음")
        return None

    df = pd.DataFrame(items)

    # 필요한 컬럼만 선택
    columns_to_keep = ["tm", "ta", "rn", "ws"] # tm: 시간, ta: 기온, rn: 강수량, ws: 풍속
    df = df[columns_to_keep]
    

    # 주말/공휴일 여부 파생변수 생성
    tm_dt = pd.to_datetime(df['tm'])
    is_weekend = tm_dt.dt.weekday >= 5
    is_holiday = tm_dt.dt.date.isin(kr_holidays)
    df['is_offday'] = (is_weekend | is_holiday).astype(int)  # 1: 주말/공휴일, 0: 평일

    
    return df

# ==============================
# 메인: 반복 요청 & CSV 저장
# ==============================
all_df = []
start = datetime.strptime(START_DATE, "%Y%m%d")
end   = datetime.strptime(END_DATE, "%Y%m%d")

print("⏳ 기상 데이터 다운로드 시작...\n")

for day in daterange_days(start, end):
    df = fetch_asos_hourly_for_day(day)
    if df is not None:
        all_df.append(df)

print("\n📌 모든 요청 완료. 데이터 병합 중...")

if all_df:
    final_df = pd.concat(all_df, ignore_index=True)

    final_df = final_df.rename(columns={ # 컬럼명 변경
        "tm": "time",
        "ta": "temp",
        "rn": "precipitation",
        "ws": "wind"
    })

    save_path = "/Users/zzioo/School/4-2/창의적문제해결/텀 프로젝트/cheonan_traffic_project/data/processed/weather.csv"
    final_df.to_csv(save_path, index=False, encoding="utf-8-sig")
    print(f"✅ 저장 완료: {save_path} (총 {len(final_df)}행)")
else:
    print("❌ 단 한 건의 데이터도 수집되지 않았습니다.")
