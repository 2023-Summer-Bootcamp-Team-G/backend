# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base

# Python은 가끔 소스 코드를 컴파일할 때 확장자가 .pyc인 파일을 생성한다.
# 도커를 이용할 때, .pyc 파일이 필요하지 않으므로 .pyc 파일을 생성하지 않도록 한다.
ENV PYTHONDONTWRITEBYTECODE 1

# Python 로그가 버퍼링 없이 출력
ENV PYTHONUNBUFFERED 1

ARG REGION_NAME=ap-northeast-2
ENV REGION_NAME=${REGION_NAME}

# 프로젝트의 작업 폴더 지정
WORKDIR /usr/src/app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN apt-get update \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# 복사하여 requirements.txt를 컨테이너에 복사
COPY requirements.txt .

# requirements.txt로부터 종속성 설치
RUN python -m pip install -r requirements.txt

# 'data/static' 디렉토리 생성 및 권한 설정
RUN mkdir -p /usr/src/app/data/static
RUN chown -R appuser:appuser /usr/src/app/data

# 현재 디렉토리의 모든 파일 복사
COPY . .

USER appuser

EXPOSE 8000

CMD python manage.py collectstatic --noinput \
    && gunicorn 'gTeamProject.wsgi:application' --bind=0.0.0.0:8000 --reload

