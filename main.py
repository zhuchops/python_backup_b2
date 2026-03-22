from datetime import datetime, timezone
import os
from pathlib import Path
import boto3
from botocore.client import Config
from dotenv import load_dotenv

from config.config import MyConfig


load_dotenv()

CONFIG_PATH = Path("./config.yml")

def main():
    access_key_id = os.getenv("ACCESS_KEY_ID")
    secret_access_key = os.getenv("SECRET_ACCESS_KEY")

    s3 = boto3.client(
        "s3",
        endpoint_url="https://s3.eu-central-003.backblazeb2.com",
        aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key,
        config=Config(signature_version="s3v4")
    )

    config_data = MyConfig(path=CONFIG_PATH)
    today = datetime.now(timezone.utc).today()


if __name__ == "__main__":
    main()
