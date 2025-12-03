import logging
import logging.config
import os
from typing import Optional

APP_LOG_NAME = "STIX_BUILD_TOOLS"
DEFAULT_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Minimal dictConfig (console-only, seconds precision)
LOG_CONFIG_MINIMAL = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(levelname)s [%(name)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": DEFAULT_LEVEL,
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {
        # Attach handlers to top-level app logger, children inherit
        APP_LOG_NAME: {
            "handlers": ["console"],
            "level": DEFAULT_LEVEL,
            "propagate": False,
        }
    },
}

_configured = False


def is_debug() -> bool:
    """
    Returns True if the root/app log level is DEBUG or lower.
    Can be used to conditionally show verbose output.
    """
    # Get top-level app logger
    logger = logging.getLogger(APP_LOG_NAME)
    return logger.isEnabledFor(logging.DEBUG)


def init_logging(level: Optional[str] = None) -> None:
    """
    Initialise logging using the minimal config.
    Call this exactly once from your application entrypoint (main).
    """
    global _configured
    if _configured:
        return

    if level:
        os.environ["LOG_LEVEL"] = level.upper()

    # update handler levels to reflect current LOG_LEVEL env
    log_level = os.getenv("LOG_LEVEL", DEFAULT_LEVEL).upper()
    LOG_CONFIG_MINIMAL["handlers"]["console"]["level"] = log_level
    LOG_CONFIG_MINIMAL["loggers"][APP_LOG_NAME]["level"] = log_level

    logging.config.dictConfig(LOG_CONFIG_MINIMAL)
    _configured = True


def get_logger(module_name: str) -> logging.Logger:
    """
    Return a logger named "APP_LOG_NAME.module_name" so you get:
    STIX_BUILD_TOOLS.some.module
    """
    return logging.getLogger(f"{APP_LOG_NAME}.{module_name}")
