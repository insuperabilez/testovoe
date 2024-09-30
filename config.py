from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    # Elasticsearch
    ELASTICSEARCH_HOST: str
    ELASTICSEARCH_PORT: str
    ELASTICSEARCH_USER: str
    ELASTICSEARCH_PASSWORD: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()