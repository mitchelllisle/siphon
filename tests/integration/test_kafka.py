import pytest
from aiokafka import AIOKafkaConsumer


@pytest.mark.asyncio
async def test_consumer_worker_setup(kafka_config, kafka_consumer):
    worker = kafka_consumer(kafka_config, ['test'])

    await worker._kafka_startup()
    assert isinstance(worker.consumer, AIOKafkaConsumer)

    await worker._kafka_shutdown()


@pytest.mark.asyncio
async def test_producer_worker_setup(kafka_config, kafka_consumer):
    worker = kafka_consumer(kafka_config, ['test'])

    await worker._kafka_startup()
    assert isinstance(worker.consumer, AIOKafkaConsumer)

    await worker._kafka_shutdown()
