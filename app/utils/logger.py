from logging import getLogger, StreamHandler, Formatter, DEBUG


def setup_logger():
    logger = getLogger("pycontg")
    logger.setLevel(DEBUG)

    handler = StreamHandler()
    handler.setLevel(DEBUG)

    formatter = Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
