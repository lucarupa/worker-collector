import json

from aiokafka import AIOKafkaProducer

from app.services.kafka import KAFKA_BOOTSTRAP


async def publish_bot_event(payload: dict):
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP)
    await producer.start()
    try:
        await producer.send(
            "start-bot", value=json.dumps(payload).encode(), headers=[("bot", b"true")]
        )
        await producer.flush()
    finally:
        await producer.stop()
