import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html
import plotly.express as px
from load_data import load_olympics_data, remove_team_duplicated_medals

TITLE = "Olympiska spelen Analys - Team Australien"
OS_LOGO = "assets/olympic-logo.svg"
PAGE_TITLE = "Landhockey"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/hockey", order=6)

df = load_olympics_data() #Laddar en csv med os athlete i en df
df = remove_team_duplicated_medals(df,"hockey")
hockey_unique = remove_team_duplicated_medals(df, "hockey")
aus_hockey = hockey_unique[hockey_unique["NOC"] == "AUS"]

aus_long = (
    aus_hockey
    .groupby(["Year", "Sex", "Medal"])
    .size()
    .reset_index(name="Count")
)


def layout():
    hockey = df[df["Sport"] == "Hockey"]
    hockey = hockey[hockey["Medal"].notna()]
    medals = (hockey.groupby(["NOC", "Medal"])
        .size().unstack(fill_value=0)) # Räknar de olika medaljerna och fyller med 0 där det saknas

    medals["Total"] = (medals["Gold"] + medals["Silver"] + medals["Bronze"]) # Räknar ihop totala antal medaljer
    top10 = medals.sort_values(by="Total", ascending=False).head(10).reset_index()

    medal_values = ["Bronze", "Silver", "Gold"]

    fig_hockey_medals = px.bar(
        top10, x=medal_values, y="NOC",
        barmode="stack",
        color_discrete_map={"Gold":"#FFD700", "Silver": "#C0C0C0", "Bronze": "#CD7F32"}, #Uppdatera färgval så vi alla har samma!
        title="Top 10 länder i landhockey",
        labels={
            "NOC": "Land",
            "value": "Antal medaljer",
            "variable": "Valör",
        },
    )

    
    return [
        html.H3("Landhockey", className="mb-3"),
        html.P(
           """En analys av landhockey i Olympiska spelen. Denna sida ger en sammanfattning av viktiga statistik och
        visualiseringar prestationer i landhockey under de Olympiska spelen.
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
                                    id="first-hockey-game",
                                    className="card-title",
                                ),
                                html.H6("Första Landhockeygren i Olympiska spelen", className="card-subtitle"),
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
                                    id="Number-of-years-hockey",
                                    className="card-title",
                                ),
                                html.H6("Antal år", className="card-subtitle"),
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
                                html.H4("-", id="total-events-hockey", className="card-title"),
                                html.H6("Antal evenemang", className="card-subtitle"),
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
                                html.H4("Toppländer landhockey - medaljer"),
                                html.P("Antal medaljer (Guld, Silver, Brons) för de 10 bästa länderna."),
                                dcc.Graph(id="id-first-graph", figure=fig_hockey_medals),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    width=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("År och kön på medaljtagarna"),
                                html.P("""
                                    Text om graf. längre text för att se hur det ser ut när det är mer text
                            """),
                                html.Label("Kön"),
                                dcc.Dropdown(
                                    id="sex-dropdown-hockey",
                                    options=[
                                        {"label": "Båda", "value": "both"},
                                        {"label": "Herr", "value": "M"},
                                        {"label": "Dam", "value": "F"},
                                    ],
                                    value="both",
                                    clearable=False,
                                    style={"marginBottom": "10px"},
                                ), 
                                dcc.Graph(id="id-second-graph"),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    width=12,
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

@callback(
        Output("id-second-graph", "figure"),
        Input("sex-dropdown-hockey", "value"),
)

def update_aus_hockey_graph(selected_sex):
    dff = aus_long.copy()
    if selected_sex == "both":
        dff_plot = (dff.groupby(["Year", "Medal"])["Count"].sum().reset_index())
        title_suffix = "(Herr & Dam)"
    else:
        dff_plot = dff[dff["Sex"] == selected_sex]
        title_suffix= "(Herr)" if selected_sex == "M" else "(Dam)"

    fig = px.bar(
        dff_plot,
        x="Year",
        y="Count",
        color="Medal",
        barmode="stack",
        category_orders={"Medal": ["Bronze", "Silver", "Gold"]},
        color_discrete_map={
            "Gold": "#FFD700",
            "Silver": "#C0C0C0",
            "Bronze": "#CD7F32",
        },
        labels={
            "Year": "År",
            "Count": "Antal medaljer",
            "Medal": "Valör",
        },
        title=f"Australiens medaljer i landhockey per år{title_suffix}",
    )

    return fig