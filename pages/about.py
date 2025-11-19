import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html

TITLE = "Olympiska spelen Analys - Team Australien"
OS_LOGO = "assets/olympic-logo.svg"
PAGE_TITLE = "Om oss"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/about", order=8)


layout = [
    html.H3("Om projektet & skaparna", className="mb-3"),
    html.P(
        [
            "Den här applikationen är skapad av ",
            html.A("Adam", href="Länk till Adam LinkedIn eller portfolio"),
            html.A("Julia", href="Länk till Julia LinkedIn eller portfolio"),
            html.A("Laura", href="Länk till Laura LinkedIn eller portfolio"),
            html.A("Pontus Johansson", href="Länk till Pontus LinkedIn eller portfolio"),
        ]
    ),
    html.H5("Källförteckning: "),
    html.Ul(
        [
            html.Li(
                [
                    html.B("Michelin logo: "),
                    "Nikolaos Dimos, CC BY-SA 3.0 ",
                    html.A("via Wikimedia Commons", href="https://creativecommons.org/licenses/by-sa/3.0"),
                    ".",
                ],
            ),
            html.Li(
                [
                    html.B("Dataset: "),
                    "Jerry Ng on ",
                    html.A("Kaggle", href="https://www.kaggle.com/datasets/ngshiheng/michelin-guide-restaurants-2021"),
                    ".",
                ],
            ),
        ]
    ),
    html.H5("Code"),
    html.P(
        [
            "The code for this app is available on ",
            html.A("Github", href="https://github.com/niekvleeuwen/michelin-guide-restaurants-dashboard"),
            ".",
        ]
    ),
]