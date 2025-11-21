import os
import dash
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, State, dcc, html
import plotly.express as px
import pandas as pd

TITLE = "Olympiska spelen Analys - Team Australien"
OS_LOGO = "assets/img/olympic-logo.svg"


app = Dash(title=TITLE, external_stylesheets=[dbc.icons.BOOTSTRAP], use_pages=True, suppress_callback_exceptions=True)
app._favicon = ("assets/favicon.ico")
server = app.server
NAVBAR = {
    "Team Australia": {
        "Översikt analys": {"icon": "bi bi-clipboard-data", "relative_path": "/", "class": "nav-item-team"},
        "Medaljer analys": {"icon": "bi bi-award", "relative_path": "/medals", "class": "nav-item-team"},
        "Åldersanalys": {"icon": "bi bi-person-vcard", "relative_path": "/age", "class": "nav-item-team"},
        "Genusanalys": {"icon": "bi bi-gender-ambiguous", "relative_path": "/gender", "class": "nav-item-team"},
    },
    "OS Sport Analys": {
        "Simning": {"icon": "swm-logo", "relative_path": "/swimming", "class": "nav-item-sport"},
        "Rodd": {"icon": "row-logo", "relative_path": "/rowing", "class": "nav-item-sport"},
        "Landhockey": {"icon": "hoc-logo", "relative_path": "/hockey", "class": "nav-item-sport"},
        "Ridning": {"icon": "equ-logo", "relative_path": "/equestrian", "class": "nav-item-sport"},
    },
    "Projektet": {
        "Om oss": {"icon": "bi bi-info-circle-fill", "relative_path": "/about", "class": "nav-item-project"},
    },
}

def generate_nav_links(navbar_dict):
    nav_items = []
    for category, items in navbar_dict.items():
        # Add a category header
        nav_items.append(html.Div(category, className="navbar-category"))
        # Add links for each item in the category
        for label, details in items.items():
            nav_items.append(
                dbc.NavLink(
                    [
                        html.I(className=details["icon"], style={"margin-right": "0.5rem"}),
                        label,
                    ],
                    href=details["relative_path"],
                    className="nav-link",
                )
            )
    return nav_items


SIDEBAR_STYLE = {
    "position": "fixed",
    "overflow": "scroll",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


sidebar = html.Div(
    [
        html.Img(src=OS_LOGO, width=60),
        html.Hr(),
        html.P("Olympiska spelen Analys - Team Australien", className="lead"),
        dbc.Nav([], vertical=True, pills=True, id="sidebar-nav"),
    ],
    style=SIDEBAR_STYLE,
    className="d-none d-md-block",  # Hidden on small screens, visible on medium+
    id="sidebar",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            dcc.Link(
                [
                    html.Img(src=OS_LOGO, width=30, height=30, className="d-inline-block align-top mr-2"),
                    "Olympiska spelen Analys - Team Australien",
                ],
                href="/",
                className="navbar-brand",
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                generate_nav_links(NAVBAR),
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="light",
    dark=False,
    className="d-block d-md-none",  # Visible only on small screens, hidden on medium+
)

content = html.Div(
    dbc.Spinner(
        dash.page_container,
        delay_show=0,
        delay_hide=100,
        color="primary",
        spinner_class_name="fixed-top",
        spinner_style={"margin-top": "100px"},
    ),
    className="content",
)

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        sidebar,
        navbar,
        content,
    ]
)

@app.callback(Output("sidebar-nav", "children"), Input("url", "pathname"))
def update_navbar(url: str) -> list:
    return [
        html.Div(
            [
                html.H5(navbar_group, className="navbar-group-title"),
                html.Hr(className="navbar-divider"),
                html.Div(
                    [
                        dcc.Link(
                            html.Div(
                                [html.I(className=page_values["icon"] + " mr-1"), page_name],
                                className="d-flex align-items-center",
                            ),
                            href=page_values["relative_path"],
                            # add the item class to the link so CSS can select it
                            className=(("nav-link active mb-1 " if page_values["relative_path"] == url else "nav-link mb-1 ") + page_values.get("class", "")),
                            title=page_name,
                        )
                        for page_name, page_values in navbar_pages.items()
                    ]
                ),
            ],
            className="mb-4",
        )
        for navbar_group, navbar_pages in NAVBAR.items()
    ]

@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks"), Input("url", "pathname")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, _, is_open):
    # close collapse when navigating to new page
    if dash.callback_context.triggered_id == "url":
        return False

    if n:
        return not is_open
    return is_open

if __name__ == "__main__":
    app.run()