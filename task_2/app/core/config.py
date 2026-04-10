from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_FILE_PATH: Path = BASE_DIR / "data" / "facts.txt"

    host: HttpUrl
    timeout: float = 5

    @property
    def host_by_str(self) -> str:
        return str(self.host)

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_prefix="APP__",
        case_sensitive=False,
    )


settings = Settings()
