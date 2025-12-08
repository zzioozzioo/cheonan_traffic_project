import pandas as pd
import os

# -------------------------------
# 1. Load weather.csv
# -------------------------------
input_path = "./data/processed/weather.csv"
df = pd.read_csv(input_path)

# -------------------------------
# 2. 컬럼명 수정
# -------------------------------
df = df.rename(columns={
    "time": "datetime",
    "ta": "temp",
    "rn": "precipitation",
    "ws": "wind"
})

# -------------------------------
# 3. Data type / Format adjustment
# -------------------------------
df["datetime"] = pd.to_datetime(df["datetime"], errors='coerce')
df["datetime"] = df["datetime"].dt.strftime("%Y-%m-%d %H:%M")


# -------------------------------
# 4. 결측치 및 이상치 처리 (Rule-based)
# -------------------------------
# 4-1. 강수량(precipitation) 결측치 → 0으로 처리
if "precipitation" in df.columns:
    df["precipitation"] = df["precipitation"].fillna(0)

# 4-2. 물리적으로 불가능한 온도값(이상치) 제거 처리
if "temp" in df.columns:
    # -40도 미만 또는 50도 초과는 NaN으로 처리
    df.loc[df["temp"] < -40, "temp"] = None
    df.loc[df["temp"] > 50, "temp"] = None


# -------------------------------
# 5. Output folder 생성 후 저장
# -------------------------------
output_dir = "./data/processed"
os.makedirs(output_dir, exist_ok=True)

output_path = f"{output_dir}/weather_clean.csv"
df.to_csv(output_path, index=False)

print("✔ weather_clean.csv 생성 완료!")