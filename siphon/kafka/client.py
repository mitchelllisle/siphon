import ssl
from abc import ABC, abstractmethod
from asyncio import Future
from typing import ClassVar, List

import aiokafka as kafka

from siphon.logger import logger
from siphon.kafka.config import KafkaConfig


class AioKafkaConsumer(ABC):
    name: ClassVar[str] = 'siphon-aiokafka-consumer'  # noqa
    consumer: kafka.AIOKafkaConsumer

    def __init__(self, config: KafkaConfig, topics: List[str]):
        self.config = config
        self.topics = topics
        self.ssl_context = ssl.SSLContext()

    async def _kafka_startup(self):
        self.consumer = kafka.AIOKafkaConsumer(
            *self.topics,
            client_id=self.name,
            bootstrap_servers=f'{self.config.host}:{self.config.port}',
            security_protocol='SASL_SSL',
            ssl_context=self.ssl_context,
            sasl_plain_username=self.config.user,
            sasl_plain_password=self.config.password.get_secret_value() if self.config.password
            else None,
        )
        logger.info(f'{self.name} starting consumer...')
        await self.consumer.start()
        logger.info(f'{self.name} consumer connected!')

    async def connect(self):
        logger.info(f'{self.name} connecting to kafka...')
        await self._kafka_startup()

    async def _kafka_shutdown(self):
        logger.info(f'{self.name} stopping consumer...')
        await self.consumer.stop()
        logger.info(f'{self.name} consumer stopped!')

    async def on_startup(self):
        pass

    async def on_shutdown(self):
        pass

    @abstractmethod
    async def on_message(self, message: kafka.ConsumerRecord, body: bytes):
        pass

    async def __aenter__(self):
        await self.connect()
        await self.on_startup()
        return self

    async def __aexit__(self, *args):
        await self._kafka_shutdown()
        await self.on_shutdown()

    async def __call__(self, *args, **kwargs):
        async with self as worker:
            async for message in worker.consumer:
                await self.on_message(message, message.value)


class AioKafkaProducer:
    name: ClassVar[str] = 'siphon-aiokafka-producer'  # noqa
    producer: kafka.AIOKafkaProducer

    def __init__(self, config: KafkaConfig):
        self.config = config
        self.ssl_context = ssl.SSLContext()

    async def _kafka_startup(self):
        self.producer = kafka.AIOKafkaProducer(
            client_id=self.name,
            bootstrap_servers=f'{self.config.host}:{self.config.port}',
            security_protocol='SASL_SSL',
            ssl_context=self.ssl_context,
            sasl_plain_username=self.config.user,
            sasl_plain_password=self.config.password.get_secret_value(),
        )
        await self.producer.start()

    async def _kafka_shutdown(self):
        await self.producer.stop()

    async def on_startup(self):
        pass

    async def on_shutdown(self):
        pass

    async def connect(self):
        await self._kafka_startup()

    async def __aenter__(self):
        await self.connect()
        await self.on_startup()
        return self

    async def __aexit__(self, *args):
        await self._kafka_shutdown()
        await self.on_shutdown()

    async def send(
        self,
        topic: str,
        value=None,
        key=None,
        partition=None,
        timestamp_ms=None,
        headers=None,
        wait: bool = False,
    ) -> Future:
        if wait:
            sender = self.producer.send_and_wait
        else:
            sender = self.producer.send
        return await sender(
            topic=topic,
            value=value,
            key=key,
            partition=partition,
            timestamp_ms=timestamp_ms,
            headers=headers,
        )
