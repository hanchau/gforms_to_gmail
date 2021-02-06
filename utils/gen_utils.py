import logging
from logging.handlers import RotatingFileHandler

def get_logger(log_file):
    format = logging.Formatter('%(asctime)s - %(message)s')
    logger = logging.getLogger(log_file)
    handler = RotatingFileHandler(log_file, mode='a', maxBytes=2000000, backupCount=10)
    logger.setLevel(logging.INFO)
    handler.setFormatter(format)
    logger.addHandler(handler)
    return logger