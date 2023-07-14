# 파이썬 버전
FROM python:3.10.12

# 프로젝트의 작업 폴더 지정
WORKDIR /usr/src/app

# Python은 가끔 소스 코드를 컴파일할 때 확장자가 .pyc인 파일을 생성한다.
# 도커를 이용할 때, .pyc 파일이 필요하지 않으므로 .pyc 파일을 생성하지 않도록 한다.
ENV PYTHONDONTWRITEBYTECODE 1

# Python 로그가 버퍼링 없이 출력
ENV PYTHONUNBUFFERED 1

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

COPY . /usr/src/app

RUN mkdir static
RUN python manage.py collectstatic

USER appuser

# COPY . .

EXPOSE 8000

# Docker 컨테이너를 시작할 때 Gunicorn 웹 서버를 실행하고 Django 애플리케이션을 서비스하기 위해 사용
# --bind "0.0.0.0:8000"은 Gunicorn이 0.0.0.0 IP 주소와 8000 포트에 바인딩되도록 지정
# 이는 외부로부터의 모든 IP로부터의 요청을 허용하여 외부에서 애플리케이션에 접근할 수 있도록 gksek.
CMD ["gunicorn", "gTeamProject.wsgi:application", "--bind", "0.0.0.0:8000"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD gunicorn 'gTeamProject.wsgi' --bind=0.0.0.0:8000
