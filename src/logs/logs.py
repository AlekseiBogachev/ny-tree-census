# -*- coding: utf-8 -*-
"""Логирование."""

import logging
from pathlib import Path
from typing import Union


def setup_logging_to_file(
    dir: Union[str, None] = None,
    format_str: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
) -> logging.Logger:
    """Возвращает настроенный логер для записи журнала.

    Возвращает настроенный логер для записи журнала в формате format_str в
    каталог dir. Если dir равен None, то журнал будет записываться в каталог
    <project_dir>/logs

    Parameters
    ----------
    dir : str, optional
        Каталог, в который будет записан журнал. По умолчанию None.
    format_str : str, optional
        Формат строк в журнале, по умолчанию
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'. Подробнее в
        описании модуля logging стандартной библиотеки.

    Returns
    -------
    logging.Logger
        Настроенный логер.
    """
    project_dir: Path = Path(__file__).resolve().parents[2]
    logs_path: Path = Path.joinpath(project_dir, "logs")

    if dir is not None:
        logs_path = Path(dir)

    logs_path.mkdir(parents=True, exist_ok=True)

    logger: logging.Logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    raw_data_handler: logging.FileHandler = logging.FileHandler(
        Path.joinpath(logs_path, f"{__name__}.log"), mode="a"
    )
    raw_data_formatter: logging.Formatter = logging.Formatter(format_str)

    raw_data_handler.setFormatter(raw_data_formatter)
    logger.addHandler(raw_data_handler)

    return logger
