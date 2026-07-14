# 🚀 교차로별 교통 혼잡도 예측 프로젝트
> 교차로 교통량 데이터를 기반으로 클러스터링과 시계열 예측(XGBoost)을 수행하고, 신호 조정 정책 효과를 시뮬레이션한 데이터 분석 프로젝트

---

## 📌 1. 프로젝트 개요
* **개발 기간:** 2025.11.08 ~ 2025.12.01 (3주)
* **참여 인원:** 개인 프로젝트
* **주요 역할:** 데이터 수집 및 전처리, EDA, 클러스터링(K-Means), 데이터 모델링 및 학습(XGBoost)

#### 💡 프로젝트 목표
천안시 교차로별 교통·기상 데이터를 기반으로 K-means 클러스터링을 통해 교차로 유형을 분류하고 맞춤형 교통량 예측 모델을 구축한다.
나아가 상시혼잡형 교차로에 신호 주기 조정 시나리오를 적용하는 정책 실험을 수행하여 실증적인 교통 혼잡 완화 효과를 분석하는 것을 목표로 한다.

---

## 2. 실행 시
- python3 -m venv venv
- source venv/bin/activate(Mac/Linux)

---

## 🛠 3. 사용 기술 및 개발 환경


<div><h3>📚 STACKS</h1></div>

<div> 

### 📊 Data / AI
  <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> 
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=Pandas&logoColor=white">
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=NumPy&logoColor=white">
  <img src="https://img.shields.io/badge/scikitlearn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white">

### 🛠️ Tools
  <img src="https://img.shields.io/badge/VS%20Code-007ACC?style=for-the-badge&logo=visual-studio-code&logoColor=white"> 
  <img src="https://img.shields.io/badge/Jupyter Notebook-F37626?style=for-the-badge&logo=Jupyter&logoColor=white">
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white">
  <br>
</div>

---

## 🎯 4. 핵심 파이프라인

* **데이터 수집 및 전처리**
  - 천안시 교통량 데이터와 기상 데이터를 수집 및 병합해 통합 데이터셋 생성
  - 불필요한 데이터 제거 및 이상치 처리
* **EDA(탐색적 데이터 분석)**
  - 날짜별, 시간대별, 요일별, 교차로별, 강수 여부에 따른 평균 교통량 분석
  - 변수간 선형 관계 분석
  - 월별 교통량 분포를 통한 계절적 변동성 분석
  - 시간대별(출근, 점심, 퇴근, 기타) 평균 교통량 분석
  - 교차로별 24시간 평균 교통량 패턴 시각화 -> 군집화의 근거 자료
* **클러스터링**
  - 교차로별 혼잡 패턴을 유형화하기 위함 
  - Elbow Method와 Silhouette Score를 고려한 K값(=2) 선정 
  - K-means 클러스터링 수행 -> (중·저혼잡형 / 상시 혼잡형)으로 분류
* **데이터 모델링 및 학습**
  - RMSE, MAE 기준 회귀 모델의 성능 비교(Linear Regression, Random Forest, XGBoost) 및 예측 모델 선정 -> XGBoost
  - 학습 성능 약 0.9 달성(R^2 기준)

---

## ⚡ 5. 기술적 성장 및 트러블 슈팅

### 🔍 Issue 1: 단일 통계량 기반 분류 한계 극복을 위한 K-means 교통 패턴 군집화
* **문제 상황:** 
  - 교차로마다 시간대별 교통 패턴이 크게 달라 단순 평균값만으로 혼잡 유형을 구분하기 어려움
  - 특정 시간대만 혼잡한 교차로와 하루 종일 혼잡한 교차로가 동일하게 해석되는 문제 존재
* **해결 방안:** 
  - 교차로 단위로 7개의 핵심 특징 변수 생성
  - 수치형 변수를 StandardScaler로 정규화하여 스케일 영향 제거
  - Elbow Plot과 Silhouette Score를 기반으로 최적 K를 탐색
  - 실험 결과 K=2가 해석 가능성이 가장 높아 상시혼잡형 / 중저혼잡형으로 분류
* **결과:** 
  - 상시혼잡형 교차로 31개 자동 식별
  - 교차로별 24시간 패턴 시각화를 통한 군집 특성 구분
  - 예측 모델링과 정책 시뮬레이션의 입력 데이터로 활용 가능한 구조 확보

### 🔍 Issue 2: 선형 모델의 비선형성 학습 한계 개선을 위한 XGBoost 도입
* **문제 상황:** 
  - 단순 선형 회귀 모델은 교통량의 비선형적인 시간 패턴을 반영하지 못함
  - 출퇴근 시간의 급격한 교통량 증가 패턴과 반복 주기를 충분히 학습하지 못함
  - 교차로별 특성과 시간 특성이 동시에 반영되지 않음
* **해결 방안:** 
  - XGBoost 기반 트리 모델을 적용해 비선형 관계를 학습하도록 개선
  - 기상 변수, 시간 변수, 클러스터 변수, 시계열 파생변수를 함께 입력
* **결과:** 
  - RandomForest RMSE: 96.3
  - XGBoost RMSE: 71.0
  - 약 26% 수준의 오차 감소로, 기존 모델 대비 실제 교통량 패턴 예측 성능 개선

### 🔍 Issue 3: 시계열 주기성 및 단기 흐름 반영을 위한 Lag/이동평균 변수 확장
* **문제 상황:** 
  - 현재 시점 기반 데이터만으로는 반복적인 시간 패턴 반영이 어려움
  - 하루 전 동일 시간대 교통량 미반영
* **해결 방안:** 
  - Lag 변수 추가(1시간 전, 24시간 전, 48시간 전, 72시간 전)
  - 이동평균 변수 추가(3시간, 6시간, 24시간, 48시간)
  - 시간 주기성을 반영하기 위해 sin/cos 인코딩 적용
* **결과:** 
  - 시간 반복성과 단기 흐름 동시 반영
  - 출퇴근 피크 예측 성능 향상
  - 클러스터별 모델링에서 안정적인 R² 확보 가능

---

## 6. 폴더 구조
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


