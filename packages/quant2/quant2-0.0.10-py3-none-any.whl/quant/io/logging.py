import logging


def setup_logging(filename="runs/log.txt", level=logging.INFO):
    logging.basicConfig(
        filename=filename,
        format="%(asctime)s:%(levelname)s:%(module)s:%(funcName)s:%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=level,
        encoding="utf8",
    )


def get_logger(name):
    return logging.getLogger(name)


def print_log(msg, logger=None, level=logging.INFO):
    print(msg)
    if logger is not None:
        logger.log(level, msg)
    else:
        logging.log(level, msg)
