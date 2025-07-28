import logging
import os
from datetime import datetime

class CustomLogger:
    def __init__(self, logs_dir="logs"):
        #Ensure Log Directory Exists
        print(os.getcwd())
        logs_dir = os.path.join(os.getcwd(), logs_dir)
        os.makedirs(logs_dir, exist_ok=True)

        #Create timestamped LogFile

        log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
        log_file_path = os.path.join(logs_dir, log_file)

        #Configure Logging
        logging.basicConfig(
            filename=log_file_path,
            format="[ %(asctime)s ] %(levelname)s %(name)s (line:%(lineno)d) - %(message)s",
            level=logging.INFO,
        )

    def get_logger(self, name=__file__):
        return logging.getLogger(os.path.basename(name))
        

