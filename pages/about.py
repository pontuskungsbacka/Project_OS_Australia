import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html

TITLE = "Olympiska spelen Analys - Team Australien"
OS_LOGO = "assets/olympic-logo.svg"
PAGE_TITLE = "Om oss"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/about", order=8)

def layout():
    return [
        html.H3("Om projektet & skaparna", className="mb-3"),
        html.P(
           """Detta projekt är en del av en grupp uppgift i Databehandling kursen 
        """
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(
                                    "Adam Hedlund",
                                    className="card-title",
                                ),
                                html.P(
                                    [
            "Kontakta via ",
            html.A("LinkedIn", href="Länk till Adam LinkedIn eller portfolio"),
            html.A("GitHub", href="Länk till Adam GitHub"), ]
                                ),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    md=3,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(
                                    "Julia Sälde",
                                    className="card-title",
                                ),
                                html.P(
                                    [
            "Kontakta via ",
            html.A("LinkedIn", href="Länk till Adam LinkedIn eller portfolio"),
            html.A("GitHub", href="Länk till Adam GitHub"), ]
                                ),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    md=3,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Laura-Mirella Lomakin", className="card-title"),
                                html.P(
                                    [
            "Kontakta via ",
            html.A("LinkedIn", href="Länk till Adam LinkedIn eller portfolio"),
            html.A("GitHub", href="Länk till Adam GitHub"), ]
                                ),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    md=3,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Pontus Johansson", className="card-title"),
                                html.P(
                                    [
                                        "Kontakta via ",
                                        html.A("LinkedIn", href="Länk till Adam LinkedIn eller portfolio"),
                                        html.A("GitHub", href="Länk till Adam GitHub"), ]
                                ),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    md=3,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Github Repository"),
                                html.P(
                                    [
                                        "Här hittar ni Github Repo för detta grupparbetet ",
                                        html.A("Github", href="https://github.com/pontuskungsbacka/Project_OS_Australia"),
                                        ".",
                                    ]
                                ),
                            
                                html.H5("Dataset"),
                                html.P(
                                    [
                                        "Datasetet som använde i projektet är hämtat från Kaggle. Datasetet är skapat av rgriffin och kan hittas här: ",
                                        html.A("Kaggle", href="https://www.kaggle.com/code/heesoo37/olympic-history-data-a-thorough-analysis"),
                                        ".",
                                    ]
                                ),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    width=12,
                ),
            ],
            class_name="g-3",
        ),
    ]