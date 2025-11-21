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


def layout():
    
    #histogram plot
    rowing_rows = df[df['Sport']=='Rowing']
    rowing_rows_uniqueID = rowing_rows.drop_duplicates(subset=['ID'])

    fig_hist2 = px.histogram(
        rowing_rows_uniqueID, 
        x='Age', 
        nbins=50
    )

    #correlation plot
    corr_columns = rowing_rows[["Weight", "Height", "Medal"]]
    corr_columns["Medal"].fillna(0, inplace=True) #ingen medalj blir 0
    # alla medaljer blir 1
    corr_columns["Medal"].mask(corr_columns["Medal"].isin(["Bronze", "Silver", "Gold"]) , other=1, inplace=True)
    # innan vi tar bort rader med saknad height elr weight rader har vi 10595 rows, sen 7794
    corr_columns.dropna(axis=0, how='any', subset=['Weight', 'Height'], inplace=True)

    corr_table = corr_columns.corr(method="pearson") # create a correlation table with pandas

    # set up the correlation plot
    fig_corr= px.imshow(
        # pass the correlation matrix,
        corr_table,
        #show the correlation values in each cell,
        text_auto=True, 
        # set the colour scale
        color_continuous_scale="RdYlGn",
        zmin=-1,
        zmax=1
    )

    return [
        html.H3("Rodd - alla länder", className="mb-3"),
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
                                html.H4(
                                    "År 1900",
                                    id="first-rowing-game",
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
                                html.H4(
                                    "1,3 OS",
                                    id="average-years-rowing",
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
                                html.H4(
                                    "8 OS", 
                                    id="max-number-of-years-rowing",
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