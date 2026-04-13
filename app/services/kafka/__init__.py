from dotenv import load_dotenv

from app.core.env.kafka_env import KafkaEnv
from app.utils.logger import AppLogger

load_dotenv()


logger = AppLogger("[KAFKA]", "app.log").get_logger()

environment_variables = KafkaEnv().search_environment_variables()
