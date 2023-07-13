# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.9.9
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

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

# WORKDIR /mainapp
WORKDIR /app

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

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

COPY . .

RUN mkdir static
RUN python manage.py collectstatic

USER appuser

# COPY . .

EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD gunicorn 'gTeamProject.wsgi' --bind=0.0.0.0:8000
