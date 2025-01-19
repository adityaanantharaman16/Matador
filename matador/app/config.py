from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str = "mongodb+srv://nirajnad:MatadorDatabase@cluster0.cnaa3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    database_name: str = "Matador"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()