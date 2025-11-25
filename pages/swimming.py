import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html
import plotly.express as px
import plotly.graph_objects as go
from load_data import load_olympics_data, remove_team_duplicated_medals


TITLE = "Olympiska spelen Analys - Team Australien"
OS_LOGO = "assets/olympic-logo.svg"
PAGE_TITLE = "Simning"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/swimming", order=4)
"""
To load and fixing the data 
"""
# Summirizey statistics and visualizations about medals won by Team Australia in the Olympics
df = load_olympics_data()
df.loc[(df["ID"] == 118133) & (df["Year"] == 2012), "Medal"] = "Gold"

# Filter medals
medals = df[df['Medal'].notna()]
medals_filtered = remove_team_duplicated_medals(medals, "Swimming")

# Filter for Swimming medals only
swimming_medals = medals_filtered[medals_filtered["Sport"] == "Swimming"]

# Count medals by country and medal type
swimming_counts = (
    swimming_medals
    .groupby(["region", "Medal"])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)

# Se till att kolumnerna finns även om någon medaljtyp saknas
for col in ["Gold", "Silver", "Bronze"]:
    if col not in swimming_counts.columns:
        swimming_counts[col] = 0

# Calculate total medals
swimming_counts["Total"] = (
    swimming_counts["Gold"] +
    swimming_counts["Silver"] +
    swimming_counts["Bronze"]
)

# Get top 10 countries by total medals
top10_swimming = swimming_counts.nlargest(10, "Total").reset_index(drop=True)
top10_swimming["Rank"] = range(1, 11)

# Sort by total for better visualization (ascending for horizontal bars)
top10_swimming = top10_swimming.sort_values("Total", ascending=True)

# Create horizontal stacked bar chart
fig_swimming = go.Figure()

# Add Bronze bars
fig_swimming.add_trace(go.Bar(
    y=top10_swimming["region"],
    x=top10_swimming["Bronze"],
    name="Bronze",
    orientation="h",
    marker_color="#996B4F",
    text=top10_swimming["Bronze"],
    textposition="inside",
    hovertemplate="Bronze: %{x}<extra></extra>",
))

# Add Silver bars
fig_swimming.add_trace(go.Bar(
    y=top10_swimming["region"],
    x=top10_swimming["Silver"],
    name="Silver",
    orientation="h",
    marker_color="#969696",
    text=top10_swimming["Silver"],
    textposition="inside",
    hovertemplate="Silver: %{x}<extra></extra>",
))

# Add Gold bars
fig_swimming.add_trace(go.Bar(
    y=top10_swimming["region"],
    x=top10_swimming["Gold"],
    name="Gold",
    orientation="h",
    marker_color="#9F8F5E",
    text=top10_swimming["Gold"],
    textposition="inside",
    hovertemplate="Gold: %{x}<extra></extra>",
))

# Add rank annotations
for _, row in top10_swimming.iterrows():
    fig_swimming.add_annotation(
        x=row["Total"] + 1,  # lite marginal utanför stapeln
        y=row["region"],
        text=f"#{row['Rank']}",
        showarrow=False,
        font=dict(size=12, color="black", family="Arial Black"),
        xanchor="left",
    )

fig_swimming.update_layout(
    xaxis_title="Antal Medaljer",
    yaxis_title="Land",
    barmode="stack",
    height=600,
    showlegend=True,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
    ),
    hovermode="y unified",
)

fig_swimming.update_xaxes(showgrid=True, gridcolor="lightgray")
fig_swimming.update_yaxes(showgrid=False)


