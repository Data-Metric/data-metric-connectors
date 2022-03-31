from __future__ import annotations

import os
from datetime import date

from loguru import logger

from data_metric_connector.logger.logger import get_logger


def test_get_logger_path():
    today = date.today().strftime("%d-%d-%Y")
    get_logger()
    assert os.path.exists(f"logs/{str(today)}.log") is True


def test_get_logger_log():
    log = get_logger()
    assert isinstance(log, type(logger)) is True
