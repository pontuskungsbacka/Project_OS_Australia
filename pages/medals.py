import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, callback, dcc, html
import plotly.express as px
import plotly.graph_objects as go
from load_data import load_olympics_data

TITLE = "Olympiska spelen Analys - Team Australien"
OS_LOGO = "assets/olympic-logo.svg"
PAGE_TITLE = "Medaljer anlys"

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/medals", order=1)
"""
To load and fixing the data 
"""
# Summirizey statistics and visualizations about medals won by Team Australia in the Olympics
df = load_olympics_data()
df.loc[(df["ID"] == 118133) & (df["Year"] == 2012), "Medal"] = "Gold"

# Filter medals
medals = df[df['Medal'].notna()]
medals_filtered = medals.drop_duplicates(
    subset=["Year", "Season", "Event", "NOC", "Medal"]
)
"""
Prepare the dataframe for plotting medal
"""
# Prepare medal counts
medal_counts_per_year = (
    medals_filtered
    .groupby(['Year', 'region'])
    .size()
    .reset_index(name='Medals')
)

medal_counts_per_year = medal_counts_per_year.sort_values('Year')
medal_counts_per_year['Cumulative_Medals'] = (
    medal_counts_per_year
    .groupby('region')['Medals']
    .cumsum()
)
# Filter for AUS and ANZ
df_medals = medals_filtered[medals_filtered["NOC"].isin(["AUS", "ANZ"])]

# Count medals per year, season, and type
medal_counts_withsports = (
    df_medals.groupby(["Season", "Year", "Sport", "Medal"])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)

# Remove the column name from the header
medal_counts_withsports.columns.name = None

medal_counts_withsports.head()

# Get top 15 + Australia
def get_top15_with_australia(year_data):
    year_data = year_data.sort_values('Cumulative_Medals', ascending=False).reset_index(drop=True)
    year_data['Rank'] = range(1, len(year_data) + 1)
    top15 = year_data.head(15).copy()
    
    if 'Australia' not in top15['region'].values:
        aus_row = year_data[year_data['region'] == 'Australia']
        if not aus_row.empty:
            result = pd.concat([top15, aus_row])
        else:
            result = top15
    else:
        result = top15
    
    return result

all_years_data = []
for year in sorted(medal_counts_per_year['Year'].unique()):
    year_data = medal_counts_per_year[medal_counts_per_year['Year'] == year]
    top_countries = get_top15_with_australia(year_data)
    top_countries['Year'] = year
    all_years_data.append(top_countries)

final_data = pd.concat(all_years_data, ignore_index=True)
final_data['Färger'] = final_data['region'].apply(
    lambda x: 'Australia' if x == 'Australia' else 'Andra länder'
)
"""
The Figure for medals to see who have the most medals
"""
# Create figure
fig = px.bar(
    final_data,
    x='Cumulative_Medals',
    y='region',
    animation_frame='Year',
    orientation='h',
    color='Färger',
    color_discrete_map={
        'Australia': '#0D5257',
        'Andra länder': '#BBBCBC'
    },
    title='Topp 15 OS-medaljör länder över tid i jämförelse med Australien',
    labels={
        'Cumulative_Medals': 'Totala Medaljer',
        'region': 'Länder',
        'Year': 'År'
    },
    range_x=[0, final_data['Cumulative_Medals'].max() * 1.1],
    text='Rank'
)

fig.update_traces(texttemplate='#%{text}', textposition='outside')
fig.update_layout(
    xaxis_title='Totala Medaljer',
    yaxis_title='Länder',
    yaxis={'categoryorder': 'total ascending'},
    height=500,
    showlegend=True,
    paper_bgcolor="rgba(0, 0, 0, 0)",
    plot_bgcolor="rgba(0, 0, 0, 0)",
)
fig.update_xaxes(showgrid=True)
fig.update_yaxes(showgrid=False)
"""
Here is for the sunburst chart to show how little winter OS is

"""
# Reshape data for sunburst
sunburst_data = []

