from typing import Literal, Optional

from pydantic import BaseSettings, SecretStr


class KafkaConfig(BaseSettings):
    host: str
    port: int = 9092
    user: Optional[str]
    password: Optional[SecretStr]
    security_protocol: Literal['PLAINTEXT', 'SSL', 'SASL_PLAINTEXT', 'SASL_SSL'] = 'PLAINTEXT'

    class Config:
        case_sensitive = False
        allow_mutation = False
        env_prefix = 'KAFKA_'
