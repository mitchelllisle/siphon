from typing import Optional

from pydantic import BaseSettings, SecretStr


class KafkaConfig(BaseSettings):
    host: str
    port: int = 9092
    user: Optional[str]
    password: Optional[SecretStr]

    class Config:
        case_sensitive = False
        allow_mutation = False
        env_prefix = 'KAFKA_'
