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

dash.register_page(__name__, name=PAGE_TITLE, title=f"{PAGE_TITLE} | {TITLE}", path="/", order=1)
"""
To load and fixing the data 
"""
# Summirizey statistics and visualizations about medals won by Team Australia in the Olympics
df = load_olympics_data()
df.loc[(df["ID"] == 118133) & (df["Year"] == 2012), "Medal"] = "Gold"
df = df[df['Year'] != 1906]
df = df[df['Sport'] != "Alpinism"]

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

# Get all Olympic years
olympic_years = sorted(medal_counts_per_year['Year'].unique())

# Create frames for each year
frames = []
for selected_year in olympic_years:
    # Get data for that year
    year_data = medal_counts_per_year[medal_counts_per_year['Year'] == selected_year].copy()
    year_data = year_data.sort_values('Cumulative_Medals', ascending=False).reset_index(drop=True)
    year_data['Rank'] = range(1, len(year_data) + 1)
    
    # Get top 10
    top10 = year_data.head(10).copy()
    
    # Get medal type counts for top 10
    top10_with_medals = []
    for _, country_row in top10.iterrows():
        country = country_row['region']
        country_medals = medals_filtered[
            (medals_filtered['region'] == country) & 
            (medals_filtered['Year'] <= selected_year)
        ]
        
        medal_counts = country_medals.groupby('Medal').size().to_dict()
        
        top10_with_medals.append({
            'region': country,
            'Rank': country_row['Rank'],
            'Total': country_row['Cumulative_Medals'],
            'Gold': medal_counts.get('Gold', 0),
            'Silver': medal_counts.get('Silver', 0),
            'Bronze': medal_counts.get('Bronze', 0)
        })
    
    top10_df = pd.DataFrame(top10_with_medals)
    top10_df = top10_df.sort_values('Total', ascending=True)
    
    # Get Australia's rank for this year
    australia_rank = year_data[year_data['region'] == 'Australia']['Rank'].values
    aus_rank = int(australia_rank[0]) if len(australia_rank) > 0 else None
    
    # Create frame data
    frame_data = []
    
    # Bronze bars
    frame_data.append(go.Bar(
        y=top10_df['region'],
        x=top10_df['Bronze'],
        name='Brons',
        orientation='h',
        marker_color='#996B4F',
        text=top10_df['Bronze'],
        textposition='inside',
        hovertemplate='Brons: %{x}<extra></extra>',
        showlegend=False
    ))
    
    # Silver bars
    frame_data.append(go.Bar(
        y=top10_df['region'],
        x=top10_df['Silver'],
        name='Silver',
        orientation='h',
        marker_color='#969696',
        text=top10_df['Silver'],
        textposition='inside',
        hovertemplate='Silver: %{x}<extra></extra>',
        showlegend=False
    ))
    
    # Gold bars
    frame_data.append(go.Bar(
        y=top10_df['region'],
        x=top10_df['Gold'],
        name='Guld',
        orientation='h',
        marker_color='#9F8F5E',
        text=top10_df['Gold'],
        textposition='inside',
        hovertemplate='Guld: %{x}<extra></extra>',
        showlegend=False
    ))
    
    # Create annotations for ranks (to the right of bars)
    annotations = []
    for idx, row in top10_df.iterrows():
        annotations.append(dict(
            x=row['Total'] + (top10_df['Total'].max() * 0.02),
            y=row['region'],
            text=f"#{int(row['Rank'])}",
            showarrow=False,
            font=dict(size=14, color='#333333', family='Arial Black'),
            xanchor='left'
        ))
    
    # Add Australia rank to title
    aus_rank_text = f"Australia: #{aus_rank}" if aus_rank else "Australia: Not in top 10"
    
    frames.append(go.Frame(
        data=frame_data,
        name=str(selected_year),
        layout=go.Layout(
            annotations=annotations,
            title=f'Topp 10 Länder OS {selected_year} - Totala Medaljer<br><sub>{aus_rank_text}</sub>'
        )
    ))

# Create initial figure (first year)
initial_year = olympic_years[0]
year_data = medal_counts_per_year[medal_counts_per_year['Year'] == initial_year].copy()
year_data = year_data.sort_values('Cumulative_Medals', ascending=False).reset_index(drop=True)
year_data['Rank'] = range(1, len(year_data) + 1)

top10 = year_data.head(10).copy()
top10_with_medals = []
for _, country_row in top10.iterrows():
    country = country_row['region']
    country_medals = medals_filtered[
        (medals_filtered['region'] == country) & 
        (medals_filtered['Year'] <= initial_year)
    ]
    medal_counts = country_medals.groupby('Medal').size().to_dict()
    top10_with_medals.append({
        'region': country,
        'Rank': country_row['Rank'],
        'Total': country_row['Cumulative_Medals'],
        'Gold': medal_counts.get('Gold', 0),
        'Silver': medal_counts.get('Silver', 0),
        'Bronze': medal_counts.get('Bronze', 0)
    })