for _, row in medal_counts_withsports.iterrows():
    season = row['Season']
    year = int(row['Year'])
    sport = row['Sport']
    
    # Add each medal type as separate row
    if row['Gold'] > 0:
        sunburst_data.append({
            'Season': season,
            'Year': year,
            'Sport': sport,
            'Medal': 'Gold',
            'Count': row['Gold']
        })
    if row['Silver'] > 0:
        sunburst_data.append({
            'Season': season,
            'Year': year,
            'Sport': sport,
            'Medal': 'Silver',
            'Count': row['Silver']
        })
    if row['Bronze'] > 0:
        sunburst_data.append({
            'Season': season,
            'Year': year,
            'Sport': sport,
            'Medal': 'Bronze',
            'Count': row['Bronze']
        })

sunburst_df = pd.DataFrame(sunburst_data)

# Calculate participation statistics
aus_participated_games = sunburst_df[['Season', 'Year']].drop_duplicates()
aus_summer_games = aus_participated_games[aus_participated_games['Season'] == 'Summer']['Year'].nunique()
aus_winter_games = aus_participated_games[aus_participated_games['Season'] == 'Winter']['Year'].nunique()
total_aus_games = aus_participated_games['Year'].nunique()

# Total Olympic Games ever held (approximate from data)
total_summer_games = df[(df['Season'] == 'Summer')]['Year'].nunique()
total_winter_games = df[(df['Season'] == 'Winter')]['Year'].nunique()

# Build hierarchical data
labels = []
parents = []
values = []
colors = []
ids = []

total_games_os = 28+22

# Root: Australia with total games participated
labels.append(f'Australien har fått medaljer i<br>{total_aus_games} olympiska spel av {total_games_os}')
parents.append('')
values.append(sunburst_df['Count'].sum())
colors.append('#FFFFFF')
ids.append('australia')

# Level 1: Season (with games participated / total games)
for season in ['Summer', 'Winter']:
    season_data = sunburst_df[sunburst_df['Season'] == season]
    if not season_data.empty:
        total_medals = season_data['Count'].sum()
        participated = season_data['Year'].nunique()
        total_games = total_summer_games if season == 'Summer' else total_winter_games
        
        labels.append(f'{season}<br>{participated}/{total_games} antal olympiska spel med medaljer<br>{int(total_medals)} medaljer')
        parents.append('australia')
        values.append(total_medals)
        colors.append('#BBBCBC' if season == 'Summer' else '#0E5959')
        ids.append(season.lower())

# Level 2: Year per Season (with medal count)
for season in ['Summer', 'Winter']:
    season_data = sunburst_df[sunburst_df['Season'] == season]
    if not season_data.empty:
        for year in sorted(season_data['Year'].unique()):
            year_data = season_data[season_data['Year'] == year]
            year_medals = year_data['Count'].sum()
            
            labels.append(f'{year}<br>{int(year_medals)} Medaljer')
            parents.append(season.lower())
            values.append(year_medals)
            colors.append('#D9D9D6' if season == 'Summer' else '#3B7F7F')
            ids.append(f'{season.lower()}_{year}')

# Level 3: Medal Type per Year
for season in ['Summer', 'Winter']:
    season_data = sunburst_df[sunburst_df['Season'] == season]
    if not season_data.empty:
        for year in sorted(season_data['Year'].unique()):
            year_data = season_data[season_data['Year'] == year]
            
            for medal in ['Gold', 'Silver', 'Bronze']:
                medal_data = year_data[year_data['Medal'] == medal]
                if not medal_data.empty:
                    medal_count = medal_data['Count'].sum()
                    
                    labels.append(f'{medal}<br>{int(medal_count)}')
                    parents.append(f'{season.lower()}_{year}')
                    values.append(medal_count)
                    
                    if medal == 'Gold':
                        colors.append('#B3A679')
                    elif medal == 'Silver':
                        colors.append('#B0B0B0')
                    else:
                        colors.append('#B6856A')
                    
                    ids.append(f'{season.lower()}_{year}_{medal.lower()}')

