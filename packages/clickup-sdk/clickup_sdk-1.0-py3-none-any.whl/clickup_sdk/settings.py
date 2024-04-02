from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CLICK_UP_",
    )

    AUTHORIZATION: str


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
