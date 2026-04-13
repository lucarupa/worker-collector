from aiokafka import AIOKafkaConsumer
from pydantic import json

from app.adapter import CollectorAdapter
from app.core.interface.start_collector_interface import StartCollector
from app.exections.general_exception import GeneralException
from app.services.kafka import TOPIC, KAFKA_BOOTSTRAP


async def start_kafka_consumer(collector: CollectorAdapter):
    consumer = AIOKafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id="scrapper-group",
        auto_offset_reset="earliest",
    )
    await consumer.start()
    print(f"[KAFKA CONSUMER] Kafka consumer started.]")
    try:
        async for message in consumer:
            payload = json.loads(message.value.decode())
            print(f"[KAFKA CONSUMER] {payload}")
            try:
                info = StartCollector(**payload)
                collector.execute(info)
            except GeneralException as e:
                print(f"[KAFKA CONSUMER] {e}")
            except Exception as e:
                print(f"[KAFKA CONSUMER] {e}")
    finally:
        await consumer.stop()
