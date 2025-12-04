import plotly.express as px
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
from dash import Input, Output, callback, dcc, html
from load_data import load_olympics_data

# Page: main title, logo path, and page name
TITLE = "Olympiska spelen Analys - Team Australien"
OS_LOGO = "assets/olympic-logo.svg"
PAGE_TITLE = "Deltagande"

# Register this file as a Dash page (title, URL, menu order)
dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/participation", order=0)

#DF for the original data and filtering for Australia
df = load_olympics_data()
    #merge "AUS" and "ANZ" to get both NOC:S
australia = df[df["NOC"].isin(["AUS", "ANZ"])]   

#prepare data for historical participation graph - groupby() turns year to index
participation_historical_aus = (
        australia.groupby(["Year", "Season"])["ID"]   #X = year/Season, Y = count of unique participants
        .nunique()
        .reset_index(name="Participants")             #Turn index back to column
    )                                                

## summary statisc 1) first year participating 2) first year winter participating 3) year with most participants###
first_year_part_summer = participation_historical_aus[participation_historical_aus["Season"]=="Summer"]["Year"].unique().min()
first_winter_year_part = participation_historical_aus[participation_historical_aus["Season"]=="Winter"]["Year"].unique().min()
most_participants_year = participation_historical_aus.loc[participation_historical_aus["Participants"].idxmax()]["Year"]

# Layout of the page
def layout():
    """
    The layout function builds the entire 'Participation' page.
    It returns all Dash components (titles, cards, and the graph.
    """
     #  .nunique() content in y-axle
    fig_aus_overview= px.line(
        participation_historical_aus,
        x= "Year", 
        y= "Participants",
        color_discrete_map={"Summer":"#efdf00", "Winter":"#52D5f2"},
        color="Season",
        markers=True
    )

    fig_aus_overview.update_yaxes(
        type="log",
        title_text="Participants (log scale)"
    )                   #Clearer curve. Shows growth instead of absolute counts.

    return [
        html.H3("Analys över Deltagande", className="mb-3"),
        html.P(
            """En sammanfattande översikt av Australiens deltagande i Olympiska spelen över tid.
        """
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                       dbc.CardBody(
                            [ 
                               html.H4(
                                   str(f"{first_year_part_summer:.0f}"),
                                   className="card-title",
                               ),
                               html.H6(
                                   "Första året i sommar-OS",
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
                               html.H4(
                                   str(f"{first_winter_year_part:.0f}"),
                                   className="card-title",
                               ),
                               html.H6(
                                   "Första året i Vinter-OS",
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
                               html.H4(
                                   str(f"{most_participants_year:.0f}"),
                                   className="card-title",
                               ),
                               html.H6(
                                   "Året med flest deltagare",
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
                                html.H4("Australiens deltagande 1896–2016"),
                                html.P("Deltagande med logaritmisk skala på y-axeln för att tydliggöra tillväxten över tid."),
                                dcc.Graph(id="id-first-graph", figure=fig_aus_overview),
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