# -*- coding: utf-8 -*-
"""Вывод и визуализации информации о данных."""

from typing import Any, Callable, Dict, List, Literal, Tuple, Union

import matplotlib.pyplot as plt
import missingno as msno
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import display
from matplotlib.colors import LinearSegmentedColormap


def review_data(df: pd.DataFrame, n_rows: int = 10) -> None:
    """Вывод общей информации о датафрейме.

    Выводит количество строк и столбцов в датафрейме, его первые n_rows строк,
    общую информацию о столбцах (результат df.info()), описательные статистики
    (df.describe()) отдельно для категориальных и количественных признаков.
    При выводе на экран таблицы функция печатает все её столбцы и все строки,
    если их количество явно не ограничено одним из параметров функции.

    Parameters
    ----------
    df: pd.DataFrame
        Датафрейм с данными.
    n_rows: int
        Количество первых строк, которые будут выведены.
        Значение по умолчанию 10.
    """
    with pd.option_context(
        "display.max_columns", None, "display.max_rows", None
    ):
        print(f"В данных\nстрок: {df.shape[0]}\nстолбцов: {df.shape[1]}")
        print()

        print("Первые 10 строк таблицы:")
        display(df.head(n_rows))
        print()

        print("Общая информация о столбцах:")
        df.info()
        print()

        print("Доля пропусков в каждом признаке:")
        display((df.isna().sum() / len(df)).round(2))

        msno.matrix(df, figsize=(15, 5))
        plt.title("Распределение пропусков по таблице", fontsize=20)
        plt.show()

        msno.bar(df, figsize=(15, 5))
        plt.title("Количество непустых значений в каждом столбце", fontsize=20)
        plt.show()

        try:
            print("Описательные статистики для числовых признаков:")
            display(
                (
                    df.describe(
                        include=["number"],
                        percentiles=[0.1, 0.25, 0.5, 0.75, 0.9],
                    ).transpose()
                )
            )
        except ValueError:
            print("Числовые признаки отсутствуют.")

        try:
            print("Описательные статистики для категориальных признаков:")
            display(df.describe(include=["object"]).transpose())
        except ValueError:
            print("Категориальные признаки отсутствуют.")

        print()

        if df.duplicated().any():
            print("В данных есть дубликаты!")
        else:
            print("Дубликаты не обнаружены.")

    return None


def count_vals(df: pd.DataFrame, name: str) -> None:
    """Выводит количество повторений уникальных значений.

    Выводит на экран количество повторений каждого уникального значения
    признака name датафрейма df.

    Parameters
    ----------
    df : pd.DataFrame
        Датафрейм, содержащий нужный признак.
    name : str
        Имя признака, количество повторений уникальных значения которого нужно
        посчитать.
    """
    print(f"Количество повторов уникальных значений признака {name}")

    with pd.option_context(
        "display.max_columns", None, "display.max_rows", None
    ):
        display(
            df[[name]]
            .value_counts(dropna=False)
            .reset_index()
            .rename(
                columns={
                    name: f"Значение признака {name}",
                    0: "Количество повторений",
                }
            )
        )


def plot_hbar(data: pd.DataFrame, column_name: str, **kwargs: Any) -> None:
    """Строит горизонтальную столбчатую диаграмму.

    Строит горизонтальную столбчатую диаграмму категориального признака
    column_name датафрейма data. График отрисовывается с помощью метода
    pd.DataFrame.plot(**kwargs), поэтому параметры графика можно передать,
    как именованные аргументы **kwargs.

    Parameters
    ----------
    data : pd.DataFrame
        Датафрейм, содержащий исследуемый признак.
    column_name : str
        Имя признака (столбца датафрейма data).
    **kwargs : Any, optional
        Параметры графика, корректные для метода pd.DataFrame.plot.
    """
    df: pd.Series = data[column_name].value_counts(dropna=False).sort_values()

    df.plot(kind="barh", **kwargs)
    plt.show()

    return None


