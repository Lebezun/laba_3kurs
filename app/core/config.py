from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    TEST_DATABASE_URL: str # ДОДАЛИ ЦЕ
    SECRET_KEY: str
    
    # Вказуємо, звідки брати змінні
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()