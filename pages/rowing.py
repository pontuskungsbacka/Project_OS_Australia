import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html
import plotly.express as px
from load_data import load_olympics_data

df = load_olympics_data()

TITLE = "Olympiska spelen Analys - Team Australien"
OS_LOGO = "assets/olympic-logo.svg"
PAGE_TITLE = "Rodd"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/rowing", order=5)

# variable for first year of rowing in OS. Will be used in CARDS 
rowing_rows = df[df['Sport']=='Rowing']
first_rowing = rowing_rows['Year'].min()
first_rowing_year = str(f"{first_rowing:.0f} år") 

# also for cards - variables for average and max times athletes compete 
unique_rower_IDs = rowing_rows["ID"].unique()
years_rowing = []

for person in unique_rower_IDs:
    single_rower_years = rowing_rows[rowing_rows['ID']==person]["Year"].nunique()
    years_rowing.append(single_rower_years)

mean_years_rowing_value = sum(years_rowing) / len(years_rowing)
mean_years_rowing = f"{mean_years_rowing_value:.1f}"
max_years_rowing = max(years_rowing) 

def layout():

    rowing_rows = df[df['Sport']=='Rowing']
    rowing_rows_uniqueID = rowing_rows.drop_duplicates(subset=['ID'])

    fig_hist2 = px.histogram(
        rowing_rows_uniqueID, 
        x='Age', 
        nbins=50,
        color_discrete_sequence=["#0D5257"]
    )

    #correlation plot
    corr_columns = rowing_rows[["Weight", "Height", "Medal"]]
    corr_columns["Medal"].fillna(0, inplace=True) # 0 instead of Nan
    # put 1 instead of any meal
    corr_columns["Medal"].mask(corr_columns["Medal"].isin(["Bronze", "Silver", "Gold"]) , other=1, inplace=True)
    # removing rows missing weight or height
    corr_columns.dropna(axis=0, how='any', subset=['Weight', 'Height'], inplace=True)

    corr_table = corr_columns.corr(method="pearson")

    fig_corr= px.imshow(
        
        corr_table,
        #show the correlation values in each cell,
        text_auto=True, 
        color_continuous_scale="RdYlGn",
        zmin=-1,
        zmax=1
    )

    return [
        html.H3("Rodd", className="mb-3"),
        html.P(
           """En analys av rodd i Olympiska spelen. Denna sida ger en sammanfattning av viktig statistik och
        visualiseringar av olika aspekter av rodd i de Olympiska spelen. Rodd är bara med i sommar-OS.
        """
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4(str(first_rowing_year),
                                    className="card-title",
                                ),
                                html.H6("Första gången rodd var med i Olympiska spelen", className="card-subtitle"),
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
                                html.H4(str(mean_years_rowing),
                                    className="card-title",
                                ),
                                html.H6("Genomsnittligt antal gånger som rodd-deltagare tävlar i OS", className="card-subtitle"),
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
                                html.H4(str(max_years_rowing),
                                    className="card-title"
                                ),
                                html.H6("Högsta antalet OS som en person tävlat inom rodd", className="card-subtitle"),
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
                                html.H4("Histogram över åldrar i rodd"),
                                html.P("Grafen visar fördelningen av åldrar bland alla deltagare i rodd"),
                                dcc.Graph(id="id-first-graph", figure=fig_hist2),
                            ]
                        ),
                    ),
                    class_name="mb-3",
                    md=12,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Undersökning av korrelation mellan medaljvinst och längd och vikt"),
                                html.P("""
                                    Det finns ingen betydande korrelation mellan medaljvinst och vikt eller längd i vår OS-data. 0 betyder ingen korrelation. 1 betyder positiv korrelation, vilket betyder att om en går upp går den andra upp också. Det finns positiv korrelation mellan höjd och vikt.
                            """),
                                dcc.Graph(id="correlation-graph", figure=fig_corr),
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
    