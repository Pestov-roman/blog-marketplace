import boto3

from src.settings import settings


def _get_client():
    return boto3.client(
        service_name="s3",
        endpoint_url=settings.s3_endpoint,
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        region_name="us-east-1",
    )


def ensure_bucket():
    client = _get_client()
    response = client.list_buckets()
    buckets = {b["Name"] for b in response.get("Buckets", [])}
    if settings.s3_bucket not in buckets:
        client.create_bucket(Bucket=settings.s3_bucket)


if __name__ == "__main__":
    ensure_bucket()
