import docker
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()


def send_slack_notification(webhook_url, message):
    payload = {'text': message}
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            print("Slack notification sent successfully.")
        else:
            print(f"Failed to send Slack notification. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending Slack notification: {e}")


def create_docker_client():
    # Docker 호스트의 IP 주소와 포트를 환경 변수로 설정 (기본값은 unix://var/run/docker.sock)
    docker_host = os.environ.get('DOCKER_HOST', 'unix://var/run/docker.sock')

    # Docker 클라이언트 생성
    client = docker.DockerClient(base_url=docker_host)
    return client


def main():
    # Slack Webhook URL
    webhook_url = 'https://hooks.slack.com/services/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'

    # Docker 클라이언트 생성
    try:
        client = create_docker_client()
    except docker.errors.DockerException as e:
        print(f"Error creating Docker client: {e}")
        return

    event_generator = client.events(decode=True)

    try:
        for event in event_generator:
            if event['Action'] == 'die':
                container_id = event['Actor']['ID']
                container_name = event['Actor']['Attributes']['name']
                status_code = event['Actor']['Attributes']['exitCode']

                message = f"Container '{container_name}' (ID: {container_id}) has exited with status code {status_code}."
                send_slack_notification(webhook_url, message)
    except KeyboardInterrupt:
        print("Event listener stopped.")


if __name__ == '__main__':
    while True:
        main()
        time.sleep(1)