def explore_cat_feature(
    data: pd.DataFrame, column_name: str, n_top: int = -1, **kwargs: Any
) -> None:
    """Выводит информацию о количестве уникальных занчений признака.

    Функция сначала печатает количество уникальных значений признака, затем,
    поочередно вызывает функции count_vals() и plot_hbar() и передаёт
    им соответствующие аргумерны. Сначала, выводится таблица с количеством
    повторений каждого уникального значения признака column_name датафрейма data
    (вызов count_vals()). Затем, строится горизонтальная столбчатая диаграмма
    категориального признака column_name датафрейма data (вызов plot_hbar()),
    где график строится с помощью метода pd.DataFrame.plot(**kwargs),
    поэтому параметры графика можно передать, как именованные аргументы
    **kwargs.

    Parameters
    ----------
    data : pd.DataFrame
        Датафрейм, содержащий исследуемый признак.
    column_name : str
        Имя признака (столбца датафрейма data).
    n_top : int
        n наиболее часто встречающихся значений, которые надо вывести. Если
        меньше 1, то выводит все. Значение по умолчанию -1.
    **kwargs : Any, optional
        Параметры графика, корректные для метода pd.DataFrame.plot.
    """
    print(f"Количество уникальных знаний: {data[column_name].nunique()}")

    most_common: List = data.loc[:, column_name].unique().tolist()
    if n_top > 0:
        most_common = (
            data.loc[:, column_name].value_counts().head(n_top).index.to_list()
        )

    selected_data: pd.DataFrame = data.loc[
        data[column_name].isin(most_common), :
    ]

    count_vals(selected_data, column_name)
    print()
    plot_hbar(selected_data, column_name, **kwargs)

    return None


def plot_num_feature_distibs(
    data: pd.DataFrame, column_name: str, bins: int = 23
) -> None:
    """Выводит графики, характеризующие распределение значений признака.

    Выводит на экран гистограмму с KDE, диаграмму размаха и ECDF для признака
    (столбца) с именем column_name из датафрема data.

    Parameters
    ----------
    data : pd.DataFrame
        Датафрейм, содержащий исследуемый признак.
    column_name : str
        Имя признака (столбца датафрейма data).
    bins: int
        Количество корзин на гистограмме. Значение по умолчанию 23.
    """
    fig, ax = plt.subplot_mosaic(
        [["hist", "ecdf"], ["box", "ecdf"]],
        figsize=(12, 6),
        gridspec_kw=dict(width_ratios=[2, 1], height_ratios=[2, 1]),
    )

    sns.histplot(
        data=data,
        x=column_name,
        ax=ax["hist"],
        stat="density",
        kde=True,
        bins=bins,
    )
    sns.ecdfplot(data=data, x=column_name, ax=ax["ecdf"], stat="proportion")
    sns.boxplot(data=data, x=column_name, ax=ax["box"])

    plt.suptitle(f"Распределение значений признака {column_name}")

    ax["hist"].set_title("Гистограмма и KDE")
    ax["hist"].set_ylabel("Плотность вероятноти")
    ax["hist"].set_xlabel("")

    ax["ecdf"].set_title("ECDF")
    ax["ecdf"].set_ylabel("Доля значений")
    ax["ecdf"].tick_params(axis="x", rotation=45)

    for axes in ax:
        ax[axes].grid()

    plt.tight_layout()

    plt.show()

    return None


def explore_num_feature(
    data: pd.DataFrame, column_name: str, bins: int = 23
) -> None:
    """Выводит информацию о распределении значений количественного признака.

    Выводит информацию о распределении значений количественного признака
    column_name датафрейма data. Сначала выводит на экран информацию о
    количестве пропусков, затем, выводит описательные статистики, затем выводит
    графики распределения значений с помощью функции plot_num_feature_distibs():
    выводит на экран гистограмму с KDE, диаграмму размаха и ECDF.

    Parameters
    ----------
    data : pd.DataFrame
        Датафрейм, содержащий исследуемый признак.
    column_name : str
        Имя признака (столбца датафрейма data).
    bins: int
        Количество корзин на гистограмме. Значение по умолчанию 23.
    """
    print(f"Признак {column_name}")
    na_counts: int = data[column_name].isna().sum()

    print(f"Количество пропусков: {na_counts}")
    print()

    print("Описательные статистики:")
    display(
        data[[column_name]].describe(percentiles=[0.1, 0.25, 0.5, 0.75, 0.9])
    )

    plot_num_feature_distibs(data, column_name, bins)

    return None


