"""Пробный дашборд-заглушка из примера из документации plotly. Будет заменён."""

from dash import Dash, Input, Output, dcc, html
from plotly import graph_objects as go

app = Dash(__name__)


app.layout = html.Div(
    [
        html.H4("Interactive color selection with simple Dash example"),
        html.P("Select color:"),
        dcc.Dropdown(
            id="getting-started-x-dropdown",
            options=["Gold", "MediumTurquoise", "LightGreen"],
            value="Gold",
            clearable=False,
        ),
        dcc.Graph(id="getting-started-x-graph"),
    ]
)


@app.callback(
    Output("getting-started-x-graph", "figure"),
    Input("getting-started-x-dropdown", "value"),
)
def display_color(color: str) -> go.Figure:
    """Возвращает столбчатую диаграмму цвета color.

    Пробный график-заглушка из примера из документации plotly.
    В будущем будет заменен графиками из исследования.

    Parameters
    ----------
    color : str
        Цвет столбчатой диаграммы.

    Returns
    -------
    go.Figure
        Интерактивный график - объект plotly.graph_object.Figure.
    """
    fig = go.Figure(
        data=go.Bar(
            y=[2, 3, 1],
            marker_color=color,
        ),
    )

    return fig


if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port="8050",
    )
