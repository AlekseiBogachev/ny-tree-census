# # -*- coding: utf-8 -*-
"""Загрузка исходного датасета и его описания."""

import logging
from pathlib import Path

import click
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


cli.add_command(get_description)


if __name__ == "__main__":
    cli()