top10_df = pd.DataFrame(top10_with_medals)
top10_df = top10_df.sort_values('Total', ascending=True)

australia_rank = year_data[year_data['region'] == 'Australia']['Rank'].values
aus_rank_text = f"Australia: #{int(australia_rank[0])}" if len(australia_rank) > 0 else "Australia: Not in top 10"

# Create figure
fig = go.Figure()

fig.add_trace(go.Bar(
    y=top10_df['region'],
    x=top10_df['Bronze'],
    name='Brons',
    orientation='h',
    marker_color='#996B4F',
    text=top10_df['Bronze'],
    textposition='inside',
    hovertemplate='Brons: %{x}<extra></extra>'
))

fig.add_trace(go.Bar(
    y=top10_df['region'],
    x=top10_df['Silver'],
    name='Silver',
    orientation='h',
    marker_color='#969696',
    text=top10_df['Silver'],
    textposition='inside',
    hovertemplate='Silver: %{x}<extra></extra>'
))

fig.add_trace(go.Bar(
    y=top10_df['region'],
    x=top10_df['Gold'],
    name='Guld',
    orientation='h',
    marker_color='#9F8F5E',
    text=top10_df['Gold'],
    textposition='inside',
    hovertemplate='Guld: %{x}<extra></extra>'
))

# Add rank annotations to the right of bars
for idx, row in top10_df.iterrows():
    fig.add_annotation(
        x=row['Total'] + (top10_df['Total'].max() * 0.02),
        y=row['region'],
        text=f"#{int(row['Rank'])}",
        showarrow=False,
        font=dict(size=14, color='#333333', family='Arial Black'),
        xanchor='left'
    )

# Add frames
fig.frames = frames

# Add slider
sliders = [dict(
    active=0,
    yanchor="top",
    y=-0.15,
    xanchor="left",
    x=0.1,
    currentvalue=dict(
        prefix="År: ",
        visible=True,
        xanchor="center",
        font=dict(size=16)
    ),
    steps=[dict(
        method="animate",
        args=[
            [str(year)],
            dict(
                mode="immediate",
                frame=dict(duration=500, redraw=True),
                transition=dict(duration=300)
            )
        ],
        label=str(year)
    ) for year in olympic_years]
)]

fig.update_layout(
    title=f'Topp 10 Länder OS {initial_year} - Totala Medaljer<br><sub>{aus_rank_text}</sub>',
    xaxis_title='Antal Medaljer',
    yaxis_title='',
    barmode='stack',
    height=600,
    showlegend=True,
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1
    ),
    sliders=sliders,
    hovermode='y unified',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    xaxis=dict(range=[0, medal_counts_per_year.groupby('Year')['Cumulative_Medals'].max().max() * 1.05])
)

fig.update_xaxes(showgrid=True, gridcolor='lightgray')
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

df_AUS = df[df["NOC"].isin(["AUS", "ANZ"])]

# Total Olympic Games ever held (approximate from data)
total_summer_games = df_AUS[(df_AUS['Season'] == 'Summer')]['Year'].nunique()
total_winter_games = df_AUS[(df_AUS['Season'] == 'Winter')]['Year'].nunique()

# Build hierarchical data
labels = []
parents = []
values = []
colors = []
ids = []

total_games_os = total_summer_games + total_winter_games
season_data = sunburst_df[sunburst_df['Season'] == season]
total_medals_all = sunburst_df['Year'].nunique()


# Root: Australia with total games participated
labels.append(f'Australia got medals in<br>{total_medals_all} Olympic Games<br>out of {total_games_os}')
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
        
        labels.append(f'{season}<br>{participated}/{total_games} total olympic games<br> with medals<br>{int(total_medals)} medals')
        parents.append('australia')
        values.append(total_medals)
        colors.append('#3B7F7F' if season == 'Summer' else '#0E5959')
        ids.append(season.lower())

# Level 2: Year per Season (with medal count)
for season in ['Summer', 'Winter']:
    season_data = sunburst_df[sunburst_df['Season'] == season]
    if not season_data.empty:
        for year in sorted(season_data['Year'].unique()):
            year_data = season_data[season_data['Year'] == year]
            year_medals = year_data['Count'].sum()
            
            labels.append(f'{year}<br>{int(year_medals)} medals')
            parents.append(season.lower())
            values.append(year_medals)
            colors.append('#7EB2B2' if season == 'Summer' else '#3B7F7F')
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
    hovertemplate='<b>%{label}</b><extra></extra>',  # Remove %{value} from hover
    branchvalues='total',  # This means parent values = sum of children
    maxdepth=3
))
sunburst_medals.update_layout(
    margin=dict(t=50, l=0, r=0, b=0),
    height=650
)

