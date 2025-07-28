from logger.custom_logger import CustomLogger

if __name__ == "__main__":
    print("hello")
    logger = CustomLogger()
    log = logger.get_logger(__file__)
    log.info("Custom Logger testing ")