# 폴더 구조
```
cheonan_traffic_project/
│
├─ data/                   # 원본/가공 데이터
│   ├─ raw/                # 서버에서 수집한 CSV 원본(traffic 데이터만 존재)
│   ├─ processed/          # 전처리한 데이터
│   └─ merged/             # 통합된 데이터
│       ├─ traffic_weather_merged.csv           # 통합된 교통량&기상 데이터
│       └─ traffic_weather_with_cluster.csv     # 최종 데이터셋(클러스터 데이터 포함)
│
├─ notebooks/              # 실험/분석용 Jupyter Notebook
│   ├─ 01_EDA.ipynb     
│   ├─ 02_Clustering.ipynb
│   ├─ 03_Modeling.ipynb
│   └─ 04_PolicySimulation.ipynb

├─ src/                    # 실제 코드
│   ├─ data_collection/    # 데이터 수집 스크립트
│   │   └─ fetch_traffic.py
│   │   └─ fetch_weather.py
│   └─ preprocessing/      # 전처리 스크립트
│   │   ├─ preprocess_traffic.py            # 교통량 데이터 전처리
│   │   ├─ preprocess_weather.py            # 기상 데이터 전처리
│   │   └─ merge_traffic_weather.py         # 교통량&기상 데이터 통합
│
└─ README.md               # 프로젝트 개요, 실행법
```

### 실행 시
- python3 -m venv venv
- source venv/bin/activate(Mac/Linux)

### 기상 데이터 openAPI
- 인증키: 5c0964a3a13033d49d842bf1e8bfdb0875bcb82588cf3d9324d4d94c7adfad0b
- 엔드포인트: https://apis.data.go.kr/1360000/AsosHourlyInfoService


