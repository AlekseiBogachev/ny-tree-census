# # -*- coding: utf-8 -*-
"""Загрузка исходного датасета и его описания."""

import logging
import os
import typing
from io import StringIO
from pathlib import Path
from typing import Any, Dict

import click
import pandas as pd
import requests

from src import setup_logging_to_file

logger: logging.Logger = setup_logging_to_file()
project_dir: Path = Path(__file__).resolve().parents[2]


@click.group()
def cli() -> None:
    """Загрузка исходного датасета и его описания."""
    pass


@click.command()
@click.option(
    "-o",
    "--output-path",
    "output_path",
    default=Path.joinpath(project_dir, "references"),
    help="Каталог, в который будет сохранено описание данных. "
    "Значение по умолчанию <project_dir>/references/",
    show_default=True,
    type=click.Path(exists=True),
)
@click.option(
    "-cs",
    "--chunk-size",
    "chunk_size",
    default=128,
    help="Размер загружаемого блока. См. requests.Response.iter_content "
    "параметр chunk_size.",
    show_default=True,
    type=int,
)
def get_description(output_path: str, chunk_size: int) -> None:
    """Загружает описание исходных данных.

    Загружает описание исходных данных в формате .pdf с сайта
    https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data
    /uvpi-gqnh/about_data в каталог, указанный в параметре output_path.
    Значение output_path по умолчанию <project_dir>/references/. Файлу, с
    описанием даётся имя ny_tree_census_description.pdf, если файл с таким
    именем существует, он будет перезаписан.\f

    Parameters
    ----------
    output_path : str
        Каталог, в который будет загружено описание данных в формате .pdf.
        Значение по умолчанию <project_dir>/references/ .
    chunk_size: int
        Размер загружаемого блока. См. requests.Response.iter_content параметр
        chunk_size. Значение по умолчанию 128.
    """
    url: str = "https://data.cityofnewyork.us/api/views/uvpi-gqnh/files/8705bfd6-993c-40c5-8620-0c81191c7e25?download=true&filename=StreetTreeCensus2015TreesDataDictionary20161102.pdf"

    logger.info(
        f"Загрузка описания исходных данных по ссылке {url}. "
        f"Описание будет сохранено в каталог {output_path}."
    )

    r: requests.Response = requests.get(url, stream=True)

    with open(
        Path.joinpath(Path(output_path), "ny_tree_census_description.pdf"), "wb"
    ) as file:
        for i, chunk in enumerate(r.iter_content(chunk_size=chunk_size)):
            file.write(chunk)
            logger.info(f"Загружено {i * chunk_size} Байт.")

    return None


def request_soda_json(
    endpoint: str, params: Dict[str, Any], timeout: int = 10
) -> pd.DataFrame:
    """Выполняет запрос к SODA API и возвращает pd.DataFrame с данными.

    Выполняет запрос к SODA API с конечной точкой endpoint и параметрами params,
    получает ответ и обрабатывает его как csv (с помощью pd.read_csv()).
    Возвращает pd.DataFrame с полученными данными.
    См. https://dev.socrata.com/foundry/data.cityofnewyork.us/uvpi-gqnh .

    В случае, если запрос к SODA API завершился с ошибками
    requests.exceptions.Timeout или requests.exceptions.HTTPError, то эти ошибки
    перехватываются, и иформация о них записывается в каталог
    <project_dir>/logs.

    Parameters
    ----------
    endpoint : str
        Конечная тока - адрес, по которому будет оправлен запрос.
        Для корректной работы должна возвращать csv.
    timeout: int, optional
        Время ожидания ответа от сервера в секундах, после которого будет
        вызвана ошибка. Значение по умолчанию 10.
    params : Dict[str, Any]
        Параметры запроса.

    Returns
    -------
    pd.DataFrame
        DataFrame с ответом SODA API. Если ответ не был получен или запрос
        завершился ошибкой, то возвращает пустой DataFrame. Если ответ был
        получен и успешно обработан, то возвращается DataFrame с полученными
        данными.
    """
    resp_json: pd.DataFrame = pd.DataFrame()
    try:
        response: requests.Response = requests.get(
            endpoint,
            params=params,
            timeout=timeout,
        )

        response.raise_for_status()

        logger.info(
            "Отправка запроса. "
            f"url: {response.url} ; "
            f"status code: {response.status_code} ; "
            f"encoding: {response.encoding} ; "
        )

        resp_json = pd.read_csv(StringIO(response.text))

    except requests.exceptions.Timeout:
        logger.error("Timeout!", exc_info=True)

    except requests.exceptions.HTTPError:
        logger.error("HTTPError!", exc_info=True)

    else:
        logger.info(
            "Запрос успешно вернул ответ. "
            f"Длина ответа {len(response.content)} Байт."
        )

    return resp_json


