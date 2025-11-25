import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html
import plotly.express as px 
from load_data import load_olympics_data

df = load_olympics_data()
#Import stuff move later
TITLE = "Olympiska spelen Analys - Team Australien"
OS_LOGO = "assets/olympic-logo.svg"
PAGE_TITLE = "Åldersanalys"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/age", order=2)

australia_rows = df[(df['NOC'] == 'AUS') | (df['NOC'] == 'ANZ') ]
australia_rows_uniqueID = australia_rows.drop_duplicates(subset=['ID'])

def layout():
    australia_rows = df[(df['NOC'] == 'AUS') | (df['NOC'] == 'ANZ')]
    australia_rows_uniqueID = australia_rows.drop_duplicates(subset=['ID'])

    fig_hist1 = px.histogram(   
        australia_rows_uniqueID, 
        x='Age', 
        nbins=50,
        color_discrete_sequence=["#0D5257"],
    )

    return [
        html.H3("Åldersanalys för Australien", className="mb-3"),
        html.P(
            """Åldrar hos atleter från Australien i de Olympiska spelen. Denna sida ger en sammanfattning av
        viktig statistik så som yngsta och älsta deltagare historiskt och medelåldern. Se även en visualisering över åldersfördelningen bland Australiens deltagare i OS.
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
                                    id="youngest_athlete",
                                    className="card-title",
                                ),
                                html.H6("Yngsta deltagarna. Detta var idrottare i simning och rodd under 60- och 70-talet.", className="card-subtitle"),
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
                                    id="average_athlete",
                                    className="card-title",
                                ),
                                html.H6("Genomsnittlig ålder", className="card-subtitle"),
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
                                    id="oldest_athlete", 
                                    className="card-title"
                                    ),
                                html.H6("Den äldsta deltagaren från Australien tävlade i konst år 1932.", className="card-subtitle"),
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
                                html.H4("Histogram över åldrar"),
                                html.P("Fördelningen av åldrarna på alla de som tävlat för Australien i OS. Det är allra flest 23-åringar"),
                                dcc.Graph(id="australia-age-histogram", figure=fig_hist1),
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
    [
        Output("youngest_athlete", "children"),
        Output("average_athlete", "children"),
        Output("oldest_athlete", "children")
    ],
    Input("youngest_athlete", "children"),  # Trigger on page load
)

def update_summary_cards_age(_):
    
    # Calculate the youngst australian participant
    youngest_athlete_value = australia_rows['Age'].min()
    youngest_athlete = f"{youngest_athlete_value:.0f} år"

    # Calculate the age of the average australian participant
    average_athlete_value = australia_rows_uniqueID['Age'].mean()
    average_athlete = f"{average_athlete_value:.0f} år"
    
    # Calculate the age of the oldest australian participant
    oldest_athlete_value = australia_rows["Age"].max()
    oldest_athlete = f"{oldest_athlete_value:.0f} år"
    
    return youngest_athlete, average_athlete, oldest_athlete