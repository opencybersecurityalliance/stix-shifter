"""Utils."""
import logging

from onecache import CacheDecorator


@CacheDecorator()
def get_debug_logger():
    """Get debug logger."""
    logger = logging.getLogger("aiosonic")
    # logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    return logger
