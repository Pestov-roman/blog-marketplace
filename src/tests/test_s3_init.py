def test_bucket_created(monkeypatch):
    calls: list[str] = []

    class _Dummy:
        def list_buckets(self):
            return {"Buckets": []}

        def create_bucket(self, Bucket):
            calls.append(Bucket)

    monkeypatch.setattr("src.utils.s3._get_client", lambda: _Dummy())

    from src.scripts.init_s3 import ensure_bucket, settings

    ensure_bucket()
    assert calls == [settings.s3_bucket]
