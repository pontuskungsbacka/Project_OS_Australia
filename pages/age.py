import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html
import plotly_express as px 
from load_data import load_olympics_data

df = load_olympics_data()
#Import stuff move later
TITLE = "Olympiska spelen Analys - Team Australien"
OS_LOGO = "assets/olympic-logo.svg"
PAGE_TITLE = "Åldersanalys"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/age", order=2)


def layout():
    australia_rows = df[(df['NOC'] == 'AUS') | (df['NOC'] == 'ANZ')]
    australia_rows_uniqueID = australia_rows.drop_duplicates(subset=['ID'])

    fig_hist1 = px.histogram(   
        australia_rows_uniqueID, 
        x='Age', 
        nbins=50 
    )

    return [
        html.H3("Åldersanalys för Australien", className="mb-3"),
        html.P(
            """Åldrar hos australiensiska atleter i de Olympiska spelen. Denna sida ger en sammanfattning av
        viktiga statistik så som yngsta och älsta deltagare historiskt och medelåldern. Se även visualiseringar relaterade till åldersfördelningen bland Australiens prestationer i de Olympiska spelen.
        """
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(
                                    "13 år",
                                    id="youngest-athlete",
                                    className="card-title",
                                ),
                                html.H6("Yngsta deltagare - detta var idrottare i simning och rodd under 60- och 70-talet.", className="card-subtitle"),
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
                                    "25 år",
                                    id="average-athlete",
                                    className="card-title",
                                ),
                                html.H6("Genomsnittlig idrottare ålder", className="card-subtitle"),
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
                                html.H4("62 år", id="oldest-athlete", className="card-title"),
                                html.H6("Den äldsta deltagaren från Australien tävlade i konst år 1932.", className="card-subtitle"),
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
                                html.H4("Histogram över åldrar"),
                                html.P("Fördelningen av åldrarna på alla de som tävlat för Australien i OS. Det är allra flest 23-åringar"),
                                dcc.Graph(id="australia-age-histogram", figure=fig_hist1),
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
                                dcc.Graph(id="id-fourth-graph"),
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