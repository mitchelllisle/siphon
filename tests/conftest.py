import json
from typing import Type

import pytest
from aio_pika import IncomingMessage
from aio_pika.message import DeliveredMessage
from pamqp import ContentHeader
from pamqp.specification import Basic

from siphon import AioKafkaConsumer, KafkaConfig, RabbitConfig


@pytest.fixture()
def kafka_config() -> KafkaConfig:
    config = KafkaConfig()
    return config


@pytest.fixture()
def kafka_consumer() -> Type[AioKafkaConsumer]:
    class MyConsumer(AioKafkaConsumer):
        def on_message(self, message, body: bytes):
            pass

    return MyConsumer


@pytest.fixture()
def rabbit_config() -> RabbitConfig:
    config = RabbitConfig()
    return config


@pytest.fixture()
def mock_message() -> IncomingMessage:
    message = DeliveredMessage(
        channel=None,
        delivery=Basic.Deliver(),
        header=ContentHeader(),
        body=json.dumps({'message': 'this is a mock message'}).encode(),
    )
    return IncomingMessage(message)
