import plotly.express as px
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html
from load_data import load_olympics_data, remove_team_duplicated_medals

TITLE = "Olympiska spelen Analys - Team Australien"
OS_LOGO = "assets/olympic-logo.svg"
PAGE_TITLE = "Ridning"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/equestrian", order=7)


def prepare_equestrianism_data(selected_medal="ALL"):
    """Förbereder equestrian-data"""
    df = load_olympics_data()
    df = remove_team_duplicated_medals(df, "Equestrianism")
    sport_equestrianism = df[df["Sport"] == "Equestrianism"]  
    sport_equestrianism_medals = sport_equestrianism[sport_equestrianism["Medal"].notna()]
    medals_sorted_per_year = (sport_equestrianism_medals.groupby(["Year", "NOC", "Medal"])
                            .size()
                            .reset_index(name="Count"))

    medals_all_years = medals_sorted_per_year.pivot_table(
        values="Count",
        index=["Year", "NOC"],
        columns="Medal",
        fill_value=0
    ).reset_index()

    medals_all_years.columns.name = None
    medals_all_years["Total"] = (
        medals_all_years["Gold"]
        + medals_all_years["Silver"]
        + medals_all_years["Bronze"]
    )
    medals_all_years["Year"] = medals_all_years["Year"].astype(int)



    ##########top10_per_year = medals_all_sorted.groupby("Year").head(10)

    # convert from wide to long format
    sorted_medals_melt = pd.melt(
        medals_all_years,
        id_vars=["Year", "NOC"],
        value_vars=["Gold", "Silver", "Bronze"],
        var_name="Medaltype",
        value_name="Amount"
    )
    
    if selected_medal != "ALL":
        sorted_medals_melt = sorted_medals_melt[sorted_medals_melt["Medaltype"] == selected_medal]
    
    return sorted_medals_melt


def layout():
    sorted_medals_melt = prepare_equestrianism_data()

    fig_medals_equestrian = px.bar(
        sorted_medals_melt,
        x="NOC",
        y="Amount",
        color="Medaltype",
        color_discrete_map={"Gold":"#9F8F5E", "Silver": "#969696", "Bronze": "#996B4F"},
        title="Medals per country - Equestrianism",
        labels={"Amount":"Medals total", "NOC":"Region", "Medaltype":"Medals type"},
        barmode="group",
        hover_data=["Year", "Medaltype"]
    )
    # kod nedan utvecklad med hjälp av Claude (Anthropic, 2025). Konversation: 16 november 2025:
    #frågan var hur jag kunde få tydligare graf.


    fig_medals_equestrian.update_layout(                               
        xaxis_tickangle=-45,                         #vrider NOC text så den är lättare att läsa
        height=600,                                  # höjd på  grafen
        xaxis={'categoryorder': 'total descending'}  # Sorterar inom staplarna inom varje år från mest till minst
    )
    fig_medals_equestrian.update_traces(
        hovertemplate="<b>%{x}</b><br>Medalj: %{customdata[1]}<br>År: %{customdata[0]}<br>Antal: %{y}<extra></extra>"
    )
# allt mellan <b> och </b> visas med fetstil    #%{x} variabel för x-värdet #radbrytning
    return [# visar att ett värde ska hämtas från datan.
        html.H3("Ridning", className="mb-3"),
        html.P(
            """En analys av ridning i Olympiska spelen. Denna sida ger en sammanfattning av viktiga statistik och
        visualiseringar prestationer i ridning under de Olympiska spelen.
        """
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(
                                    "",
                                    id="first-equestrian-game",
                                    className="card-title",
                                ),
                                html.H6("Första Ridningsgren i Olympiska spelen", className="card-subtitle"),
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
                                    id="Number-of-years-equestrian",
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
                                html.H4("Filtrera på medalj", className="card-title"),
                                dbc.Label("Välj medaljtyp"),
                                dcc.Dropdown(
                                    id="Medal-filter",
                                    options=[
                                        {"label": "Alla medaljer", "value": "ALL"},
                                        {"label": "Guld", "value": "Gold"},
                                        {"label": "Silver", "value": "Silver"},
                                        {"label": "Brons", "value": "Bronze"},
                                    ],
                                    value="ALL",
                                    clearable=False
                                ),
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
                                html.H4("Medaljer i ridning per land"),
                                html.P("Text om graf."),
                                dcc.Graph(id="id-first-graph", figure=fig_medals_equestrian),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    md=12,
                    sm=12,
                ),
            ],
            class_name="g-3",
        ),
    ]


@callback(
    Output("id-first-graph", "figure"),
    Input("Medal-filter", "value")
)

def update_medal_figure(selected_medal):
    sorted_medals_melt = prepare_equestrianism_data(selected_medal)

    updated_fig = px.bar(
        sorted_medals_melt,
        x="NOC",
        y="Amount",
        color="Medaltype",
        color_discrete_map= {"Gold": "#9F8F5E", "Silver": "#969696", "Bronze": "#996B4F"},
        title= "Medals per country - Equestrianism",
        barmode= "group",
        hover_data=["Year", "Medaltype"]
    )
    updated_fig.update_layout(
        xaxis_tickangle=-45,
        height=600,
        xaxis={'categoryorder': 'total descending'}
    )
    updated_fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Medalj: %{customdata[1]}<br>År: %{customdata[0]}<br>Antal: %{y}<extra></extra>"
    )

    return updated_fig