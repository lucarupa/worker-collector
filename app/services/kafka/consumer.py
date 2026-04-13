import json
from aiokafka import AIOKafkaConsumer

from app.adapter import CollectorAdapter
from app.core.interface.start_collector_interface import StartCollector
from app.exections.general_exception import GeneralException
from app.services.kafka import TOPIC, KAFKA_BOOTSTRAP, logger


async def start_kafka_consumer(collector: CollectorAdapter):
    consumer = AIOKafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        group_id="scrapper-group",
        auto_offset_reset="earliest",
    )
    logger.info(f"[KAFKA CONSUMER] Connecting to {KAFKA_BOOTSTRAP}, topic: {TOPIC}")
    await consumer.start()
    logger.info(f"[KAFKA CONSUMER] Started. Waiting for messages...")
    try:
        async for message in consumer:
            headers = {k: v.decode() for k, v in message.headers}
            if headers.get("collector") != "true":
                logger.info(
                    f"[KAFKA CONSUMER] Skipping message, missing collector header"
                )
                continue
            logger.info(f"[KAFKA CONSUMER] Raw message received: {message}")
            payload = json.loads(message.value.decode())
            try:
                info = StartCollector(**payload)
                logger.info(f"[KAFKA CONSUMER] start: {info.slug} - {info.id}")
                collector.execute(info)
            except GeneralException as e:
                logger.error(f"[KAFKA CONSUMER] GeneralException: {e}")
            except Exception as e:
                logger.error(f"[KAFKA CONSUMER] Exception: {e}")
    finally:
        await consumer.stop()
        logger.info(f"[KAFKA CONSUMER] Stopped.")