def cat_vs_cat_scatter(
    data: pd.DataFrame,
    x: str,
    y: str,
    jitter: float = 0.5,
    **kwargs: Any,
) -> None:
    """Выводит scatterplot с точками для каждого сочетания признаков x и y.

    Выводит scatterplot, в котором каждая точка соответствует сочетанию значений
    признаков x и y, цвет точки указывает на количество повторений каждого
    сочетания. Точки случайно разбросаны вокруг центра, соответствующего
    сочетанию значений x и y, "количество" случайной величины регулирует
    параметр jitter. Параметры графика по умолчанию, например cmap и alpha
    можно переопределить, а также добавить новые, передав их по имени
    (в **kwargs).

    Параметры графика по умолчанию:
    xlabel=x
    ylabel=y
    c="Количество"
    cmap="winter"
    alpha=0.4
    grid=True
    rot=-90

    Parameters
    ----------
    data : pd.DataFrame
        Датафрейм, содержащий исследуемые признаки.
    x : str
        Категориальный признак, уникальные значения которого будут отложены по
        горизонтальной оси.
    y : str
        Категориальный признак, уникальные значения которого будут отложены по
        вертикальной оси.
    jitter : float, optional
        "Количество" случайной составляющей, которая разбрасывает точки на
        графике вокруг точки пересечения их категорий, чтобы те не слипались в
        одну. Значение по умолчанию 0.5.
    **kwargs :  Any, optional
        Параметры графика, корректные для метода
        pd.DataFrame.plot(kind="scatter"). Позволяет переопределить аналогичные
        параметры, заданные по умолчанию.
    """
    plotparams: Dict[str, Any] = dict(
        xlabel=x,
        ylabel=y,
        c="Количество",
        cmap="winter",
        alpha=0.4,
        grid=True,
        rot=-90,
    )
    plotparams.update(**kwargs)

    x_cats: List[str] = sorted(data[x].unique().tolist())
    y_cats: List[str] = sorted(data[y].unique().tolist())

    add_jitter: Callable[[pd.Series], pd.Series] = lambda x: (
        x + np.random.uniform(0, jitter, size=x.shape) - jitter / 2
    )

    x_ids: Dict[str, int] = {cat: i for i, cat in enumerate(x_cats)}
    y_ids: Dict[str, int] = {cat: i for i, cat in enumerate(y_cats)}

    df: pd.DataFrame = data[[x, y]].copy()
    df["x_vals"] = add_jitter(df[x].replace(x_ids))
    df["y_vals"] = add_jitter(df[y].replace(y_ids))
    df["Количество"] = df.groupby([x, y]).x_vals.transform("count")

    df.plot(kind="scatter", x="x_vals", y="y_vals", **plotparams)

    plt.xticks(list(x_ids.values()))
    plt.gca().set_xticklabels(x_ids.keys())

    plt.yticks(list(y_ids.values()))
    plt.gca().set_yticklabels(y_ids.keys())

    plt.show()

    return None


