#!/bin/bash

# 감지할 디렉토리 경로
WATCH_DIR="/usr/share/nginx/html"

# 파일 변경 사항이 감지되면 Nginx 재시작
monitor_changes() {
    while true; do
        inotifywait -r -e modify,create,delete,move $WATCH_DIR
        echo "Nginx 재시작 시도: $(date)"
        nginx -s reload
    done
}

# Nginx 주기적 재시작 함수
restart_nginx_periodically() {
    while true; do
        sleep $((6 * 60 * 60))
        echo "주기적으로 Nginx를 재시작합니다: $(date)"
        nginx -s reload
    done
}

# 파일 변경 감지 스크립트를 백그라운드에서 실행
monitor_changes &

# Nginx 주기적 재시작 함수를 백그라운드에서 실행
restart_nginx_periodically &

# Nginx 데몬 실행
nginx -g "daemon off;"
