from pydantic import BaseSettings, Extra, SecretStr
from typing import Optional


class DatabaseConfig(BaseSettings):
    host: SecretStr
    port: int
    user: SecretStr
    password: SecretStr

    class Config:
        extra = Extra.ignore


class MySQLConfig(DatabaseConfig):
    port: int = 3306
    db: Optional[str]


class PostgresConfig(DatabaseConfig):
    port: int = 5432
    database: str
