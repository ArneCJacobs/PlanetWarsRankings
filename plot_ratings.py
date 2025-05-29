from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import pandas as pd


def main():
    # matplotlib.use("nbagg")
    df = pd.read_parquet("ratings.parquet")

    app = Dash(__name__)

    app.layout = html.Div([
        html.H4('Interactive color selection with simple Dash example'),
        html.P("Select theme:"),
        dcc.Dropdown(
            id="dropdown",
            options=list(pio.templates),
            value='Gold',
            clearable=False,
        ),
        dcc.Graph(id="graph"),
    ])


    @app.callback(
        Output("graph", "figure"),
        Input("dropdown", "value"),
    )
    def display_color(template):
        fig = px.line(
            df,
            x="timestamp",
            y="rating_mu",
            color="id",
            template=template,
        )
        return fig


    app.run(debug=True)


if __name__ == "__main__":
    main()
