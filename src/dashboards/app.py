"""Пробный дашборд-заглушка из примера из документации plotly. Будет заменён."""

from typing import List

from dash import Dash, Input, Output, dcc, html
from plotly import express as px

app = Dash(__name__)


app.layout = html.Div(
    [
        html.H1("Interactive scatter plot with Iris dataset"),
        dcc.Graph(id="scatter-plot"),
        html.P("Filter by petal width:"),
        dcc.RangeSlider(
            id="range-slider",
            min=0,
            max=2.5,
            step=0.1,
            marks={0: "0", 2.5: "2.5"},
            value=[0.5, 2],
        ),
    ]
)


@app.callback(
    Output("scatter-plot", "figure"),
    Input("range-slider", "value"),
)
def update_scatter_plot(slider_range: List[float]) -> px.scatter:
    """Возвращает диаграмму рассеяния.

    Возвращает диаграмму рассеяния, диапазон значений petal_width выставляется
    с помощью слайдера под диаграммой.

    Parameters
    ----------
    slider_range : List[float]
        Диапазон значений petal_width, выставленный с помощью слайдера.

    Returns
    -------
    px.scatter
        Диаграмма рассеяния.
    """
    df = px.data.iris()

    low, high = slider_range
    mask = (df["petal_width"] > low) & (df["petal_width"] < high)

    fig = px.scatter(
        df[mask],
        x="sepal_width",
        y="sepal_length",
        color="species",
        size="petal_length",
        hover_data=["petal_width"],
    )

    return fig


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port="8050",
    )
