# 파이썬 버전
FROM python:3.10.12

# 프로젝트의 작업 폴더 지정
WORKDIR /usr/src/app

# Python은 가끔 소스 코드를 컴파일할 때 확장자가 .pyc인 파일을 생성한다.
# 도커를 이용할 때, .pyc 파일이 필요하지 않으므로 .pyc 파일을 생성하지 않도록 한다.
ENV PYTHONDONTWRITEBYTECODE 1

# Python 로그가 버퍼링 없이 출력
ENV PYTHONUNBUFFERED 1

# 로컬 컴퓨터의 현재 위치(Dockerfile이 있는 경로)의 모든 파일을 전부 WORKDIR로 복사
# 장고 프로젝트가 도커 이미지에 모두 담긴다.
COPY . /usr/src/app

RUN apt-get update && apt-get install -y default-libmysqlclient-dev

# requirements.txt에 나열된 라이브러리를 설치
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["gunicorn", "gTeamProject.wsgi:application", "--bind", "0.0.0.0:8000"]
