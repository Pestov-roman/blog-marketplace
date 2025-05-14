from unittest.mock import MagicMock, patch

import pytest

from src.scripts.init_s3 import ensure_bucket


@pytest.mark.asyncio
async def test_bucket_created():
    mock_client = MagicMock()
    mock_client.list_buckets.return_value = {"Buckets": []}

    with patch("src.utils.s3._get_client", return_value=mock_client):
        await ensure_bucket()

        mock_client.create_bucket.assert_called_once()
