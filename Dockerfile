# syntax=docker/dockerfile:1

# Python 이미지를 사용합니다.
ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base

# Python 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 컨테이너 내에서 작업할 디렉토리를 설정합니다.
WORKDIR /usr/src/app

# 컨테이너 내에서 사용할 non-privileged 유저를 생성합니다.
# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user 참조
ARG UID=1000
RUN addgroup --gid "${UID}" appuser && \
    adduser --disabled-password --gecos "" --home "/nonexistent" --shell "/sbin/nologin" --no-create-home --uid "${UID}" --ingroup "appuser" appuser

# 시스템 의존성 패키지를 설치합니다.
RUN apt-get update \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Python 종속성을 복사하고 설치합니다.
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# 애플리케이션 코드를 컨테이너에 복사합니다.
COPY . .

# 'static/admin' 디렉토리를 생성하고 권한을 설정합니다.
#RUN python manage.py collectstatic --noinput
#RUN chown -R appuser:appuser /usr/src/app/static

# non-privileged 유저로 전환합니다.
USER appuser

# Gunicorn 서버가 실행될 포트를 노출합니다.
EXPOSE 8000

# Gunicorn을 사용하여 Django 애플리케이션을 실행합니다.
CMD gunicorn 'gTeamProject.wsgi:application' --bind=0.0.0.0:8000 --reload

