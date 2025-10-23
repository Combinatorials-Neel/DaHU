"""
Class containing all Dash items and layout information for the profil tab
"""
from dash import html, dcc
import dash_bootstrap_components as dbc


def profil_top_left_card():
    card = dbc.Card([
            dbc.CardHeader("Heatmap Options"),
            dbc.CardBody([
                html.Label("Currently plotting:"),
                html.Br(),
                dbc.Select(
                    id="profil_heatmap_select",
                    options=[],
                    placeholder="Select property",
                ),
                dbc.Row([
                    html.Label("Colorbar bounds"),
                    dbc.Input(
                        id="profil_heatmap_max",
                        type="number",
                        placeholder="maximum value",
                        value=None,
                    ),
                    dbc.Input(
                        id="profil_heatmap_min",
                        type="number",
                        placeholder="minimum value",
                        value=None,
                    ),
                    html.Label("Colorbar precision"),
                    dbc.Input(
                        id="profil_heatmap_precision",
                        type="number",
                        placeholder="Colorbar precision",
                        value=2,
                    ),
                    html.Label(""),
                    html.Br(),
                    dcc.RadioItems(
                        id="profil_heatmap_edit",
                        options=[
                            {"label": "Unfiltered", "value": "unfiltered"},
                            {"label": "Filtered", "value": "filter"},
                            {"label": "Edit mode", "value": "edit"},
                        ],
                        value="filter",
                        style={"display": "inline-block"},
                    ),
                ]),
            ]),
            dbc.CardFooter([])
    ], className="h-100 w-100")
    return card

def profil_top_middle_card():
    card = dbc.Card([
        dbc.CardHeader(html.H5(id="profil_path_box", children="Current File:")),
        dbc.CardBody([
            dbc.Row([
                dbc.Select(
                    id="profil_select_dataset",
                    options=[],
                    value=None,
                )
            ]),
            dbc.Row([
                html.H5(id="profil_text_box")
            ])
        ]),
        dbc.CardFooter([])
    ], className="h-100 w-100")

    return card

def profil_top_right_card():
    card = dbc.Card([
        dbc.CardHeader("Plot options"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([html.Label("Select mode"),
                        dbc.Select(id="profil_select_fit_mode", options=["Spot fitting", "Batch fitting", "Manual"],
                                   value="Spot fitting"),]),
                dbc.Col(id="profil_fit_inputs", children=[]),
                dbc.Col([dbc.Button(children="Go", id="profil_fit_button", className="long-item", n_clicks=0)]),
            ]),
            dbc.Row([
                html.Label("Plot Options"),
                html.Br(),
                dbc.Checklist(
                    id="profil_plot_select",
                    options=[{"label": "Adjusting Slope", "value": "adjusting_slope"},
                             {"label": "Profile Fits", "value": "fit_parameters"}],
                    value=["adjusting_slope", "profile_fits"],
                    style={"display": "inline-block"}
                )
            ])
        ]),
        dbc.CardFooter([])
    ], className="h-100 w-100"),

    return card

def profil_heatmap():
    card = dbc.Card([
        dbc.CardHeader(),
        dbc.CardBody([
            dcc.Graph(id="profil_heatmap")
        ]),
        dbc.CardFooter([])
    ], className="h-100 w-100")

    return card

def profil_plot():
    card = dbc.Card([
        dbc.CardHeader(),
        dbc.CardBody([
            dcc.Graph(id="profil_plot")
        ]),
        dbc.CardFooter([])
    ], className="h-100 w-100")

    return card

def profil_stores():
    stores = html.Div(
        children=[
            dcc.Store(id="profil_position_store", data=None),
            dcc.Store(id="profil_database_path_store", data=None),
            dcc.Store(id="profil_file_path_store", data=None),
            dcc.Store(id="profil_parameters_store", data=None),
            dcc.Store(id="profil_database_metadata_store", data=None)
        ])
    return stores

def make_profil_tab(upload_folder_root):
    profil_tab = dbc.Tab(
        id="profil",
        label="PROFIL",
        children=[html.Div(children=[
            dcc.Loading(
                id="loading-profil",
                type="default",
                delay_show=500,
                children=[
                    profil_stores(),
                    dbc.Row([
                        dbc.Col(profil_top_left_card(), width=4, className="d-flex flex-column"),
                        dbc.Col(profil_top_middle_card(), width=4, className="d-flex flex-column"),
                        dbc.Col(profil_top_right_card(), width=4, className="d-flex flex-column"),
                    ], className="mb-4 d-flex align-items-stretch"),
                    dbc.Row([
                        dbc.Col(profil_heatmap(), width=4, className="d-flex flex-column"),
                        dbc.Col(profil_plot(), width=8, className="d-flex flex-column"),
                    ], className="mb-4 d-flex align-items-stretch")
                ]
            )
        ])]
    )

    return profil_tab