def explore_cat_vs_cat(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    **kwargs: Any,
) -> None:
    """Выводит информацию о количестве сочетаний признаков x и y.

    Сначала печатает строку, переданную в параметр title. Затем, выводит
    сводную таблице с количеством повторений каждого уникального сочетания
    параметро в x и y датафрейма data с помощью pd.crosstab(data[x], data[y]).
    Затем выводит график (scatterplot), иллюстрирующий данные выведенной
    таблицы с помощью функции cat_vs_cat_scatter().

    Для того, чтобы переопределить параметры графика по умолчанию можно передать
    дополнительный аргументы по имени (в **kwargs).

    Parameters
    ----------
    data : pd.DataFrame
        Датафрейм, содержащий исследуемые признаки.
    x : str
        Категориальный признак, уникальные значения которого будут отложены по
        горизонтальной оси.
    y : str
        Категориальный признак, уникальные значения которого будут отложены по
        вертикальной оси.
    title : str
        Строка с описанием содержимого сводной таблицы и заголовок графика.
    **kwargs :  Any, optional
        Параметры графика, корректные для функции cat_vs_cat_scatter().
        Позволяет переопределить аналогичные параметры, заданные по умолчанию.
        Если в **kwargs передать аргумент cmap, то тепловая карта будет
        применена как к цвету текста сводной таблицы, так и к графику после
        неё.
        Если в **kwargs передать аргумент norm, то соответствующая нормализация
        цветов будет применена как к цвету текста сводной таблицы, так и к
        графику после неё. См. matplotlib.colors.LogNorm . Таким образом, текст
        сводной таблицы будет иметь те же цвета, что и элементы графика.
    """
    plot_params: Dict[str, Any] = {
        "title": title,
        "cmap": "winter",
    }
    plot_params.update(**kwargs)

    print(plot_params["title"])

    crosstab: pd.DataFrame = pd.crosstab(data[x], data[y])

    gmap: Union[None, np.ndarray] = None
    if plot_params.get("norm") is not None:
        gmap = plot_params["norm"](crosstab)

    display(
        crosstab.style.text_gradient(
            cmap=plot_params["cmap"],
            axis=None,
            gmap=gmap,
        )
    )

    print()

    cat_vs_cat_scatter(
        data,
        x=x,
        y=y,
        **plot_params,
    )

    return None


def num_vs_cat_boxplots(
    data: pd.DataFrame,
    cat_feature: str,
    num_feature: str,
    **kwargs: Any,
) -> None:
    """Строит диаграммы размаха признака num_feature в разрезе cat_feature.

    Строит диаграммы размаха признака num_feature в разрезе cat_feature и
    формирует заголовок вида "Диаграммы размаха признака {num_feature} в разрезе
    признака {cat_feature} . В функцию можно передать параметры графика,
    корректные для метода pd.DataFrame.boxplot() с помощью именованных
    аргументов **kwargs.

    Параметры графика можно переопределить передав именнованные параметры,
    корректные для метода pd.DataFrame.boxplot() через **kwargs.

    Parameters
    ----------
    data : pd.DataFrame
        Датафрейм, содержащий исследуемый признак.
    cat_feature : str
        Имя категориального признака в разрезе которого будут построены
        диаграммы размаха количественного признака.
    num_feature : str
        Имя количественного признака, для которого будут построены диаграммы
        размаха.
    **kwargs : Any, optional
        Параметры графика, корректные для метода pd.DataFrame.boxplot().
    """
    data.boxplot(
        column=num_feature,
        by=cat_feature,
        **kwargs,
    )

    plt.title(
        f"Диаграммы размаха признака {num_feature} в разрезе "
        f"признака {cat_feature}"
    )

    plt.suptitle("")

    return None


def num_vs_num_scatterhexbin(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    xlabel: str,
    ylabel: str,
    scatter_alpha: float = 0.1,
    scatter_s: Union[int, None] = None,
    hexbin_gridsize: int = 100,
    figsize: Tuple[int, int] = (18, 6),
) -> None:
    """Строит график, характеризующий взаимосвязь двух количественных признаков.

    Выводит на экран два графика, характеризующих взаимосвязь двух
    количественных признаков: диаграмму рассеяния
    (pd.DataFrame.plot(kind="scatter")) и hexbin-plot (plt.hexbin()) с тепловой
    картой, характерезующий количество наблюдений в каждой корзине. На каждом
    график по горизонтальной оси отложены значения признака x датафрейма data,
    по вертикальной оси - значения признака у датафрейма data.

    Parameters
    ----------
    data : pd.DataFrame
        Датафрейм, содержащий исследуемые признаки.
    x : str
        Имя признака (название столбца data), который будет отложен по оси X.
    y : str
        Имя признака (название столбца data), который будет отложен по оси Y.
    title : str
        Заголовок графика (suptitle).
    xlabel : str
        Название оси X.
    ylabel : str
        Название оси y.
    scatter_alpha : float, optional
        Прозрачность точек на диаграмме рассеяния. Аналогичен аргументу alpha
        метода pd.DataFrame.plot.scatter(). Значение по умолчанию 0.1.
    scatter_s : Union[int, None], optional
        Размер точек на диаграмме рассеяния.Аналогичен аргументу s
        метода pd.DataFrame.plot.scatter(). Значение по умолчанию None.
    hexbin_gridsize : int, optional
        Размер шестиугольника на hexbin, соответствует аргументу gridsize
        метода plt.hexbin(). Значение по умолчанию 100.
    figsize : Tuple[int, int], optional
        Размер всего графика с двумя подграфиками. Значение по умолчанию
        (18, 6).
    """
    fig, (ax0, ax1) = plt.subplots(
        ncols=2, figsize=figsize, gridspec_kw={"width_ratios": [3, 4]}
    )

    fig.suptitle(title)

    data.plot(
        kind="scatter",
        x=x,
        y=y,
        xlabel=xlabel,
        ylabel=ylabel,
        title="Диаграмма рассеяния",
        alpha=scatter_alpha,
        s=scatter_s,
        grid=True,
        ax=ax0,
    )

    hb = ax1.hexbin(
        data[x], data[y], gridsize=hexbin_gridsize, cmap="Blues", mincnt=1
    )
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.set_title("Hexbin-plot")
    fig.colorbar(hb, ax=ax1, label="Количество")

    plt.show()

    return


