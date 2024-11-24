# good_news

## 가상환경
### 가상 환경 생성 (Windows)
python -m venv venv

### 가상 환경 생성 (Mac/Linux)
python3 -m venv venv

### 가상 환경 활성화 (Windows)
source venv/Scripts/activate

### 가상 환경 활성화 (Mac/Linux)
source venv/bin/activate

### requirements.txt 작성법
pip freeze > requirements.txt

### 패키지 목록이 존재할 때 그것들을 설치하는 방법
pip install -r requirements.txt

sudo service postgresql start   # 서버 시작
sudo service postgresql stop    # 서버 종료
sudo service postgresql restart # 서버 재시작