import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html
from pathlib import Path
import plotly.express as px

#Import stuff move later
TITLE = "Olympiska spelen Analys - Team Australien"
OS_LOGO = "assets/olympic-logo.svg"
PAGE_TITLE = "Åldersanalys"

# Load data
directory_data = Path("./data")

athletes = pd.read_csv(f"{directory_data}/athlete_events.csv")
regions = pd.read_csv(f"{directory_data}/noc_regions.csv")
merged = pd.merge(athletes, regions, on="NOC", how="outer")
df = merged

aus = df[df["NOC"].isin(["AUS", "ANZ"])]
gender_per_year = (
    aus
    .groupby(["Year", "Season", "Sex"], as_index=False)
    .size()
    .rename(columns={"size": "Count"})
)
gender_per_year["Total"] = gender_per_year.groupby(["Year", "Season"])["Count"].transform("sum")
gender_per_year["Percent"] = gender_per_year["Count"] / gender_per_year["Total"] * 100
gender_per_year["NOC"] = "AUS"

countries = ["CAN", "SWE", "GBR"]

def gender_compare(df, country):
    country_df = df[df["NOC"] == country]
    gender = (
        country_df
        .groupby(["Year", "Season", "Sex"], as_index=False)
        .size()
        .rename(columns={"size": "Count"})
    )
    gender["Total"] = gender.groupby(["Year", "Season"])["Count"].transform("sum")
    gender["Percent"] = gender["Count"] / gender["Total"] * 100
    gender["NOC"] = country
    return gender

df_gender = pd.concat([gender_compare(df, c) for c in countries], ignore_index=True)
df_gender = pd.concat([df_gender, gender_per_year], axis=0)


dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/gender", order=3)


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
                                html.H4("Gender Chart"),
                                html.P("Här är en graf som visar könsfördelning över åren för valda länder."),
                                html.Label("Välj land (NOC):"),
                                dcc.Dropdown(
                                    id="country-dropdown",
                                    options=[
                                        {"label": "Australia (AUS)", "value": "AUS"},
                                        {"label": "Canada (CAN)", "value": "CAN"},
                                        {"label": "Sweden (SWE)", "value": "SWE"},
                                        {"label": "Great Britain (GBR)", "value": "GBR"},
                                    ],
                                    value="AUS",
                                    clearable=False
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
    Input("country-dropdown", "value")
)
def update_gender_graph(selected_noc):
    dff = df_gender[df_gender["NOC"] == selected_noc]

    fig = px.bar(
        dff,
        x="Year",
        y="Percent",
        color="Sex",
        barmode="stack",
        facet_row="Season",
        width=900,
        height=500,
        hover_data={
            "Count": True,
            "Total": True,
            "Percent": ":.2f",
            "NOC": True,
        },
        title=f"Könsfördelning per år – {selected_noc}"
    )
    fig.update_layout(margin=dict(t=80, l=40, r=40, b=40))
    return fig