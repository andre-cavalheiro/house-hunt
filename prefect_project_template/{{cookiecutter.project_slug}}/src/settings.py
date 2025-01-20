from dotenv import load_dotenv

from dataclasses import dataclass

from pydantic import BaseConfig, Extra, ValidationError
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
    SLUG: str = "{{cookiecutter.project_slug}}"
    ENVIRONMENT: str = "local"
    DEBUG: bool = False

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "prod"

    @property
    def is_local(self) -> bool:
        return self.ENVIRONMENT == "local"


class DevelopmentSettings(BaseSettings):
    """Development settings."""

    class Config(RootConfig):  # noqa: D106
        env_prefix = "DEVELOPMENT_"

    ENABLED: bool = False

    def __post_init__(self):
        # This method is called after the model is fully initialized
        if not self.ENABLED:
            for key, field in self.model_fields.items():
                if key != "ENABLED":
                    if field.annotation is bool:
                        setattr(self, key, False)
                    else:
                        setattr(self, key, None)


class LoggingSettings(BaseSettings):
    """Logging settings."""

    class Config(RootConfig):  # noqa: D106
        env_prefix = "LOGGING_"

    LEVEL: str = "INFO"
    FORMAT: str = "{name}:{function}:{line} - {message}"


@dataclass(frozen=True, kw_only=True, slots=True)
class SettingsConfig:
    app: AppSettings
    development: DevelopmentSettings
    logging: LoggingSettings


_loaded_settings: SettingsConfig = None


def load_settings(force_reload: bool = False) -> SettingsConfig:
    global _loaded_settings
    if _loaded_settings is not None and not force_reload:
        return _loaded_settings

    load_dotenv()
    try:
        _loaded_settings = SettingsConfig(
            app=AppSettings(),
            development=DevelopmentSettings(),
            logging=LoggingSettings(),
        )
    except ValidationError as exc:
        print(f"Error loading settings: {exc}")
        raise

    return _loaded_settings


config: SettingsConfig = load_settings()
