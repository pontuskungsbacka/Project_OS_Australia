from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

directory_data = "./data"

athletes = pd.read_csv(f"{directory_data}/athlete_events.csv")
regions = pd.read_csv(f"{directory_data}/noc_regions.csv")
merged = pd.merge(athletes, regions, on="NOC", how="outer")
df = merged

aus = df[df["NOC"].isin(["AUS", "ANZ"])]
gender_per_year = (
    aus
    .groupby(["Year", "Season", "Sex"], as_index=False)
    .size()
    .rename(columns={"size": "Count"})
)
gender_per_year["Total"] = gender_per_year.groupby(["Year", "Season"])["Count"].transform("sum")
gender_per_year["Percent"] = gender_per_year["Count"] / gender_per_year["Total"] * 100
gender_per_year["NOC"] = "AUS"

countries = ["CAN", "SWE", "GBR"]

def gender_compare(df, country):
    country_df = df[df["NOC"] == country]
    gender = (
        country_df
        .groupby(["Year", "Season", "Sex"], as_index=False)
        .size()
        .rename(columns={"size": "Count"})
    )
    gender["Total"] = gender.groupby(["Year", "Season"])["Count"].transform("sum")
    gender["Percent"] = gender["Count"] / gender["Total"] * 100
    gender["NOC"] = country
    return gender

df_gender = pd.concat([gender_compare(df, c) for c in countries], ignore_index=True)
df_gender = pd.concat([df_gender, gender_per_year], axis=0)

app = Dash(
    __name__,
    meta_tags=[dict(name="viewport", content="width=device-width, initial-scale=1.0")],
)
app.title = 'Olympic Games - Team Australia Dashboard'
app._favicon = ("assets/favicon.ico")

app.layout = html.Div(
    children=[
        html.H1(
            children='Olympic Games - Team Australia Dashboard',
            style={'textAlign': 'center'}
        ),

        html.Div(
            [
                html.Label("Välj land (NOC):"),
                dcc.Dropdown(
                    id="country-dropdown",
                    options=[
                        {"label": "Australia (AUS)", "value": "AUS"},
                        {"label": "Canada (CAN)", "value": "CAN"},
                        {"label": "Sweden (SWE)", "value": "SWE"},
                        {"label": "Great Britain (GBR)", "value": "GBR"},
                    ],
                    value="AUS",
                    clearable=False
                ),
            ],
            style={"width": "300px", "margin": "0 auto 20px auto"}
        ),

        dcc.Graph(id="gender-graph"),
    ]
)

@callback(
    Output("gender-graph", "figure"),
    Input("country-dropdown", "value")
)
def update_gender_graph(selected_noc):
    dff = df_gender[df_gender["NOC"] == selected_noc]

    fig = px.bar(
        dff,
        x="Year",
        y="Percent",
        color="Sex",
        barmode="stack",
        facet_row="Season",
        width=900,
        height=500,
        hover_data={
            "Count": True,
            "Total": True,
            "Percent": ":.2f",
            "NOC": True,
        },
        title=f"Könsfördelning per år – {selected_noc}"
    )
    fig.update_layout(margin=dict(t=80, l=40, r=40, b=40))
    return fig

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