def layout():
    return [
        html.H3("Medaljer", className="mb-3"),
        html.P(
            """En analys över hur många medaljer Team Australia har fått genom tiderna och i vilken säsong det presterar bäst i. 
        """
        ),
        html.Div([
        html.Span("-", id="gold_medals", className="gold dot"),
        html.Span("-", id="silver_medals", className="silver dot"),
        html.Span("-", id="bronze_medals", className="bronze dot"),
        ], style={"margin-bottom": "20px", "text-align": "center"}),
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
                                html.H6("Totalt atleter", className="card-subtitle"),
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
                                    id="number_of_summer_medals",
                                    className="card-title",
                                ),
                                html.H6("Antal sommar OS-medaljer", className="card-subtitle"),
                                html.P("-", id="medals_in_each_summer", className="card-subtitle", style={"margin-top": "0.5rem", "font-weight": "bold", "font-size" : "0.7rem"}),
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
                                    id="number_of_winter_medals",
                                    className="card-title",
                                ),
                                html.H6("Antal vinter OS-medaljer", className="card-subtitle"),
                                html.P("-", id="medals_in_each_winter", className="card-subtitle", style={"margin-top": "0.5rem","font-weight": "bold", "font-size" : "0.7rem"}),
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
                                    id="number_of_athlete_medals",
                                    className="card-title",
                                ),
                                html.H6("Antal atleter med OS-medaljer", className="card-subtitle"),
                                html.P("-", id="medals_for_team_event", className="card-subtitle", style={"margin-top": "0.5rem","font-weight": "bold", "font-size" : "0.7rem"}), 
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
                                html.H4("I vilka och hur många medaljer har Australien fått i OS som det har deltagit i? Är det någon skillnad mellan sommar- och vinter-OS?", className="card-title"),
                                html.P("Grafen visar en hierarkisk vy av medaljer som Australien har fått i Olympiska spelen, uppdelat efter säsong, år, medaljtyp och sport."),
                                dcc.Graph(
                                    id="sunburst_medals",
                                    figure = sunburst_medals
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
                                html.H4("Hur många medaljer har Australien fått kontra övriga top 10 länder i de olympiska spelen, genom åren?"),
                                html.P("Grafen illustrerar hur många medaljer alla länder fått i OS och vilken ställning just Australien har."),
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
            ],
            class_name="g-3",
        ),
    ]

@callback(
    [
        Output("number_of_olympic_games", "children"),
        Output("Number_of_medals", "children"),
        Output("total_athletes", "children"),
        Output("gold_medals", "children"),
        Output("silver_medals", "children"),
        Output("bronze_medals", "children"),
        Output("number_of_summer_medals", "children"),
        Output("medals_in_each_summer", "children"),
        Output("number_of_winter_medals", "children"),
        Output("medals_in_each_winter", "children"),
        Output("number_of_athlete_medals", "children"),
        Output("medals_for_team_event", "children"),
    ],
    Input("number_of_olympic_games", "children"),  # Trigger on page load
)
def update_summary_cards(_):
    # Filter for Australia
    aus_data = df[df['region'] == 'Australia']
    
    # Calculate number of Olympic Games Australia participated in
    number_of_olympic_games = total_games_os
    
    # Calculate total medals won by Australia
    aus_medals = medals_filtered[medals_filtered['NOC'].isin(['AUS', 'ANZ'])]
    Number_of_medals = len(aus_medals)
    
    # Calculate total unique athletes
    total_athletes = aus_data['ID'].nunique()
    
    # Calculate total gold, silver, and bronze medals for Australia
    gold_medals = len(aus_medals[aus_medals['Medal'] == 'Gold'])
    silver_medals = len(aus_medals[aus_medals['Medal'] == 'Silver'])
    bronze_medals = len(aus_medals[aus_medals['Medal'] == 'Bronze'])
    
    # Calculate number of summer and winter games with medals
    summer_medals = aus_medals[aus_medals['Season'] == 'Summer']
    winter_medals = aus_medals[aus_medals['Season'] == 'Winter']
    
    number_of_summer_medals = len(summer_medals)
    number_of_winter_medals = len(winter_medals)
    
    # Calculate games participated vs medals won for summer
    summer_games_with_medals = summer_medals['Year'].nunique()
    summer_games_participated = aus_data[aus_data['Season'] == 'Summer']['Year'].nunique()
    medals_in_each_summer = f"{summer_games_with_medals}/{summer_games_participated} antal olympiska spel med medaljer"
    
    # Calculate games participated vs medals won for winter
    winter_games_with_medals = winter_medals['Year'].nunique()
    winter_games_participated = aus_data[aus_data['Season'] == 'Winter']['Year'].nunique()
    medals_in_each_winter = f"{winter_games_with_medals}/{winter_games_participated} antal olympiska spel med medaljer"
    
    # Calculate unique athletes with medals
    number_of_athlete_medals = aus_medals['ID'].nunique()
    
    # Calculate how many team event medals
    team_event_medals = aus_medals[aus_medals['Event'].str.contains("Team", case=False, na=False)]
    medals_for_team_event= f"Antal vunna lag-tävlingar {len(team_event_medals)} st"

    return number_of_olympic_games, Number_of_medals, total_athletes, gold_medals, silver_medals, bronze_medals, number_of_summer_medals, medals_in_each_summer, number_of_winter_medals, medals_in_each_winter, number_of_athlete_medals, medals_for_team_event