import pandas as pd
import os

# ----------------------------
# 1. 파일 경로 설정
# ----------------------------
traffic_file = os.path.join("data/processed", "traffic_clean.csv")
weather_file = os.path.join("data/processed", "weather.csv")
output_file = os.path.join("data/merged", "traffic_weather_merged.csv")

# ----------------------------
# 2. 데이터 로드
# ----------------------------
traffic = pd.read_csv(traffic_file)
weather = pd.read_csv(weather_file)

# ----------------------------
#  3. 컬럼명 변경 및 날짜 형식 통일 (merge 기준: YYYY-MM-DD HH:00)
# ----------------------------
traffic = traffic.rename(columns={"traffic": "traffic_volume"})
weather = weather.rename(columns={
    "time": "datetime",
    "ta": "temp",
    "rn": "precipitation",
    "ws": "wind"
})

traffic["datetime"] = pd.to_datetime(traffic["datetime"], errors='coerce')
weather["datetime"] = pd.to_datetime(weather["datetime"], errors='coerce')


# ----------------------------
# 4. 기상 결측치 처리
#    - 강수량(rn)이 빈칸 → 0
#    - 그 외(NaN)는 그대로 두되, 필요 시 이후 단계에서 처리
# ----------------------------
if "precipitation" in weather.columns:
    weather["precipitation"] = weather["precipitation"].fillna(0)

# ----------------------------
# 5. 병합(기상 데이터는 모든 교차로에 동일 적용
#    → cross join 필요 없음
#    → datetime 기준으로 left merge만 하면 자동으로 전체 교차로에 전달됨)
# ----------------------------
merged = pd.merge(
    traffic,
    weather,
    on="datetime",
    how="left"   # traffic 기준 → 교통 데이터가 기준이므로 left
)

# ----------------------------
# 6. 이상치 처리 (Rule-based)
# ----------------------------

# 6-1. 교통량 음수 → 0으로 수정
merged.loc[merged["traffic_volume"] < 0, "traffic_volume"] = 0

# 6-2. 매우 큰 값 제거/수정 (1시간 교통량이 10만 이상이면 오류로 간주)
merged.loc[merged["traffic_volume"] > 100000, "traffic_volume"] = 100000

# 6-3. 물리적으로 불가능한 온도값 제거 처리
if "temp" in merged.columns:
    merged.loc[merged["temp"] < -40, "temp"] = None
    merged.loc[merged["temp"] > 50, "temp"] = None

# datetime 형식 맞추기
merged["datetime"] = pd.to_datetime(merged["datetime"], errors="coerce")
merged["datetime"] = merged["datetime"].dt.strftime("%Y-%m-%d %H:%M").astype(str)

# ----------------------------
# 7. 저장
# ----------------------------
merged.to_csv(output_file, index=False)

print(f"✔ 병합 완료! → {output_file}")
