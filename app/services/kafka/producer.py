import json

from aiokafka import AIOKafkaProducer

from app.services.kafka import environment_variables


async def publish_bot_event(payload: dict):
    producer = AIOKafkaProducer(
        bootstrap_servers=environment_variables.bootstrap_servers
    )
    await producer.start()
    try:
        await producer.send(
            environment_variables.topic_producer,
            value=json.dumps(payload).encode(),
            headers=[("bot", b"true")],
        )
        await producer.flush()
    finally:
        await producer.stop()
