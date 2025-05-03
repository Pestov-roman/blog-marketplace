from uuid import uuid4

import boto3
from botocore.client import Config
from types_boto3_s3.client import S3Client

from src.settings import settings

_SESSION: boto3.Session | None = None


def _get_client(endpoint_url: str | None = None) -> S3Client:
    global _SESSION
    if _SESSION is None:
        _SESSION = boto3.Session()
    return _SESSION.client(
        service_name="s3",
        endpoint_url=endpoint_url or settings.s3_endpoint,
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        config=Config(signature_version="s3v4"),
    )


def upload_file(data: bytes, content_type: str) -> str:
    client = _get_client()
    key = f"{uuid4()}.bin"
    client.put_object(
        Bucket=settings.s3_bucket,
        Key=key,
        Body=data,
        ContentType=content_type,
        ACL="public-read",
    )
    return f"{settings.s3_endpoint}/{settings.s3_bucket}/{key}"


def ensure_bucket() -> None:
    client = _get_client()
    buckets = {b["Name"] for b in client.list_buckets()["Buckets"]}
    if settings.s3_bucket not in buckets:
        client.create_bucket(Bucket=settings.s3_bucket)
