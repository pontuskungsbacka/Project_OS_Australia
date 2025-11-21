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
    title="Topp 10 Länder med Flest Simnings-Medaljer (Totalt)",
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
           """En analys av simning i Olympiska spelen. Denna sida ger en sammanfattning av viktiga statistik och
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
                                    id="Number_of_years_swimming",
                                    className="card-title",
                                ),
                                html.H6("Antal år sporten simning har varit med i OS", className="card-subtitle"),
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
                                html.H4("-", id="total_events_swimming", className="card-title"),
                                html.H6("Antal grenar det finns i simning", className="card-subtitle"),
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
                                html.H4("Topp 10 länder – simning", className="card-title"),
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
    [
        Output("first_swimming_game", "children"),
        Output("Number_of_years_swimming", "children"),
        Output("total_events_swimming", "children")
    ],
    Input("first_swimming_game", "children"),  # Trigger on page load
)

def update_summary_cards_swim(_):
    
    # Calculate the first year Swimming was in the Olympics
    first_swimming_game = swimming_medals['Year'].min()
    
    # Calculate how many years Swimming has been in the Olympics
    Number_of_years_swimming = swimming_medals['Year'].nunique()
    
    # Calculate how many events it is in Swimming
    total_events_swimming = swimming_medals['Event'].nunique()
    
    return first_swimming_game, Number_of_years_swimming, total_events_swimming