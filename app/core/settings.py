from decouple import config
from app.schemas.settings import Settings


settings = Settings(
    env=config("ENV"),
    name=config("NAME", default="PyCon Togo Official Website"),
    version=config("VERSION", default="1.2.0"),
    algorithm=config("ALGORITHM"),
    secret_key=config("SECRET_KEY"),
    access_token_expire_minutes=config(
        "ACCESS_TOKEN_EXPIRE_MINUTES", cast=int),
    supabase_url=config("SUPABASE_URL"),
    supabase_key=config("SUPABASE_KEY"),
    smtp_server=config("SMTP_SERVER"),
    smtp_port=config("SMTP_SERVER_PORT", cast=int),
    smtp_user=config("SENDER_EMAIL"),
    smtp_pass=config("SENDER_EMAIL_PASSWORD"),
    python_togo_api_base_url=config("PYTHON_TOGO_API_BASE_URL"),
    python_togo_api_key=config("PYTHON_TOGO_API_KEY"),
    python_togo_api_timeout_seconds=config(
        "PYTHON_TOGO_API_TIMEOUT_SECONDS", cast=int, default=12
    ),
    python_togo_event_code=config("PYTHON_TOGO_EVENT_CODE"),
)
