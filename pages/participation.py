import plotly.express as px
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html
from load_data import load_olympics_data

TITLE = "Olympiska spelen Analys - Team Australien"
OS_LOGO = "assets/olympic-logo.svg"
PAGE_TITLE = "Översikt analys"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/", order=0)


def layout():
    df = load_olympics_data()
    #merge "AUS" and "ANZ" to get both NOC:S
    australia = df[df["NOC"].isin(["AUS", "ANZ"])]   

    participation_historical_aus = (
        australia.groupby(["Year", "Season"])["ID"]
        .nunique()
        .reset_index(name="Participants") 
    )#. groupby() turns year to index
                                                                                                                      #  .nunique() content in y-axle

    fig_aus_overview= px.line(
        participation_historical_aus,
        x= "Year", 
        y= "Participants",
        color="Season",
        markers=True,
        title= "Australia participation 1896–2016"
    )

    fig_aus_overview.update_yaxes(
        type="log",
        title_text="Participants (log scale)"
    )                   #Clearer curve. Shows growth instead of absolute counts.

    return [
        html.H3("Översikt analys", className="mb-3"),
        html.P(
            """En översikt över Olympiska spelen med fokus på Team Australien. Denna sida ger en sammanfattning av
        viktiga statistik och visualiseringar relaterade till Australiens prestationer i de Olympiska spelen.
        """
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(
                                    "-",
                                    id="number-of-olympic-games",
                                    className="card-title",
                                ),
                                html.H6("Antal olympiska spel", className="card-subtitle"),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    md=4,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(
                                    "-",
                                    id="Number-of-medals",
                                    className="card-title",
                                ),
                                html.H6("Antalet medaljer", className="card-subtitle"),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    md=4,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("-", id="total-athlets", className="card-title"),
                                html.H6("Totalt althleter", className="card-subtitle"),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    md=4,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Första grafen kommer här"),
                                html.P("Text om graf."),
                                dcc.Graph(id="id-first-graph", figure=fig_aus_overview),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    md=6,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Andra grafen kommer här"),
                                html.P("""
                                    Text om graf. längre text för att se hur det ser ut nör det är mer text
                            """),
                                dcc.Graph(id="id-second-graph"),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    md=6,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Tredje grafen kommer här"),
                                html.P("Text om graf."),
                                dcc.Graph(id="id-third-graph"),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    md=6,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Fjärde grafen kommer här"),
                                html.P(
                                    """Text om graf. Längre text för att se hur det ser ut när det är mer text."""
                                ),
                                dcc.Graph(id="id-fourth-graph")
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    md=6,
                    sm=12,
                ),
            ],
            class_name="g-3",
        ),
    ]