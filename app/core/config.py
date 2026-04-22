from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Imóvel Direto Monitor"
    app_env: str = "development"
    secret_key: str = "change-me"
    database_url: str = "sqlite:///./imovel_monitor.db"
    admin_email: str = "admin@example.com"
    admin_password: str = "change-me-now"
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    alert_min_score: int = 70

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
