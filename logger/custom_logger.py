import logging
import os
from datetime import datetime
import structlog

class CustomLogger:
    def __init__(self, logs_dir="logs"):
        #Ensure Log Directory Exists
        logs_dir = os.path.join(os.getcwd(), logs_dir)
        os.makedirs(logs_dir, exist_ok=True)

        #Create timestamped LogFile
        log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        self.log_file_path = os.path.join(logs_dir, log_file)

    def get_logger(self, name=__file__):
        logger_name = os.path.basename(name)

        #Configure logging for both console + file (both JSON)
        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(message)s")) #RAW JSON lines

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(message)s"))

        logging.basicConfig(
            level = logging.INFO,
            format = "%(message)s",
            handlers = [console_handler, file_handler]
        )

        #Configure structLog for JSON structured logging

        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso", utc="True", key="timestamp"),
                structlog.processors.add_log_level,
                structlog.processors.EventRenamer(to="event"),
                structlog.processors.JSONRenderer()
            ],
            logger_factory = structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use = True,
        )
        return structlog.get_logger(logger_name)

# Usage Examples

if __name__=="__main__":
    logger = CustomLogger().get_logger(__file__)
    logger.info("user uplaoded a file ", user_id=123)