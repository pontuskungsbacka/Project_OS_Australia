from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd


app = Dash(
    __name__,
    meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")],
)
app.title = 'Olympic Games - Team Australia Dashboard'
app._favicon = ("assets/favicon.ico")

app.layout = [
    html.H1(children='Olympic Games - Team Australia Dashboard', style={'textAlign':'center'})
]


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)