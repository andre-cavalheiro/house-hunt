from dotenv import load_dotenv

from dataclasses import dataclass

from pydantic import BaseConfig, Extra, SecretStr, ValidationError
from pydantic_settings import BaseSettings


class RootConfig(BaseConfig):
    env_file: str = ".env"
    env_file_encoding: str = "utf-8"
    validate_default: bool = True
    case_sensitive: bool = False
    extra: Extra = Extra.ignore


class AppSettings(BaseSettings):
    """Application settings."""

    class Config(RootConfig):  # noqa: D106
        env_prefix = "APP_"

    NAME: str = "Bailout Bot"
    SLUG: str = "bailout_bot"
    ENVIRONMENT: str = "local"
    DEBUG: bool = False

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "prod"

    @property
    def is_local(self) -> bool:
        return self.ENVIRONMENT == "local"


class PrefectSettings(BaseSettings):
    """Prefect settings."""

    class Config(RootConfig):  # noqa: D106
        env_prefix = "PREFECT_"

    API_URL: str
    API_KEY: str
    WORK_POOL: str
    CRON_SCHEDULE: str


class PrefectBlocksSettings(BaseSettings):
    """Prefect settings."""

    class Config(RootConfig):  # noqa: D106
        env_prefix = "BLOCKS_"

    GITHUB_CREDENTIALS: str | None = None


class GitSettings(BaseSettings):
    """Git settings."""

    class Config(RootConfig):  # noqa: D106
        env_prefix = "GIT_"

    REPOSITORY_LINK: str
    ACCESS_TOKEN: SecretStr


class DockerSettings(BaseSettings):
    """Git settings."""

    class Config(RootConfig):  # noqa: D106
        env_prefix = "DOCKER_"

    USERNAME: str | None = None
    PASSWORD: SecretStr | None = None


@dataclass(frozen=True, kw_only=True, slots=True)
class SettingsConfig:
    app: AppSettings
    prefect: PrefectSettings
    blocks: PrefectBlocksSettings
    git: GitSettings
    docker: DockerSettings


_loaded_settings: SettingsConfig = None


def load_settings(force_reload: bool = False) -> SettingsConfig:
    global _loaded_settings
    if _loaded_settings is not None and not force_reload:
        return _loaded_settings

    load_dotenv()
    try:
        _loaded_settings = SettingsConfig(
            app=AppSettings(),
            prefect=PrefectSettings(),
            blocks=PrefectBlocksSettings(),
            git=GitSettings(),
            docker=DockerSettings(),
        )
    except ValidationError as exc:
        print(f"Error loading settings: {exc}")
        raise

    return _loaded_settings


config: SettingsConfig = load_settings()