def plot_corr_matrix(
    data: pd.DataFrame,
    columns: Union[List[str], None] = None,
    method: Literal["pearson", "kendall", "spearman"] = "pearson",
    numeric_only: bool = True,
    annot: bool = True,
    figsize: Tuple[int, int] = (7, 7),
    vmin: float = -1,
    vmax: float = 1,
    rot: int = 0,
) -> None:
    """Выводит матрицу корреляции. Игнорирует пустые значения (NA/null).

    Parameters
    ----------
    data : pd.DataFrame
        Датафрейм с данными, для которых будут расчитаны коэффициенты
        корреляции.
    columns : Union[List[str], None], optional
        Столбцы датафрейма data, для которых будет построена матрица корреляции,
        если None, то матрица корреляции будет построена для всех столбцов с
        числовыми типами. Значение по умолчанию None.
    method : {"pearson", "kendall", "spearman"}, optional
        Метод по которому будут расчитываться коэффициенты корреляции. Допустимы
        следующие значения:
        "pearson" - коэффициент корреляции Пирсона,
        "kendall" - коэффициент корреляции Кендалла,
        "spearman" - коэффициент ранговой корреляции Спирмена.
        Значение по умолчанию "pearson".
    numeric_only : bool, optional
        Если True корреляция вычисляется только для количественных и логических
        значений. Соответствует параметру numeric_only метода
        pd.DataFrame.corr(). Значение по умолчанию True.
    annot : bool, optional
        Если True, то в матрице корреляции для каждой пары признаков будут
        указаны значения коэффициента корреляции. Значение по умолчанию True.
    figsize : Tuple[int, int], optional
        Размер графика, значение по умолчанию (7, 7)
    vmin : float, optional
        Минимальное значение коэффициента корреляции, имеющее собственный цевет
        на тепловой карте. Значение по умолчанию -1. Соответствует параметру
        vmin функции sns.heatmap()
    vmax : float, optional
        Максимальное значение коэффициента корреляции, имеющее собственный цевет
        на тепловой карте. Значение по умолчанию 1. Соответствует параметру
        vmax функции sns.heatmap()
    rot : int, optional
        Угол на который повёрныты подписи значений осей.
        Значение по умолчанию 0.
    """
    cols: List[str] = data.columns.tolist()
    if columns is not None:
        cols = columns

    corr: pd.DataFrame = data[cols].corr(
        method=method, numeric_only=numeric_only
    )

    mask: np.ndarray = np.triu(np.ones_like(corr, dtype=bool))

    f, ax = plt.subplots(figsize=figsize)

    cmap: LinearSegmentedColormap = sns.diverging_palette(230, 20, as_cmap=True)

    ax = sns.heatmap(
        corr,
        mask=mask,
        cmap=cmap,
        annot=annot,
        vmax=vmax,
        vmin=vmin,
        center=0,
        square=True,
        linewidths=1,
        cbar_kws=dict(shrink=0.5),
        ax=ax,
    )

    ax.set_title("Матрица корреляции")

    ax.set_yticklabels(ax.get_yticklabels(), rotation=rot)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90 - rot)

    plt.show()

    return None
