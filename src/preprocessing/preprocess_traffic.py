import pandas as pd
import os

# -------------------------------
# 1. Load traffic.csv
# -------------------------------
input_path = "./data/processed/traffic.csv"
df = pd.read_csv(input_path)

# -------------------------------
# 2. Delete '합계' column
# -------------------------------
if "합계" in df.columns:
    df = df.drop(columns=["합계"])

# -------------------------------
# 3. Sum traffic per intersection (교차로명)
#    - groupby: 일자 + 교차로명
#    - sum: 시간 컬럼만 합산
# -------------------------------
time_cols = [col for col in df.columns if col.endswith("시")]

# -------------------------------
# 4. WIDE → LONG 변환
#    melt 사용
#    time 컬럼에서 '00시' → 0 정수로 변환
# -------------------------------
df_long = df.melt(
    id_vars=["일자", "교차로명", "접근로명"],
    value_vars=time_cols,
    var_name="time",
    value_name="traffic_volume"
)

df_long["time"] = df_long["time"].str.replace("시", "", regex=False).astype(int)

# -------------------------------
# 5. 교차로별 시간대 합산
#    (접근로명을 제거하고 같은 교차로명의 같은 시간대끼리 합침)
# -------------------------------
df_sum = df_long.groupby(["일자", "교차로명", "time"])["traffic_volume"].sum().reset_index()

# -------------------------------
# 6. Column rename for consistency
# -------------------------------
df_sum = df_sum.rename(columns={
    "일자": "date",
    "교차로명": "intersection"
})

# -------------------------------
# datetime 생성
# -------------------------------
df_sum["datetime"] = pd.to_datetime(df_sum["date"] + " " + df_sum["time"].astype(str).str.zfill(2) + ":00")
df_sum = df_sum.drop(columns=["date", "time"]) # date, time 컬럼 제거
df_sum["datetime"] = df_sum["datetime"].dt.strftime("%Y-%m-%d %H:%M") # datetime 형식 맞추기
df_sum = df_sum[["datetime", "intersection", "traffic_volume"]] # 컬럼 순서 정리


# -------------------------------
# 6. Output folder 생성 후 저장
# -------------------------------
output_dir = "./data/processed"
os.makedirs(output_dir, exist_ok=True)

output_path = f"{output_dir}/traffic_clean.csv"
df_sum.to_csv(output_path, index=False)

print("완료! 저장됨 →", output_path)
