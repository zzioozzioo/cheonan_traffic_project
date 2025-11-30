# 폴더 구조
```
cheonan_traffic_project/
│
├─ data/                   # 원본/가공 데이터
│   ├─ raw/                # 서버에서 수집한 CSV 원본(traffic 데이터)
│   ├─ processed/          # 전처리 후 분석용 CSV
│   └─ merged/             # 통합된 전체 데이터
│
├─ notebooks/              # 실험/분석용 Jupyter Notebook
│   ├─ 01_EDA.ipynb
│   └─ 02_Clustering.ipynb
│
├─ src/                    # 실제 코드
│   ├─ data_collection/    # 데이터 수집 스크립트
│   │   └─ fetch_traffic.py
│   │   └─ fetch_weather.py
│   ├─ preprocessing/      # 전처리 스크립트
│   │   └─ merge_traffic_weather.py 
│   │   └─ preprocess_traffic.py 
│   └─ modeling/           # 모델링 코드
│
├─ requirements.txt        # 프로젝트 패키지/환경 관리
└─ README.md               # 프로젝트 개요, 실행법
```

### 실행 시
- python3 -m venv venv
- source venv/bin/activate(Mac/Linux)

### 기상 데이터 openAPI
- 인증키: 5c0964a3a13033d49d842bf1e8bfdb0875bcb82588cf3d9324d4d94c7adfad0b
- 엔드포인트: https://apis.data.go.kr/1360000/AsosHourlyInfoService


