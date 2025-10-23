from dash import html, dcc
import dash_bootstrap_components as dbc

def edx_top_left_card():
    card = dbc.Card([
            dbc.CardHeader("Heatmap Options"),
            dbc.CardBody([
                html.Label("Currently plotting:"),
                html.Br(),
                dbc.Select(
                    id="edx_heatmap_select",
                    options=[],
                    placeholder="Select Element",
                ),
                dbc.Row([
                    html.Label("Colorbar bounds"),
                    dbc.Input(
                        id="edx_heatmap_max",
                        type="number",
                        placeholder="maximum value",
                        value=None,
                    ),
                    dbc.Input(
                        id="edx_heatmap_min",
                        type="number",
                        placeholder="minimum value",
                        value=None,
                    ),
                    html.Label("Colorbar precision"),
                    dbc.Input(
                        id="edx_heatmap_precision",
                        type="number",
                        placeholder="Colorbar precision",
                        value=2,
                    ),
                    html.Label(""),
                    html.Br(),
                    dcc.RadioItems(
                        id="edx_heatmap_edit",
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

def edx_top_middle_card():
    card = dbc.Card([
        dbc.CardHeader(html.H5(id="edx_path_box", children="Current File:")),
        dbc.CardBody([
            dbc.Row([
                dbc.Select(
                    id="edx_select_dataset",
                    options=[],
                    value=None,
                )
            ]),
            dbc.Row([
                html.H5(id="edx_text_box")
            ])
        ]),
        dbc.CardFooter([])
    ], className="h-100 w-100")

    return card

def edx_top_right_card():
    card = dbc.Card([
        dbc.CardHeader(),
        dbc.CardBody([
        ]),
        dbc.CardFooter([])
    ], className="h-100 w-100"),

    return card

def edx_heatmap():
    card = dbc.Card([
        dbc.CardHeader(),
        dbc.CardBody([
            dcc.Graph(id="edx_heatmap")
        ]),
        dbc.CardFooter([])
    ], className="h-100 w-100")

    return card

def edx_plot():
    card = dbc.Card([
        dbc.CardHeader(),
        dbc.CardBody([
            dcc.Graph(id="edx_plot")
        ]),
        dbc.CardFooter([])
    ], className="h-100 w-100")

    return card

def edx_stores():
    stores = html.Div(
        children=[
            dcc.Store(id="edx_position_store"),
            dcc.Store(id="edx_parameters_store"),
        ])
    return stores

def make_edx_tab(upload_folder_root):
    edx_tab = dbc.Tab(
        id="edx",
        label="EDX",
        children=[html.Div(children=[
            dcc.Loading(
                id="loading-edx",
                type="default",
                delay_show=500,
                children=[
                    edx_stores(),
                    dbc.Row([
                        dbc.Col(edx_top_left_card(), width=4, className="d-flex flex-column"),
                        dbc.Col(edx_top_middle_card(), width=4, className="d-flex flex-column"),
                        dbc.Col(edx_top_right_card(), width=4, className="d-flex flex-column"),
                    ], className="mb-4 d-flex align-items-stretch"),
                    dbc.Row([
                        dbc.Col(edx_heatmap(), width=4, className="d-flex flex-column"),
                        dbc.Col(edx_plot(), width=8, className="d-flex flex-column"),
                    ], className="mb-4 d-flex align-items-stretch")
                ]
            )
        ])]
    )

    return edx_tab




