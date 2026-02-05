# 💰 Flask 가계부 웹 애플리케이션

Flask + SQLite 기반의 간단한 가계부 웹 애플리케이션입니다.  
수입/지출을 기록하고, 사용처별 비율을 원그래프로 시각화할 수 있습니다.

---

## 📌 주요 기능

- 수입 / 지출 기록
- 사용처(카테고리) 선택 + 상세내역 입력
- 내역에서 상세내역 바로 수정
- 수입/지출 + 세부 사용처 비율 원그래프
- 기간별 조회
- 금액 3자리 콤마 표시

---

## 🛠️ 기술 스택

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite3
- **Chart**: Chart.js

---

## 📂 프로젝트 구조
Account_Book_Proj/
│
├─ app.py
├─ account.db # (자동 생성됨)
├─ requirements.txt
├─ README.md
│
├─ templates/
│ └─ index.html
│
└─ static/
└─ style.css


> ⚠️ `account.db`는 GitHub에 포함하지 않습니다.  
> 실행 시 자동으로 생성됩니다.

---

## ▶️ 실행 방법

```bash
git clone <레포주소>
cd Account_Book_Proj

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
python app.py

### 1️⃣ 저장소 클론
```bash
git clone <레포지토리 주소>
cd Account_Book_Proj