@click.command()
@click.option(
    "-o",
    "--output-path",
    "output_path",
    default=Path.joinpath(project_dir, "data", "raw"),
    help="Каталог, в который будет сохранён файл с исходными данными "
    "в формате csv. "
    "Значение по умолчанию <project_dir>/data/raw/",
    show_default=True,
    type=click.Path(exists=True),
)
@click.option(
    "-cs",
    "--chunk-size",
    "chunk_size",
    default=1000,
    help="Количество строк, загружаемых за 1 запрос. API поставщика данных"
    "ограничивает количество строк 1000.",
    show_default=True,
    type=int,
)
@click.option(
    "-m",
    "--max-rows",
    "maxrows",
    default=-1,
    help="Общее количество загруженных строк. Если -1,"
    "то загрузить весь датасет.",
    show_default=True,
    type=int,
)
@click.option(
    "-t",
    "--timeout",
    "timeout",
    default=10,
    help="Время ожидания ответа от сервера в секундах, после которого будет "
    "вызвана ошибка.",
)
def get_data(
    output_path: str,
    chunk_size: int = 1000,
    maxrows: int = -1,
    timeout: int = 10,
) -> int:
    """Загружает датасет в формате .csv через SODA API.

    Загружает данные в формате .csv с помощью SODA API
    (см. https://dev.socrata.com/foundry/data.cityofnewyork.us/uvpi-gqnh)
    и сохраняет их в каталог output_path в файл data.csv. Если файл с таким
    именем существует, то он перезаписывается.

    В случае, если запрос к SODA API завершился с ошибками
    requests.exceptions.Timeout или requests.exceptions.HTTPError, то эти
    ошибки перехватываются, и иформация о них записывается в каталог
    <project_dir>/logs.

    Поставщик данных ограничивает количество строк, загружаемых за 1 запрос,
    до 1000.\f

    Parameters
    ----------
    output_path : str
        Каталог, в которой будет сохранён файл с исходными данными data.csv .
        Значение по умолчанию <project dir>/data/raw/ .
    chunk_size : int, optional
        Количество строк загружаемых за 1 запрос. API поставщика данных
        ограничивает количество строк 1000." Значение по умолчанию 1000.
    maxrows : int, optional
        Общее количество загруженных строк. Если -1, то загружает весь датасет.
        Если значение maxrows больше -1, но меньше chunk_size, то будет
        загружено chunk_size строк. Значение по умолчанию -1.
    timeout: int, optional
        Время ожидания ответа от сервера в секундах, после которого будет
        вызвана ошибка. Значение по умолчанию 10.

    Returns
    -------
    int
        Количество полученных строк.
    """
    endpoint: str = "https://data.cityofnewyork.us/resource/uvpi-gqnh.csv"

    logger.info("Загрузка датасета через SODA API.")
    query_params: Dict[str, Any] = {"$select": "count(*)"}

    dataset_len = typing.cast(
        int,
        request_soda_json(endpoint, params=query_params, timeout=timeout).loc[
            0, "count"
        ],
    )
    logger.info(f"Количество наблюдений в исходном датасете: {dataset_len}")

    file_name: Path = Path(output_path).joinpath("data.csv")
    logger.info(f"Данные будут сохранены в файл {file_name}")

    if file_name.exists():
        logger.info(f"Файл {file_name} существует.")
        os.remove(file_name)
        logger.info(f"Файл {file_name} удалён.")

    logger.info(f"Создаём файл {file_name}.")

    n_data_rows: int = 0

    query_params = {
        "$limit": chunk_size,
        "$offset": 0,
        "$order": "tree_id",
    }

    if maxrows < 0:
        maxrows = dataset_len
    logger.info(f"Будет загружено строк: {maxrows}.")

    while True:
        logger.info(
            f"Загрузка строк с {query_params['$offset']} "
            f"по {query_params['$offset'] + query_params['$limit']}."
        )

        new_data: pd.DataFrame = request_soda_json(
            endpoint, params=query_params, timeout=timeout
        )

        new_data.to_csv(
            file_name,
            header=not (file_name.exists()),
            index=False,
            mode="a",
        )

        logger.info(f"Строки записаны в файл {file_name}")

        n_data_rows = query_params["$offset"] + len(new_data)
        logger.info(f"Получено строк {n_data_rows} / {maxrows}.")

        if query_params["$offset"] + query_params["$limit"] < maxrows:
            query_params["$offset"] += query_params["$limit"]
        else:
            break

    logger.info(f"Датасет загружен. Получено строк: {n_data_rows}")

    return n_data_rows


cli.add_command(get_description)
cli.add_command(get_data)


if __name__ == "__main__":
    cli()
