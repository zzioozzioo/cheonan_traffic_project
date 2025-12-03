import os
import glob
import pandas as pd

# ── 데이터 폴더 & 출력 파일 경로 ──
RAW_DATA_DIR = "/Users/zzioo/School/4-2/창의적문제해결/텀 프로젝트/cheonan_traffic_project/data/raw"
OUTPUT_FILE = "/Users/zzioo/School/4-2/창의적문제해결/텀 프로젝트/cheonan_traffic_project/data/processed/traffic.csv"

# ── 파일 목록 가져오기 ──
all_files = glob.glob(os.path.join(RAW_DATA_DIR, "*.xlsx"))

if not all_files:
    print("[X] XLSX 파일이 없습니다!")
    exit()

# ── 파일 이름 숫자 기준으로 정렬 ──
def extract_number(file_path):
    """파일 이름에서 숫자만 추출 (예: '1.xlsx' -> 1)"""
    base_name = os.path.basename(file_path)
    number_part = os.path.splitext(base_name)[0]  # '1.xlsx' -> '1'
    return int(number_part)

all_files.sort(key=extract_number)

# ── XLSX 합치기 ──
df_list = [pd.read_excel(f) for f in all_files]
merged_df = pd.concat(df_list, ignore_index=True)

# ── 필요시 날짜 컬럼 기준으로 정렬 (예: '날짜' 컬럼)
# merged_df = merged_df.sort_values(by="날짜").reset_index(drop=True)

# ── CSV로 저장 ──
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
merged_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print(f"[✓] 날짜 순으로 통합 CSV 생성 완료: {OUTPUT_FILE}")
