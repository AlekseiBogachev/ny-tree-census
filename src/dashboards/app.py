"""Пробный дашборд-заглушка из примера из документации plotly. Будет заменён."""

import json
import urllib

from dash import Dash, Input, Output, dcc, html
from plotly import graph_objects as go

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1("Supply chain of the energy production"),
        dcc.Graph(id="graph"),
        html.P("Opacity"),
        dcc.Slider(
            id="slider",
            min=0,
            max=1,
            value=0.5,
            step=0.1,
        ),
    ]
)


@app.callback(Output("graph", "figure"), Input("slider", "value"))
def display_sankey(opacity: float) -> go.Figure:
    """Возвращает диаграмму потока (Sankey Diagram).

    Возвращает диаграмму потока (Sankey Diagram, см.
    https://plotly.com/python/sankey-diagram/). С помощью слайдера выставляется
    прозрачность линий на диаграмме. Для слайдера выставлено значение
    по умолчанию 0.5 и шаг 0.1.

    Parameters
    ----------
    opacity : float
        Значение прозрачности линий, выставляемое с мощью слайдера на дашборде.

    Returns
    -------
    go.Figure
        Диаграмма потока (Sankey Diagram).
    """
    url = "https://raw.githubusercontent.com/plotly/plotly.js/master/test/image/mocks/sankey_energy.json"
    response = urllib.request.urlopen(url)  # type: ignore
    data = json.loads(response.read())

    node = data["data"][0]["node"]
    node["color"] = [
        f"rgba(255, 0, 255, {opacity})"
        if c == "magenta"
        else c.replace("0.8", str(opacity))
        for c in node["color"]
    ]

    link = data["data"][0]["link"]
    link["color"] = [node["color"][src] for src in link["source"]]

    fig = go.Figure(go.Sankey(link=link, node=node))
    fig.update_layout(font_size=10)

    return fig


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port="8050",
    )
