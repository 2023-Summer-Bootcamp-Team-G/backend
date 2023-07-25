FROM nginx:latest

# certbot을 설치합니다.
RUN apt-get update && apt-get install -y certbot

# 기존 코드에서 nginx 설정 파일을 올바른 경로로 복사하는 명령어를 수정합니다.
COPY nginx.conf /etc/nginx/conf.d/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-available/

# sites-enabled 디렉토리를 생성하고 심볼릭 링크를 추가합니다.
RUN mkdir -p /etc/nginx/sites-enabled/ \
    && ln -s /etc/nginx/sites-available/nginx-app.conf /etc/nginx/sites-enabled/

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
