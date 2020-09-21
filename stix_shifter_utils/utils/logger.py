import logging
from colorlog import ColoredFormatter
import traceback
import jsonmerge
import threading

loggers = {}

def init(level):
    handler = logging.StreamHandler()
    formatter = ColoredFormatter('%(log_color)s %(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                                 reset=True,
                                 log_colors={
                                   'DEBUG':    'cyan',
                                   'INFO':     'white',
                                   'WARNING':  'yellow',
                                   'ERROR':    'red',
                                   'CRITICAL': 'red,bg_white',
                                 },
                                 secondary_log_colors={}
                                 )
    handler.setFormatter(formatter)
    logging.basicConfig(level=level, handlers=(handler,))

    jsonmerge.log.setLevel(logging.INFO)

def set_external_logger(logger):
    thread_local = threading.local()
    loggers[thread_local.thread_id] = logger

def set_logger(module):
    thread_local = threading.local()
    if thread_local.thread_id in loggers:
        return loggers[thread_local.thread_id]
    logger = logging.getLogger(module)
    return logger


def exception_to_string(excp):
    stack = traceback.extract_stack()[:-3] + traceback.extract_tb(excp.__traceback__)
    pretty = traceback.format_list(stack)
    return ''.join(pretty) + '\n  {} {}'.format(excp.__class__, excp)
