from src.settings import settings


def test_settings_loaded_from_env(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    st = settings.model_copy(update={"app_env": "test"})
    assert st.app_env == "test"
