## 00. Skills

 - Python 3.12
 - Fast API 0.115.6

### Require Libraries
 - Starlette ( 비동기 ASGI 프레임워크 )
 - Pydantic ( 입출력 항목 정의 및 검증 )
 - SQLAlchemy, alembic ( ORM 라이브러리 )
 - Uvicorn ( ASGI(Asynchronous Server Gateway Interface) 웹 서버 구현체 )

### Other Libraries
 - Swagger ( API 스펙 문서 자동화 )
 - python-multipart
 - python-jose ( JSON Web Token (JWT) )


## 01. Run Locally

Clone the project

```bash
  git clone https://github.com/shin-ga-eun/fastapi-myapi.git
```

Go to the project directory

```bash
  cd fastapi-myapi
```

Install dependencies

가상환경 생성
```bash
  # 가상환경 만들기
  python -m venv myapi

  # 가상환경 진입하기
  myapi\Scripts\activate

  # 가상환경 벗어나기
  myapi\Scripts\deactivate
```

가상환경에 FastAPI 설치
```bash
  myapi\Scripts\activate

  # pip 최신 버전 설치
  python -m pip install --upgrade pip

  # FastAPI 설치
  pip install fastapi
```

라이브러리 설치
```bash
# Pydantic 추가 email 검증 관련
  pip install "pydantic[email]"
  pip install "passlib[bcrypt]"

# SQLAlchemy, alembic
  pip install sqlalchemy
  pip install alembic
  alembic init migrations

# Uvicorn
  pip install uvicorn

# 인증 인가
  pip install python-multipart
  pip install "python-jose[cryptography]"
```

Start the server

```bash
  uvicorn main:app --reload
```

## 02. API 명세 

```
  # swagger
  http://127.0.0.1:8000/docs
```

## 03. DB 변경사항 반영
```
  # 리비전 파일 생성
  alembic revision --autogenerate

  # 생성된 리비전 파일로 DB 변경 
  alembic upgrade head
```
## Related

점프 투 FastAPI WikiDocs ( https://wikidocs.net/175066 )

