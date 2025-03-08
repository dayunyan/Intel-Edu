from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "教育辅助系统"
    DATABASE_URL: str
    MILVUS_HOST: str
    MILVUS_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    LLM_SERVER_URL: str
    OPENAI_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()
