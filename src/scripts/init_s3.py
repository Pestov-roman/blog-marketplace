from src.settings import settings
from src.utils import s3 as _s3


async def ensure_bucket() -> None:
    # В CI/CD используем localhost вместо minio
    endpoint = (
        "http://localhost:9000" if settings.app_env == "ci" else settings.s3_endpoint
    )
    client = _s3._get_client(endpoint_url=endpoint)
    buckets = {b["Name"] for b in client.list_buckets()["Buckets"]}
    if settings.s3_bucket not in buckets:
        client.create_bucket(Bucket=settings.s3_bucket)


if __name__ == "__main__":
    import asyncio

    asyncio.run(ensure_bucket())
