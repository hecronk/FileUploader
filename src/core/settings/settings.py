from dotenv import load_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()

class Settings(BaseSettings):
    # Метаданные о конфигурации
    model_config = SettingsConfigDict(env_file="src/core/settings/.env", env_file_encoding="utf-8")

    # Параметры БД
    db_user: str
    db_password: str
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str

    # Прочие параметры
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    media_path: str
    password_pepper: str
    debug: bool = False

    @property
    def database_url(self) -> str:
        """Готовая строка подключения к SQLAlchemy"""
        return f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

# Создаём глобальный объект настроек
settings = Settings()
