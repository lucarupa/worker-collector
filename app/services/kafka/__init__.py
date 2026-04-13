from app.utils.logger import AppLogger

KAFKA_BOOTSTRAP = "localhost:9092"
TOPIC = "start-scrapper"

logger = AppLogger("[KAFKA]", "app.log").get_logger()
