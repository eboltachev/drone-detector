from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://demo:demo_password@postgres:5432/drone_demo"
    cors_origins: str = "http://localhost:8080,http://127.0.0.1:8080"

    @property
    def origins(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]

settings = Settings()
