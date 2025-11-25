import plotly.express as px
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html
from load_data import load_olympics_data, remove_team_duplicated_medals
import numpy as np

# Page: main title, logo path, and page name
TITLE = "Olympiska spelen Analys - Team Australien"
OS_LOGO = "assets/olympic-logo.svg"
PAGE_TITLE = "Ridning"

# Register this file as a Dash page (title, URL, menu order)

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/equestrian", order=7)


df = load_olympics_data()
df = remove_team_duplicated_medals(df, "Equestrianism")
sport_equestrianism = df[df["Sport"] == "Equestrianism"]  

# prepare equestrianism data. Group, filter, pivot and melt
def prepare_equestrianism_data(selected_medal="ALL", selected_years=None):
    """Prepare equestrian-data"""

    # only rows with medals
    sport_equestrianism_medals = sport_equestrianism[sport_equestrianism["Medal"].notna()]
    
    # When specific years are choosen, filter dataset to only show them
    if selected_years:
        sport_equestrianism_medals = sport_equestrianism_medals[sport_equestrianism_medals["Year"].isin(selected_years)]
    
    # sort medals per YEAR, NOC and type
    medals_sorted_per_year = (sport_equestrianism_medals.groupby(["Year", "NOC", "Medal"])
                            .size()
                            .reset_index(name="Count"))

    #pivot to wide format - one medal type per column
    medals_all_years = medals_sorted_per_year.pivot_table(
        values="Count",
        index=["Year", "NOC"],
        columns="Medal",
        fill_value=0
    ).reset_index()
 
    # Remove the column name from the header
    medals_all_years.columns.name = None

    #total medal for all countries all years
    medals_all_years["Total"] = (
        medals_all_years["Gold"]
        + medals_all_years["Silver"]
        + medals_all_years["Bronze"]
    )

    #remove float. Needed for dropdown.
    medals_all_years["Year"] = medals_all_years["Year"].astype(int)
 
 
    # convert from wide to long format
    sorted_medals_melt = pd.melt(
        medals_all_years,
        id_vars=["Year", "NOC"],
        value_vars=["Gold", "Silver", "Bronze"],
        var_name="Medaltype",
        value_name="Amount"
    )

    # Filter the data to show only the selected medal type
    if selected_medal != "ALL":
        sorted_medals_melt = sorted_medals_melt[sorted_medals_melt["Medaltype"] == selected_medal]
   
    return sorted_medals_melt

#sorted medals per year for dropdown
years_sorted = sorted(sport_equestrianism["Year"].dropna().unique().astype(int))

#dashcard summmary stats
first_year = np.min(sport_equestrianism["Year"].unique())
mean_age = np.mean(sport_equestrianism["Age"].dropna())
gender_counts = sport_equestrianism["Sex"].value_counts()

def layout():

    sorted_medals_melt = prepare_equestrianism_data()


    fig_medals_equestrian = px.bar(
        sorted_medals_melt,
        x= "NOC",
        y="Amount",
        color= "Medaltype",
        color_discrete_map={
            "Gold":"#9F8F5E",
            "Silver": "#969696",
            "Bronze": "#996B4F"
            },
        labels={"value": "Medals total", "NOC":"Region", "Medaltype":"Medals type"},
        barmode="stack"
    )
    
    # delar av kod nedan utvecklad med hjälp av Claude (Anthropic, 2025). Konversation: 16 november 2025:
    # frågan var hur jag kunde få tydligare graf.

    fig_medals_equestrian.update_layout(                               
        xaxis_tickangle=-45,                         #vrider NOC text så den är lättare att läsa
        height=600,                                  # höjd på  grafen
        xaxis={'categoryorder': 'total descending'}  # Sorterar inom staplarna inom varje år från mest till minst
    )
    fig_medals_equestrian.update_traces(
        hovertemplate="<b>%{x}</b><br>Medalj: %{customdata[1]}<br>År: %{customdata[0]}<br>Antal: %{y}<extra></extra>"
    )

    return [
        html.H3("Ridning", className="mb-3"),
        html.P(
            """En analys av ridning i Olympiska spelen. Denna sida ger en sammanfattning av viktig statistik och
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
                                   str(f"{first_year:.0f}"),
                                   className="card-title",
                               ),
                               html.H6(
                                   "Första året i OS",
                                   className="card-subtitle",
                               ),
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
                                html.H4(str(f"{mean_age:.1f}"),
                                    className="card-title",
                                ),
                                html.H6("medelålder", className="card-subtitle"),
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
                                html.H4(str(f"Kvinnor: {gender_counts.get('F', 0)} | Män: {gender_counts.get('M', 0)}"),
                                    className="card-title",
                                ),
                                html.H6("Könsfördelning", className="card-subtitle"),
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
                                html.H4("Medaljfördelning för ridsport i OS"),
                                html.P("Medaljer fördelat på land historiskt. Sortera på önskad medaljtyp nedan."),
                                html.H4("", className="card-title"),
                                dbc.Label("Välj"),
                                    dcc.Dropdown(
                                        id="Medal_filter",
                                        options=[
                                            {"label": "Alla medaljer", "value": "ALL"},
                                            {"label": "Guld", "value": "Gold"},
                                            {"label": "Silver", "value": "Silver"},
                                            {"label": "Brons", "value": "Bronze"},
                                            ],
                                        value= "ALL",
                                        clearable= False
                                    ),
                                    dcc.Dropdown(
                                        id="Year_filter",
                                        options=[{"label": str(year), "value": int(year)} for year in years_sorted],
                                        value=[],
                                        placeholder="Välj år",
                                        multi=True,
                                        clearable=True,
                                    ),
                                dcc.Graph(id="id_first_graph", figure=fig_medals_equestrian),
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
@callback(
    Output("id_first_graph", "figure"),
    Input("Medal_filter", "value"),
    Input("Year_filter", "value"),
)
 
def update_medal_figure(selected_medal, selected_years):
    sorted_medals_melt = prepare_equestrianism_data(selected_medal=selected_medal,
                                                     selected_years=selected_years)
 
    updated_fig = px.bar(
        sorted_medals_melt,
        x="NOC",
        y="Amount",
        color="Medaltype",
        color_discrete_map={"Gold": "#9F8F5E", "Silver": "#969696", "Bronze": "#996B4F"},
        barmode="stack",
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
 