# Level 4: Sport per Medal Type
for season in ['Summer', 'Winter']:
    season_data = sunburst_df[sunburst_df['Season'] == season]
    if not season_data.empty:
        for year in sorted(season_data['Year'].unique()):
            year_data = season_data[season_data['Year'] == year]
            
            for medal in ['Gold', 'Silver', 'Bronze']:
                medal_data = year_data[year_data['Medal'] == medal]
                if not medal_data.empty:
                    for sport in medal_data['Sport'].unique():
                        sport_data = medal_data[medal_data['Sport'] == sport]
                        sport_count = sport_data['Count'].sum()
                        
                        labels.append(f'{sport}<br>{int(sport_count)}')
                        parents.append(f'{season.lower()}_{year}_{medal.lower()}')
                        values.append(sport_count)
                        
                        # Sport colors - very light shade
                        if medal == 'Gold':
                            colors.append('#CABC99')
                        elif medal == 'Silver':
                            colors.append('#CACACA')
                        else:
                            colors.append('#D0A38A')
                        
                        ids.append(f'{season.lower()}_{year}_{medal.lower()}_{sport}')

# Create sunburst figure at module level
sunburst_medals = go.Figure(go.Sunburst(
    ids=ids,
    labels=labels,
    parents=parents,
    values=values,
    marker=dict(colors=colors, line=dict(width=1, color='white')),
    textinfo='label',
    hovertemplate='<b>%{label}</b><br>Medaljer: %{value}<extra></extra>',
    branchvalues='total',
    maxdepth=3
))
sunburst_medals.update_layout(
    title='Australia Olympic Participation & Medals: Games → Year → Medal Type → Sport',
    margin=dict(t=50, l=0, r=0, b=0),
    height=600
)

def layout():
    return [
        html.H3("Medaljer analys", className="mb-3"),
        html.P(
            """En analys av medaljer vunna av Team Australien i Olympiska spelen. Denna sida ger en sammanfattning av viktiga statistik och
        visualiseringar relaterade till Australiens medaljprestationer i de Olympiska spelen.
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
                                    id="number_of_olympic_games",
                                    className="card-title",
                                ),
                                html.H6("Antal olympiska spel", className="card-subtitle"),
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
                                    id="Number_of_medals",
                                    className="card-title",
                                ),
                                html.H6("Antalet medaljer", className="card-subtitle"),
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
                                html.H4("-", id="total_athletes", className="card-title"),
                                html.H6("Totalt althleter", className="card-subtitle"),
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
                                html.H4("Första grafen kommer här"),
                                html.P("Text om graf."),
                                dcc.Graph(
                                id='animated-bar-chart',
                                figure=fig,
                                style={'height': '700px'}
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
                                html.H4("Australiens OS-medaljer", className="card-title"),
                                html.P("Sunburst: Säsong → År → Medalj → Sport"),
                                dcc.Graph(
                                    id="sunburst_medals",
                                    figure = sunburst_medals
                                ),
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
        Output("number_of_olympic_games", "children"),
        Output("Number_of_medals", "children"),
        Output("total_athletes", "children")
    ],
    Input("number_of_olympic_games", "children"),  # Trigger on page load
)
def update_summary_cards(_):
    # Filter for Australia
    aus_data = df[df['region'] == 'Australia']
    
    # Calculate number of Olympic Games Australia participated in
    number_of_olympic_games = aus_data['Games'].nunique()
    
    # Calculate total medals won by Australia
    aus_medals = medals_filtered[medals_filtered['NOC'].isin(['AUS', 'ANZ'])]
    Number_of_medals = len(aus_medals)
    
    # Calculate total unique athletes
    total_athletes = aus_data['ID'].nunique()
    
    return number_of_olympic_games, Number_of_medals, total_athletes
