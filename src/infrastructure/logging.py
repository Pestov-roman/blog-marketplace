from __future__ import annotations

import logging
import os
import sys
from typing import Any

import structlog
from structlog.typing import EventDict

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_JSON = bool(int(os.getenv("LOG_JSON", "0")))


def _add_log_level(_: Any, __: str, event: EventDict) -> EventDict:
    event["level"] = event["level"].upper()
    return event


def _add_logger_name(_: Any, __: str, event: EventDict) -> EventDict:
    if "logger" in event:
        event["logger"] = __
    return event


def configure_logging() -> None:
    timestamper = structlog.processors.TimeStamper(fmt="iso")

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            timestamper,
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
