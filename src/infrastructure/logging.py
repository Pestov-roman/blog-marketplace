from __future__ import annotations

import logging
import os
import sys
from typing import Any

import structlog
from structlog.processors import JSONRenderer
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
    shared_processors = [
        structlog.processors.TimeStamper(fmt="iso"),
        _add_logger_name,
        _add_log_level,
    ]

    structlog.configure(
        processors=shared_processors
        + ([JSONRenderer()] if LOG_JSON else [structlog.dev.ConsoleRenderer()]),
        wrapper_class=structlog.male_filtering_bound_logger(
            logging.getLevelName(LOG_LEVEL)
        ),
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
    )

    logging.basicConfig(
        level=LOG_LEVEL,
        handlers=[
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter(
                logging.StreamHandler(),
                foreign_pre_chain=shared_processors,
                processor=(
                    JSONRenderer() if LOG_JSON else structlog.dev.ConsoleRenderer()
                ),
            )
        ],
    )
