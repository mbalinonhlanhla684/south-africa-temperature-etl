import boto3
import os
from dotenv import load_dotenv

load_dotenv()

# Get credentials from .env
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

# Create S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

def upload_file(local_path, s3_key):
    print(f"Uploading {local_path} to s3://{BUCKET_NAME}/{s3_key} ...")
    s3.upload_file(local_path, BUCKET_NAME, s3_key)
    print("✅ Upload complete!")

if __name__ == "__main__":
    upload_file("temperature_changes.csv", "clean/temperature_changes.csv")