def layout():
    return [
        html.H3("Simning", className="mb-3"),
        html.P(
           """En analys av simning i Olympiska spelen. Denna sida ger en sammanfattning av viktig statistik och
        visualiseringar prestationer i simning under de Olympiska spelen.
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
                                    id="first_swimming_game",
                                    className="card-title",
                                ),
                                html.H6("Första året simning fanns med som gren i OS", className="card-subtitle"),
                            ]
                        ),className="mh-100", style={"height": "7rem"},
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
                                    id="Number_of_years_swimming",
                                    className="card-title",
                                ),
                                html.H6("Antal olympiska spel simning har varit med som en sport", className="card-subtitle"),
                            ]
                        ),className="mh-100", style={"height": "7rem"},
                    ),
                    class_name="mb-3",
                    md=4,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("-", id="total_events_swimming", className="card-title"),
                                html.H6("Antal grenar det finns i simning", className="card-subtitle"),
                            ]
                        ),className="mh-100", style={"height": "7rem"},
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
                                    id="best_country_swimming",
                                    className="card-title",
                                ),
                                html.H6("Är landet med flest medaljer.", className="card-subtitle"),
                                html.P("-", id="second_country_swimming", className="card-subtitle", style={"margin-top": "0.5rem","font-weight": "bold", "font-size" : "0.7rem"}), 
                            ]
                        ),className="mh-100", style={"height": "10rem"},
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
                                    id="best_swimmer_medals",
                                    className="card-title",
                                ),
                                html.H6("Antal medaljer den bästa simmaren har vunnit genom tiderna", className="card-subtitle"),
                                html.P("-", id="best_swimmer_gender_event", className="card-subtitle", style={"margin-top": "0.5rem","font-weight": "bold", "font-size" : "0.7rem"}),
                            ]
                        ),className="mh-100", style={"height": "10rem"},
                    ),
                    class_name="mb-3",
                    md=4,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("-", id="gender_swimming", className="card-title"),
                                html.H6("Könsfördelning", className="card-subtitle"),
                            ]
                        ),className="mh-100", style={"height": "10rem"},
                    ),
                    class_name="mb-3",
                    md=4,
                    sm=12,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Vilka länder är top 10 och har mest medaljer genom tiderna?", className="card-title"),
                                    dcc.Graph(
                                        id="swimming-top10-graph",
                                        figure=fig_swimming,  # <-- här kopplas figuren in
                                    ),
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
    [
        Output("first_swimming_game", "children"),
        Output("Number_of_years_swimming", "children"),
        Output("total_events_swimming", "children"),
        Output("gender_swimming", "children"),
        Output("best_country_swimming", "children"),
        Output("second_country_swimming", "children"),
        Output("best_swimmer_medals", "children"),
        Output("best_swimmer_gender_event", "children"),
    ],
    Input("first_swimming_game", "children"),  # Trigger on page load
)

def update_summary_cards_swim(_):
    
    # Calculate the first year Swimming was in the Olympics
    first_swimming_game_value = swimming_medals['Year'].min()
    first_swimming_game = str(f"{first_swimming_game_value:.0f} år")

    # Calculate how many years Swimming has been in the Olympics
    Number_of_years_swimming_value = swimming_medals['Year'].nunique()
    Number_of_years_swimming = str(f"{Number_of_years_swimming_value} st")
    
    # Calculate how many events it is in Swimming
    total_events_swimming_value = swimming_medals['Event'].nunique()
    total_events_swimming = str(f"{total_events_swimming_value} st")

    # Count how many Female and Male has won medals in Swimming
    gender_counts_swimming = swimming_medals["Sex"].value_counts()
    gender_swimming = str(f"Kvinnor: {gender_counts_swimming.get('F', 0)} | Män: {gender_counts_swimming.get('M', 0)}")

    # Best country (most medals)
    best_country_row = swimming_counts.sort_values("Total", ascending=False).iloc[0]
    best_country_swimming = str(f"{best_country_row['region']}")

    # Second best country
    second_best_row = swimming_counts.sort_values("Total", ascending=False).iloc[1]
    second_country_swimming = str(f"Andra plats: {second_best_row['region']}")

    # Best swimmer by ID (most medals)
    best_swimmer_id = swimming_medals['ID'].value_counts().idxmax()
    best_swimmer_medal_count = swimming_medals['ID'].value_counts().max()
    best_swimmer_medals = str(f"{best_swimmer_medal_count} st")

    # Get best swimmer details
    best_swimmer_data = swimming_medals[swimming_medals['ID'] == best_swimmer_id].iloc[0]
    best_swimmer_gender = best_swimmer_data['Sex']
    
    # Get the event they won most medals in
    swimmer_events = swimming_medals[swimming_medals['ID'] == best_swimmer_id]
    best_event = swimmer_events['Event'].value_counts().idxmax()
    
    best_swimmer_gender_event = str(f"Kön: {best_swimmer_gender} - Bästa gren: {best_event}")
    
    return first_swimming_game, Number_of_years_swimming, total_events_swimming, gender_swimming, best_country_swimming, second_country_swimming, best_swimmer_medals, best_swimmer_gender_event