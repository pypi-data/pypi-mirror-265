import dash_bootstrap_components as dbc
from dash import dcc, html

from .plugin_loader import load_plugins


# Function to create the layout of the Dash app
def create_layout(app):
    plugins = load_plugins()  # Loads available plugins
    plugin_options = [
        {
            "label": plugin.replace("_", " ").title(),
            "value": plugin,
        }  # Format plugins for dropdown
        for plugin in plugins.keys()
    ]

    # Define the navigation bar with logo and title
    navbar = dbc.Navbar(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src="https://assets.streamlinehq.com/image/private/w_200,h_200,ar_1/f_auto/v1/icons/freebies-freemojis/objects/objects/bar-chart-f5c5npy7d6s2nmc8ttmgxd.png?_a=DAJFJtWIZAAC",
                                height="30px",
                                className="me-3",
                            )
                        ),
                        dbc.Col(dbc.NavbarBrand("Commit Tracker", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
            ],
            fluid=True,
        ),
        color="primary",
        dark=True,
        className="mb-3",
    )

    # Plugin selector dropdown
    plugin_selector = dcc.Dropdown(
        id="plugin-selector",
        options=plugin_options,
        multi=True,  # Allows selecting multiple plugins
        placeholder="Select plugins...",
        className="mb-2",
    )

    # Input field for repository URL
    repo_input = dbc.Input(
        id="repo-input",
        type="text",
        placeholder="Enter repository URL or path...",
        className="mb-2",
    )

    # Button to load the repository
    submit_button = dbc.Button(
        "Load Repository", id="load-repo-button", color="primary", className="mb-4"
    )

    # Error messages for URL and plugin validation
    url_error_message = html.Div(id="url-error-message", style={"color": "red"})
    plugin_error_message = html.Div(id="plugin-error-message", style={"color": "red"})

    # Area where plugin outputs will be displayed
    plugin_output_area = dcc.Loading(
        id="loading", children=[html.Div(id="plugin-output-area")], type="default"
    )

    # Overall layout definition, including all components above
    layout = html.Div(
        [
            navbar,
            dbc.Container(
                [
                    dbc.Row(dbc.Col(plugin_selector, width=12, lg=8), justify="center"),
                    dbc.Row(dbc.Col(repo_input, width=12, lg=8), justify="center"),
                    dbc.Row(
                        dbc.Col(url_error_message, width=12, lg=8), justify="center"
                    ),
                    dbc.Row(
                        dbc.Col(plugin_error_message, width=12, lg=8), justify="center"
                    ),
                    dbc.Row(dbc.Col(submit_button, width=12, lg=8), justify="center"),
                    dbc.Row(dbc.Col(plugin_output_area, md=8), justify="center"),
                ],
                fluid=True,  # Container uses the entire horizontal space
            ),
        ]
    )

    return layout  # Returns the defined layout for the app
