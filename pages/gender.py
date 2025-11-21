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
                                    id="first-women-aus",
                                    className="card-title",
                                ),
                                html.H6("Första året en kvinna från Australien deltog", className="card-subtitle"),
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
                                    id="max-percent-aus",
                                    className="card-title",
                                ),
                                html.H6("Största kvinnodeltagandet från Australien", className="card-subtitle"),
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
                                html.H4("-", id="min-percent-aus", className="card-title"),
                                html.H6("Minsta kvinnodeltagandet från Australien", className="card-subtitle"),
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
                )
            ])
    ]

@callback(
    Output("gender-graph", "figure"),
    Output("first-women-aus","children"),
    Output("max-percent-aus","children"),
    Output("min-percent-aus","children"),
    Input("gender-chart-type", "value"),
)
def update_gender_graph(chart_type):
    if chart_type == "bar":
        fig = fig_gender_bar
    else:
        fig = fig_gender_line

    first_woman_aus = int(df[(df["Sex"] == "F") & (df["Team"] == "Australia")]["Year"].min())
    best_row = compare_reset.loc[compare_reset["Australien"].idxmax()]
    worst_row = compare_reset.loc[compare_reset["Australien"].idxmin()]
    
    max_percentage_aus = f"{int(best_row["Year"])} - {best_row["Australien"]:.1f}%"
    min_percentage_aus = f"{int(worst_row["Year"])} - {worst_row["Australien"]:.1f}%"
    return fig, str(first_woman_aus), max_percentage_aus, min_percentage_aus


