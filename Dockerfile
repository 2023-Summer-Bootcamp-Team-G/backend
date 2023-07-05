FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

## -----------------------------------------------------
##EC2에서 돌릴 경우
#
#RUN apt-get -y update
#RUN apt-get -y install vim
#
## 작업 디렉토리 생성
#RUN mkdir /srv/docker-server
#ADD . /src/docker-server
#
#WORKDIR /srv/docker-server
#
### 의존성 패키지 설치
##RUN apt install --upgrade pip
##RUN apt install -r requirements.txt
#
## -----------------------------------------------------

##local에서 돌릴 경우
#ADD . D:/Teacheer/Docker
## 작업 디렉토리 설정
#WORKDIR D:/Teacheer/Docker
#
## 의존성 패키지 설치
#COPY requirements.txt ./Docker/requirements.txt
#COPY manage.py ./Docker/manage.py
#
##RUN pip install --upgrade pip # pip 업글
##RUN pip install -r requirements.txt # 필수 패키지 설치
#
## 소스 코드 복사
#COPY . ./Docker

WORKDIR /mainapp

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

## -----------------------------------------------------
# 포트 노출 및 Django 실행 명령
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]