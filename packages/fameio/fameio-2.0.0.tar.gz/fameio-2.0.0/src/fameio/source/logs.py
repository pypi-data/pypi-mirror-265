# SPDX-FileCopyrightText: 2023 German Aerospace Center <fame@dlr.de>
#
# SPDX-License-Identifier: Apache-2.0

import logging as log
from pathlib import Path
from typing import NoReturn, Optional, List

LOG_LEVELS = {
    "critical": log.CRITICAL,
    "error": log.ERROR,
    "warn": log.WARNING,
    "warning": log.WARNING,
    "info": log.INFO,
    "debug": log.DEBUG,
}

_loggers: List[log.Logger] = []

_FORMAT_NORMAL = "%(asctime)s — %(levelname)s — %(message)s"  # noqa
_FORMAT_DETAILLED = "%(asctime)s.%(msecs)03d — %(levelname)s — %(module)s:%(funcName)s:%(lineno)d — %(message)s"  # noqa
_TIME_FORMAT = "%H:%M:%S"

_WARN_ALREADY_INITIALIZED = "Cannot set up new FAMEIO logger: using existing logger with previous settings."
_WARN_NOT_INITIALIZED = "Logger not initialised for FAMEIO - using default root logger"

LOGGER_NAME = "fameio"


def logger() -> log.Logger:
    """Returns already set up FAME-Io's logger or - if not set up - a new logger with level `INFO`"""
    if not _loggers:
        set_up_logger("info")
        log.warning(_WARN_NOT_INITIALIZED)
    return _loggers[0]


def log_and_raise_critical(message: str) -> NoReturn:
    """Raises a critical error and logs with given `error_message`"""
    logger().critical(message)
    raise Exception(message)


def log_error_and_raise(exception: Exception) -> NoReturn:
    """Raises the specified `exception` and logs an error with the same `message`"""
    logger().error(str(exception))
    raise exception


def set_up_logger(level_name: str, file_name: Optional[Path] = None) -> None:
    """Uses existing logger or sets up logger"""
    if not _loggers:
        _loggers.append(log.getLogger(LOGGER_NAME))
        level = LOG_LEVELS.get(level_name.lower())
        _set_log_level(level)
        formatter = _get_formatter(level)
        _add_handler(log.StreamHandler(), formatter)
        if file_name:
            _add_handler(log.FileHandler(file_name, mode="w"), formatter)
    else:
        log.warning(_WARN_ALREADY_INITIALIZED)


def _set_log_level(level: int) -> None:
    """Set the global log level to given `level`"""
    logger().setLevel(level)


def _get_formatter(level: int) -> log.Formatter:
    """
    Returns a log formatter depending on the given log `level`
    Args:
        level: this log level determines how detailed the logger's output is
    Returns:
        new log formatter
    """
    return log.Formatter(_FORMAT_DETAILLED if level is log.DEBUG else _FORMAT_NORMAL, _TIME_FORMAT)


def _add_handler(handler: log.Handler, formatter: log.Formatter) -> None:
    """Adds given `handler` to root logger using the specified `formatter`"""
    handler.setFormatter(formatter)
    logger().addHandler(handler)
