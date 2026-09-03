from pydantic_settings import BaseSettings , SettingsConfigDict
from datetime import timedelta

class Settings(BaseSettings):
    DATABASE_URL : str
    JWT_SECRET : str
    JWT_ALGORITHM : str
    JWT_TOKEN_EXP : timedelta
    RazorpayKeyId : str
    RazorpayKeySecret : str
    
    model_config = SettingsConfigDict(
        env_file = ".env",
        extra = "ignore"
    )

Config = Settings()