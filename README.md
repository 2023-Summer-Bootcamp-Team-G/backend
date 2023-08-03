# It's ME?!
# Instruction
질문에 대한 친구들의 답변들의 키워드를 추출하여 본인을 형상화한 캐릭터를 만들어주는 서비스
</br>
[It'me?! medium](https://medium.com/@hgh1057/its-me-46d9de903a94)
# DEMO
이미지, 영상 등

# System Architecture
![teamg drawio (6)](https://github.com/2023-Summer-Bootcamp-Team-G/backend/assets/91904079/033c5dcd-f538-43c8-a1a5-5486108aa0c4)

# Tech Stack


| Frontend | Backend | DevOps | DB | Others |
| :---: | :---: | :---: | :---: | :---: |
|![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=TypeScript&logoColor=white)<br> ![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=React&logoColor=white)<br> ![Vite](https://img.shields.io/badge/vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)<br> ![Styled-Components](https://img.shields.io/badge/Styled_Components-DB7093?style=for-the-badge&logo=Styledcomponents&logoColor=white)<br>![Axios](https://img.shields.io/badge/Axios-5A29E4?style=for-the-badge&logo=Axios&logoColor=white)<br>![zustand](https://img.shields.io/badge/zustand-ECD53F?style=for-the-badge&logo=zustand&logoColor=white)|![python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)<br> ![django](https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white)<br> ![RabbitMQ](https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge&logo=RabbitMQ&logoColor=white)<br> ![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=Celery&logoColor=white)<br> ![gunicorn](https://img.shields.io/badge/gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)<br>|![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white)<br> ![NGINX](https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=NGINX&logoColor=white)<br> ![AMAZON_EC2](https://img.shields.io/badge/AMAZON_EC2-FF9900?style=for-the-badge&logo=AMAZONEC2&logoColor=white)<br>![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white)<br> ![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=Grafana&logoColor=white)<br>![ELK stack](https://img.shields.io/badge/ELK_stack-005571?style=for-the-badge&logo=Elastic&logoColor=white)|![MySql](https://img.shields.io/badge/MySql-4479A1?style=for-the-badge&logo=MySql&logoColor=white)<br> ![AMAZON_RDS](https://img.shields.io/badge/AMAZON_RDS-527FFF?style=for-the-badge&logo=AMAZONRDS&logoColor=white)<br> ![AMAZON_S3](https://img.shields.io/badge/AMAZON_S3-569A31?style=for-the-badge&logo=AMAZONS3&logoColor=white)<br> ![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=Redis&logoColor=white)<br>|![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=Swagger&logoColor=white)<br>![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=Notion&logoColor=white)<br>![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=Slack&logoColor=white)<br>![POSTMAN](https://img.shields.io/badge/POSTMAN-FF6C37?style=for-the-badge&logo=POSTMAN&logoColor=white)<br>

# Intallation
```
docker-compose up
```
# Database
<details><summary>ERD
</summary>
<img src=https://github.com/2023-Summer-Bootcamp-Team-G/backend/assets/91904079/5fb8a02a-b305-47d3-80d6-28285ce1fc14
/>
</details>

# API
<details><summary>swagger
</summary>
<img src=
/>
</details>

## Detailed Info
**NAME** | **Description**
:---:|:---:
Nginx | 웹서버, 프록시 서버, https 연결 등을 담당합니다. | 
React | 질문 생성 및 답변, 캐릭터를 생성하여 보여주는 역할을 담당합니다. | 
Django | It's me의 서버로서 각종 요청을 처리하며 DB와 직접 소통합니다. | 
Gunicorn</br>Uvicorn | Gunicorn으로 Uvicorn 프로세스를 관리하며 요청을 비동기로 처리합니다. |
Mysql(RDS) | Database | 
RabbitMQ | 메세지 브로커로서 이미지 생성 처리 시간이 길기 때문에 사용합니다. | 
Celery | 이미지 생성과 같은 작업을 비동기 수행하기 위해 사용합니다. | 
Grafana | Prometheus로부터 받은 메트릭 데이터 등을 시각화하여 대시보드를 구성합니다. | 
Prometheus | Django의 메트릭 데이터를 수집하여 모니터링 합니다. | 
Filebeat | Nginx의 로그파일을 Filebeat로 수집합니다. | 
Logstash | Filebeat로 수집한 로그를 Logstash에 전달합니다. |
Elasticsearch | Logstash로부터 전달 받은 로그를 Elasticsearch에 저장합니다. | 
Kibana | Elasticsearch에 저장된 로그를 Kibana를 통해 분석 및 시각화합니다. | 

# Team Member


| Name | 최세엽 | 황장현 | 정우희 | 김동헌 | 김주언 | 이지은 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Profile | ![최세엽](https://github.com/2023-Summer-Bootcamp-Team-G/backend/assets/91904079/fb0f1ab1-894f-40f1-a817-46372ceb3eca) | ![황장현](https://github.com/2023-Summer-Bootcamp-Team-G/backend/assets/91904079/ecaf518a-f985-4dfe-ae4d-0094676b153e) | ![정우희](https://github.com/2023-Summer-Bootcamp-Team-G/backend/assets/91904079/f6d9eaa8-c653-4a03-bf96-66de26aa151d) | ![김동헌](https://github.com/2023-Summer-Bootcamp-Team-G/backend/assets/91904079/c72b9d8e-a3b9-4b3a-a120-48972f7f2990) | ![김주언](https://github.com/2023-Summer-Bootcamp-Team-G/backend/assets/91904079/43fe5160-ca0f-434c-af9e-e830896c65f0) | ![이지은](https://github.com/2023-Summer-Bootcamp-Team-G/backend/assets/91904079/188bfab0-acb6-4b18-ba37-b5548d197a58) |
| Role | Team Leader</br>Backend</br>DevOps| Frontend | Frontend | Backend | Backend | Frontend |
| GitHub | [non-cpu](https://github.com/non-cpu) | [JH722](https://github.com/JH722) | [woohee-jeong](https://github.com/woohee-jeong) | [heondong9265](https://github.com/heondong9265) | [wndjs803](https://github.com/wndjs803) | [egg-silver](https://github.com/egg-silver) |
