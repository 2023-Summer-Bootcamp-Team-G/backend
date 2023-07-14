import os
import json
import boto3

from dotenv import load_dotenv

load_dotenv()


class AWSManager:
    _session = None

    @classmethod
    def get_session(cls):
        if not cls._session:
            env = os.environ.get("SERVER_NAME")

            if env == "EC2":
                cls._session = boto3.Session()
            else:
                cls._session = boto3.Session(
                    region_name=os.getenv("REGION_NAME"),
                    aws_access_key_id=os.getenv("AWS_SECRET_ACCESS_KEY"),
                    aws_secret_access_key=os.getenv("AWS_SECRET_SECRET_KEY"),
                )

        return cls._session

    @classmethod
    def get_secret(cls, secret_name):
        session = cls.get_session()
        client = session.client(service_name="secretsmanager")

        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        return json.loads(get_secret_value_response["SecretString"])
