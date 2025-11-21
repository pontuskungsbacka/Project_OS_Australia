import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html
from pathlib import Path
import plotly.express as px
from load_data import load_olympics_data

#Import stuff move later
TITLE = "Olympiska spelen Analys - Team Australien"
OS_LOGO = "assets/olympic-logo.svg"
PAGE_TITLE = "Åldersanalys"

df = load_olympics_data()


dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/gender", order=3)

per_country_year = df.groupby(["Year","Season", "Team"])["Sex"].value_counts().unstack()
per_country_year["Percent_women_global"] = per_country_year["F"] / (per_country_year["F"] + per_country_year["M"]) * 100
global_avg_per_year = (per_country_year.groupby(["Year", "Season"])["Percent_women_global"].mean())

df_aus = df[df["Team"] == "Australia"]
per_year_aus = df_aus.groupby(["Year", "Season"])["Sex"].value_counts().unstack(fill_value=0)
per_year_aus["Percent_women_aus"] = per_year_aus["F"] / (per_year_aus["F"] + per_year_aus["M"]) *100

compare = pd.concat([global_avg_per_year, per_year_aus["Percent_women_aus"]], axis=1)
compare_reset = compare.reset_index()
compare_reset = compare_reset.rename(columns={
    "Percent_women_global": "Globalt",
    "Percent_women_aus": "Australien"
})
fig_gender_bar = px.bar(
    compare_reset, x="Year", y=["Globalt", "Australien"],
    barmode="group",
    facet_row="Season",
    labels={
        "value": "Andel kvinnor %",
        "variable": "Kategori",
        "Year": "År",
        "Season": "Säsong",

    },
    title="Andel kvinnliga deltagare - Globalt vs Australien (stapeldiagram)"
)

fig_gender_line = px.line(
    compare_reset, x="Year", y=["Globalt", "Australien"],
    facet_row="Season",
    labels={
        "value": "Andel kvinnor %",
        "variable": "Kategori",
        "Year": "År",
        "Season": "Säsong",
    },
    title="Andel kvinnliga deltagare - Globalt vs Australien (linjediagram)"
)

def layout():
    return [
        html.H3("Genusanalys", className="mb-3"),
        html.P(
            """En analys av könsfördelning i Olympiska spelen. Denna sida ger en sammanfattning av viktiga statistik och
        visualiseringar prestationer baserat på kön under de Olympiska spelen.
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
                                    id="First-year-woman",
                                    className="card-title",
                                ),
                                html.H6("Första året kvinnor deltog", className="card-subtitle"),
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
                                    id="gender-distribution",
                                    className="card-title",
                                ),
                                html.H6("Könfördelning i Olympiskaspelen", className="card-subtitle"),
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
                                html.H4("-", id="best-gender-distribution-country", className="card-title"),
                                html.H6("Landet med bästa könsfördelningar", className="card-subtitle"),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    md=4,
                    sm=12,
                ),
               #HÄR ÄR BÖRJAN TILL GRAF !
                dbc.Col(
    dbc.Card(
        dbc.CardBody(
            [
                html.H4("Globalt vs Australien – könsfördelning"),
                html.P("Växla mellan linjediagram och stapeldiagram för andel kvinnor globalt vs Australien."),
                html.Label("Diagramtyp"),
                dcc.Dropdown(
                    id="gender-chart-type",
                    options=[
                        {"label": "Linjediagram", "value": "line"},
                        {"label": "Stapeldiagram", "value": "bar"},
                    ],
                    value="line",
                    clearable=False,
                    style={"marginBottom": "10px"},
                ),
                dcc.Graph(id="gender-graph"),
            ]
        )
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
    Output("gender-graph", "figure"),
    Input("gender-chart-type", "value"),
)
def update_gender_graph(chart_type):
    if chart_type == "bar":
        return fig_gender_bar
    else:
        return fig_gender_line

def update_cards(_):
    first_woman_aus = df[(df["Sex"] == "F") & (df["Team"] == "Australia")]["Year"].min()
    max_percentage_aus = compare.loc[compare["Australien"].idmax()]
    min_percentage_aus = compare.loc[compare["Australien"].idmin()]

    return first_woman_aus, max_percentage_aus, min_percentage_aus


