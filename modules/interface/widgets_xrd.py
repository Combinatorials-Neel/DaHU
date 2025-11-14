"""
Class containing all Dash items and layout information for the XRD tab
"""

from dash import html, dcc
import dash_bootstrap_components as dbc

def xrd_top_left_card():
    card = dbc.Card([
            dbc.CardHeader("Heatmap Options"),
            dbc.CardBody([
                html.Label("Currently plotting:"),
                html.Br(),
                dbc.Row([
                    dbc.Col(
                        dbc.Select(
                            id="xrd_heatmap_select",
                            options=[],
                            placeholder="Select property",
                        ),
                    ),
                    dbc.Col(
                        dbc.Checkbox(
                            id="xrd_analysis_toggle",
                            label="analysis mode",
                            value=False,
                            className="form-check-reverse"
                        )
                    )
                ]),
                dbc.Row([
                    html.Label("Colorbar bounds"),
                    dbc.Input(
                        id="xrd_heatmap_max",
                        type="number",
                        placeholder="maximum value",
                        value=None,
                    ),
                    dbc.Input(
                        id="xrd_heatmap_min",
                        type="number",
                        placeholder="minimum value",
                        value=None,
                    ),
                    html.Label("Colorbar precision"),
                    dbc.Input(
                        id="xrd_heatmap_precision",
                        type="number",
                        placeholder="Colorbar precision",
                        value=2,
                    ),
                    html.Label(""),
                    html.Br(),
                    dcc.RadioItems(
                        id="xrd_heatmap_edit",
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

def xrd_top_middle_card():
    card = dbc.Card([
        dbc.CardHeader(
            dbc.Row([
                dbc.Col([
                    html.H5(id="xrd_path_box", children="Initializing")
                ], width=10),
                dbc.Col([
                    dbc.Checkbox(
                        id="xrd_isolate_toggle",
                        label="isolate tab",
                        value=False,
                        className="form-check-reverse"
                    )
                ], width=2)
            ])
        ),
        dbc.CardBody([
            dbc.Row([
                dbc.Select(
                    id="xrd_select_dataset",
                    options=[],
                    value=None,
                )
            ]),
            dbc.Row([
                html.H5(id="xrd_text_box")
            ])
        ]),
        dbc.CardFooter([
            dbc.Button(id="xrd_export_button", children="Export for fitting", n_clicks=0),
            dbc.Button(id="xrd_pyfai_button", children="Re-integrate", n_clicks=0),
        ])
    ], className="h-100 w-100")

    return card

def xrd_top_right_card():
    card = dbc.Card([
        dbc.CardHeader("Plot options"),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.RadioItems(
                    id="xrd_plot_select",
                    options=[
                        {"label": "Image", "value": "image"},
                        {"label": "Integrated", "value": "integrated"},
                        {"label": "Fitted", "value": "fitted"},
                    ],
                    value="image"
                )]),
                dbc.Col([
                    dcc.Dropdown(
                    id="xrd_fits_select",
                    options=[],
                    multi=True
                    )
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Label("Image colorbar bounds"),
                    dbc.Input(id="xrd_image_max", type="number", placeholder="maximum value",
                              value=None),
                    dbc.Input(id="xrd_image_min", type="number", placeholder="minimum value",
                              value=None)
                ], width=4)
            ])
        ]),
        dbc.CardFooter([])
    ], className="h-100 w-100"),

    return card

def xrd_heatmap():
    card = dbc.Card([
        dbc.CardHeader(),
        dbc.CardBody([
            dcc.Graph(id="xrd_heatmap")
        ]),
        dbc.CardFooter([])
    ], className="h-100 w-100")

    return card

def xrd_plot():
    card = dbc.Card([
        dbc.CardHeader(
            dbc.Row([
                dbc.Col(
                    dbc.Checkbox(
                        id="xrd_plot_append_toggle",
                        label="append mode",
                        value=False,
                        className="form-check-reverse"
                    )
                )
            ])
        ),
        dbc.CardBody([
            dcc.Graph(id="xrd_plot")
        ]),
        dbc.CardFooter([])
    ], className="h-100 w-100")

    return card

def xrd_stores():
    stores = html.Div(
        children=[
            dcc.Store(id="xrd_position_store", data=None),
            dcc.Store(id="xrd_path_store", data=None),
            dcc.Store(id="xrd_current_path_store", data=None),
            dcc.Store(id="xrd_results_store", data=None),
            dcc.Store(id="xrd_nexus_mode_store", data=False)
        ]
    )
    return stores

def widget_xrd_integrate_modal():
    widget = dbc.Modal(
        id="pyfai_popup",
        is_open=False,
        centered=True,
        size="s",
        children=[
            dbc.ModalHeader(["Re-integrate with PyFAI"]),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col(children=[
                        dbc.Select(
                            id="pyfai_poni_select",
                            options=["esrf1", "esrf2", "esrf3"]
                        )
                    ], width=8)
                ]),
                dbc.Row([
                    dbc.Col([
                        html.Label("Function"),
                        dbc.Select(
                            id="pyfai_function_select",
                            options=["integrate1d", "medfilt1d"]
                        )
                    ]),
                ]),
                dbc.Row([
                    dbc.Col(children=[
                        html.Label("Number of points"),
                        dbc.Input(
                            id="pyfai_points",
                            type="number"
                        ),
                    ])
                ])
            ]),
            dbc.ModalFooter([
                dbc.Button(id="pyfai_integrate_button", children="Integrate", color="success", n_clicks=0),
            ])
        ]
    )
    return widget

def make_xrd_tab(upload_folder_root):
    xrd_tab = dbc.Tab(
        id="xrd",
        label="XRD",
        children=[html.Div(children=[
            dcc.Loading(
                id="loading-xrd",
                type="default",
                delay_show=500,
                children=[
                    xrd_stores(),
                    widget_xrd_integrate_modal(),
                    dbc.Row([
                        dbc.Col(xrd_top_left_card(), width=4, className="d-flex flex-column"),
                        dbc.Col(xrd_top_middle_card(), width=4, className="d-flex flex-column"),
                        dbc.Col(xrd_top_right_card(), width=4, className="d-flex flex-column"),
                    ], className="mb-4 d-flex align-items-stretch"),
                    dbc.Row([
                        dbc.Col(xrd_heatmap(), width=5, className="d-flex flex-column"),
                        dbc.Col(xrd_plot(), width=7, className="d-flex flex-column"),
                    ], className="mb-4 d-flex align-items-stretch")
                ]
            )
        ])]
    )

    return xrd_tab
