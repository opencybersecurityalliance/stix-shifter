import sys
import logging
from colorlog import ColoredFormatter

DEBUG = False

def set_logger(module):
    logger = logging.getLogger(module)
    handler = logging.StreamHandler()
    formatter = ColoredFormatter('%(log_color)s %(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    
    return logger