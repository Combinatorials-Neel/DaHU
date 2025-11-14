"""
Class containing all Dash items and layout information for the MOKE tab
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq

def moke_top_left_card():
    card = dbc.Card([
            dbc.CardHeader("Heatmap Options"),
            dbc.CardBody([
                html.Label("Currently plotting:"),
                html.Br(),
                dbc.Select(
                    id="moke_heatmap_select",
                    options=[],
                    placeholder="Select property",
                ),
                dbc.Row([
                    html.Label("Colorbar bounds"),
                    dbc.Input(
                        id="moke_heatmap_max",
                        type="number",
                        placeholder="maximum value",
                        value=None,
                    ),
                    dbc.Input(
                        id="moke_heatmap_min",
                        type="number",
                        placeholder="minimum value",
                        value=None,
                    ),
                    html.Label("Colorbar precision"),
                    dbc.Input(
                        id="moke_heatmap_precision",
                        type="number",
                        placeholder="Colorbar precision",
                        value=2,
                    ),
                    html.Label(""),
                    html.Br(),
                    dcc.RadioItems(
                        id="moke_heatmap_edit",
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

def moke_top_middle_card():
    card = dbc.Card([
        dbc.CardHeader(html.H5(id="moke_path_box", children="Current File:")),
        dbc.CardBody([
            dbc.Row([
                dbc.Select(
                    id="moke_select_dataset",
                    options=[],
                    value=None,
                )
            ]),
            dbc.Row([
                html.H5(id="moke_text_box")
            ])
        ]),
        dbc.CardFooter([])
    ], className="h-100 w-100")

    return card

def moke_top_right_card():
    card = dbc.Card([
        dbc.CardHeader("Plot options"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([dbc.Select(id="moke_plot_dropdown")])
            ]),
            dbc.Row([
                dbc.Col([
                        html.Label("Coil Factor (T/100V)"),
                        dbc.Input(
                            className="long-item",
                            id="moke_coil_factor",
                            type="number",
                            min=0,
                            step=0.00001,
                        ),
                    ]),
                dbc.Col([
                    html.Label("Smoothing Polyorder"),
                    dbc.Input(
                        id="moke_smoothing_polyorder",
                        type="number",
                        min=0,
                        step=1,
                    ),
                ]),
                dbc.Col([
                    html.Label("Smoothing Range"),
                    dbc.Input(
                        id="moke_smoothing_range",
                        type="number",
                        min=0,
                        step=1,
                    ),
                ]),
                dbc.Col([
                    dbc.Button(
                        id="moke_make_database_button",
                        children="Make database!",
                        n_clicks=0,
                    )
                ])
            ], align="end"),
            dbc.Row([
                dbc.Col([
                    html.Label("Plot Options"),
                    html.Br(),
                    dbc.RadioItems(
                        id="moke_plot_select",
                        options=[
                            {"label": "Oscilloscope Data", "value": "oscilloscope"},
                            {"label": "M(H) Loop", "value": "loop"},
                            {"label": "M(H) Loop + Stored Result", "value": "stored_result"},
                            {"label": "M(H) Loop + Live Result", "value": "live_result"},
                        ],
                        value="loop",
                        style={"display": "inline-block"},
                    )
                ]),
                dbc.Col([
                    dbc.Checklist(
                        id="moke_data_treatment_checklist",
                        options=[
                            {"label": "Smoothing", "value": "smoothing"},
                            {"label": "Correct offset", "value": "correct_offset"},
                            {"label": "Low field filter", "value": "filter_zero"},
                            {"label": "Connect loops", "value": "connect_loops"},
                            {"label": "Shift loops", "value": "shift_loops"},
                        ],
                        value=[
                            "smoothing",
                            "correct_offset",
                            "filter_zero",
                            "connect_loops",
                        ],
                    )
                ])
            ])
        ]),
        dbc.CardFooter([])
    ], className="h-100 w-100"),

    return card

def moke_heatmap():
    card = dbc.Card([
        dbc.CardHeader(),
        dbc.CardBody([
            dcc.Graph(id="moke_heatmap")
        ]),
        dbc.CardFooter([])
    ], className="h-100 w-100")

    return card

def moke_plot():
    card = dbc.Card([
        dbc.CardHeader(),
        dbc.CardBody([
            dcc.Graph(id="moke_plot")
        ]),
        dbc.CardFooter([])
    ], className="h-100 w-100")

    return card

def moke_loop_map():
    card = dbc.Card([
        dbc.CardHeader(),
        dbc.CardBody([
            dcc.Graph(id="moke_loops_figure")
        ]),
        dbc.CardFooter([])
    ], className="h-100 w-100")

    return card

def moke_loop_map_options():
    card = dbc.Card([
        dbc.CardHeader(),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Button(
                        id="moke_loops_make_button",
                        children="Make loop map!",
                        n_clicks=0,
                        color="success"
                    )
                ], width=10),
                dbc.Col([
                    daq.BooleanSwitch(
                        id="moke_loops_normalize",
                        on=False,
                        label="Normalize",
                        persistence=False
                    )
                ], width=2)
            ])
        ]),
        dbc.CardFooter([])
    ])

    return card

def moke_stores():
    stores = html.Div(
        children=[
            dcc.Store(id="moke_position_store", data=None),
            dcc.Store(id="moke_database_path_store", data=None),
            dcc.Store(id="moke_results_store", data=None),
            dcc.Store(id="moke_data_treatment_store", data=None),
        ]
    )
    return stores

def make_moke_tab(upload_folder_root):
    moke_tab = dbc.Tab(
        id="moke",
        label="MOKE",
        children=[
            moke_stores(),
            html.Div(
                children=[
                    dbc.Tabs(
                        id="moke_subtabs",
                        active_tab="moke_main",
                        children=[
                            dbc.Tab(
                                id="moke_main",
                                label="Main",
                                children=[
                                    dcc.Loading(
                                        id="loading_main_moke",
                                        type="default",
                                        delay_show=500,
                                        children=[
                                            dbc.Row([
                                                dbc.Col(moke_top_left_card(), width=4, className="d-flex flex-column"),
                                                dbc.Col(moke_top_middle_card(), width=4,
                                                        className="d-flex flex-column"),
                                                dbc.Col(moke_top_right_card(), width=4, className="d-flex flex-column"),
                                            ], className="mb-4 d-flex align-items-stretch"),
                                            dbc.Row([
                                                dbc.Col(moke_heatmap(), width=4, className="d-flex flex-column"),
                                                dbc.Col(moke_plot(), width=8, className="d-flex flex-column"),
                                            ], className="mb-4 d-flex align-items-stretch")
                                        ]
                                    )
                                ]
                            ),
                            dbc.Tab(
                                id="moke_loop",
                                label="Loop map",
                                children=[
                                    dcc.Loading(
                                        id="loading_loop_moke",
                                        type="default",
                                        delay_show=500,
                                        children=[
                                            html.Div(
                                                children=[
                                                    dbc.Row([
                                                        dbc.Col(moke_loop_map(), width=8, className="d-flex flex-column"),
                                                        dbc.Col(moke_loop_map_options(), width=4, className="d-flex flex-column"),
                                                    ])
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

    return moke_tab

