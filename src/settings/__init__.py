from .base import Settings, get_settings

settings: Settings = get_settings()

__all__ = ["settings", "get_settings", "Settings"]
