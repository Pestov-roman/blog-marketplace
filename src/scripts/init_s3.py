from src.settings import settings
from src.utils import s3 as _s3


async def ensure_bucket() -> None:
    client = _s3._get_client()
    buckets = {b["Name"] for b in client.list_buckets()["Buckets"]}
    if settings.s3_bucket not in buckets:
        client.create_bucket(Bucket=settings.s3_bucket)


if __name__ == "__main__":
    import asyncio

    asyncio.run(ensure_bucket())
