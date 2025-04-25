from settings import settings


def test_env_loaded():
    assert settings.pg_host == "db"
    assert settings.pg_port == 5432
    assert settings.pg_db == "marketplace_blog"
    assert settings.pg_user == "postgres"
    assert settings.pg_password == "postgres"
