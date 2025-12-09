import pandas as pd
import os
import holidays

# 1. 파일 경로 설정
traffic_file = os.path.join("data/processed", "traffic_clean.csv")
weather_file = os.path.join("data/processed", "weather_clean.csv")
output_file = os.path.join("data/merged", "traffic_weather_merged.csv")

# 2. 데이터 로드
traffic = pd.read_csv(traffic_file)
weather = pd.read_csv(weather_file)

#  3. 날짜 형식 통일 (merge 기준: YYYY-MM-DD HH:00)
traffic["datetime"] = pd.to_datetime(traffic["datetime"], errors='coerce')
weather["datetime"] = pd.to_datetime(weather["datetime"], errors='coerce')

# 4. is_offday 파생변수 생성(공휴일 및 주말 여부 판별)
kr_holidays = holidays.KR(years=[2024, 2025]) # 한국 공휴일

traffic['weekday'] = traffic['datetime'].dt.dayofweek # 주말 플래그 생성
traffic['is_offday'] = traffic['weekday'].apply(lambda x: 1 if x >= 5 else 0) # 5: 토요일, 6: 일요일

# 공휴일이면 is_offday = 1로 업데이트 (주말/공휴일 중복 가능)
traffic['date_only'] = traffic['datetime'].dt.normalize() # 날짜만 추출
traffic.loc[traffic['date_only'].isin(kr_holidays), 'is_offday'] = 1

# 임시 컬럼 제거
traffic = traffic.drop(columns=['weekday', 'date_only'])


# 5. 병합(기상 데이터는 모든 교차로에 동일 적용
#    → cross join 필요 없음
#    → datetime 기준으로 left merge만 하면 자동으로 전체 교차로에 전달됨)
merged = pd.merge(
    traffic,
    weather,
    on="datetime",
    how="left"   # traffic 기준 → 교통 데이터가 기준이므로 left
)

# 6. datetime 형식 다시 한 번 맞추기
merged["datetime"] = pd.to_datetime(merged["datetime"], errors="coerce")
merged["datetime"] = merged["datetime"].dt.strftime("%Y-%m-%d %H:%M").astype(str)

# 7. 저장
merged.to_csv(output_file, index=False)

print(f"✔ 병합 완료! → {output_file}")
