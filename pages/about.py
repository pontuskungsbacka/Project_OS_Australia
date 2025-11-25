import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html

TITLE = "Olympiska spelen Analys - Team Australien"
OS_LOGO = "assets/olympic-logo.svg"
AUS_LOGO = "assets/img/team-AUS-logo.svg"
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
                    dbc.Card([
                        dbc.CardImg(src="/assets/img/profile.svg", top=True, style={"width": "100%", "height": "auto", "fill": "#0D5257"}),
                        dbc.CardBody(
                            [
                                html.H4(
                                    "Adam Hedlund        ",
                                    className="card-title",
                                ),
                                html.A(
                                    href="https://www.linkedin.com/in/adam-hedlund-76492a88/",
                                    children=[
                                        html.Img(
                                            alt="Länk till Adam Hedlund Linkedin",
                                            src="/assets/img/linkedin-logo.svg",
                                            width=30, height=30, style={"margin-right": "10px"},
                                        ),
                                    ]
                                ),
                                html.A(
                                    href="https://github.com/Adamhedlund",
                                    children=[
                                        html.Img(
                                            alt="Länk till Adam Hedlund Github",
                                            src="/assets/img/github-mark.svg",
                                            width=30, height=30, style={"margin-right": "10px"},
                                        ),
                                    ]
                                ), 
                            ], className="mh-100", style={"height": "8rem"}
                        ),]
                    ),
                    class_name="mb-3",
                    md=3,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardImg(src="/assets/img/profile.svg", top=True, style={"width": "100%", "height": "auto", "color": "#0D5257", "fill": "#3B7F7F"}),
                        dbc.CardBody(
                            [
                                html.H4(
                                    "Julia Sälde        ",
                                    className="card-title",
                                ),
                                html.A(
                                    href="https://www.linkedin.com/in/julia-s%C3%A4lde-571129381/",
                                    children=[
                                        html.Img(
                                            alt="Länk till Julia Sälde Linkedin",
                                            src="/assets/img/linkedin-logo.svg",
                                            width=30, height=30, style={"margin-right": "10px"},
                                        ),
                                    ]
                                ),
                                html.A(
                                    href="https://github.com/JuliaMoa",
                                    children=[
                                        html.Img(
                                            alt="Länk till Julia Sälde Github",
                                            src="/assets/img/github-mark.svg",
                                            width=30, height=30, style={"margin-right": "10px"},
                                        ),
                                    ]
                                ),
                            ], className="mh-100", style={"height": "8rem"}
                        ),]
                    ),
                    class_name="mb-3",
                    md=3,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardImg(src="/assets/img/profile.svg", top=True, style={"width": "100%", "height": "auto", "color": "#0D5257", "fill": "#3B7F7F"}),
                        dbc.CardBody(
                            [
                                html.H4("Laura-Mirella Lomakin", className="card-title"),
                                html.A(
                                    href="https://www.linkedin.com/in/laura-mirella-lomakin-0258532a3/",
                                    children=[
                                        html.Img(
                                            alt="Länk till Laura-Mirella Lomakin Linkedin",
                                            src="/assets/img/linkedin-logo.svg",
                                            width=30, height=30, style={"margin-right": "10px"},
                                        ),
                                    ]
                                ),
                                html.A(
                                    href="https://github.com/lauralomakin-hub",
                                    children=[
                                        html.Img(
                                            alt="Länk till Laura-Mirella Lomakin Github",
                                            src="/assets/img/github-mark.svg",
                                            width=30, height=30, style={"margin-right": "10px"},
                                        ),
                                    ]
                                ),
                            ],className="mh-100", style={"height": "8rem"}
                        ),]
                    ),
                    class_name="mb-3",
                    md=3,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardImg(src="/assets/img/profile.svg", top=True, style={"width": "100%", "height": "auto", "color": "#0D5257", "fill": "#3B7F7F"}),
                        dbc.CardBody(
                            [
                                html.H4("Pontus Johansson", className="card-title"),
                                html.A(
                                    href="https://www.linkedin.com/in/pontuskungsbacka/",
                                    children=[
                                        html.Img(
                                            alt="Länk till Pontus Johansson Linkedin",
                                            src="/assets/img/linkedin-logo.svg",
                                            width=30, height=30, style={"margin-right": "10px"},
                                        ),
                                    ]
                                ),
                                html.A(
                                    href="https://github.com/pontuskungsbacka/",
                                    children=[
                                        html.Img(
                                            alt="Länk till Pontus Johansson Github",
                                            src="/assets/img/github-mark.svg",
                                            width=30, height=30, style={"margin-right": "10px"},
                                        ),
                                    ]
                                ),
                            ], className="mh-100", style={"height": "8rem"}
                        ),]
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
                            
                                html.H5("Dashboard layout"),
                                html.P(
                                    [
                                        "Denna dashboard har fått sina grunder från detta dashboard - michelin-guide-restaurants-dashboard. Dashboard grundmallen är skapat av Niek van Leeuwen och kan hittas här: ",
                                        html.A("Github", href="https://github.com/niekvleeuwen/michelin-guide-restaurants-dashboard"),
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