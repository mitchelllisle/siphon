from pydantic import BaseSettings, Extra


class DatabaseConfig(BaseSettings):
    host: str
    port: int
    user: str
    password: str

    class Config:
        extra = Extra.ignore
