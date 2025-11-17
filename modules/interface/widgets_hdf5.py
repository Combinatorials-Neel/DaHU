import dash_uploader as du
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
from datetime import datetime


def top_left_card():
    card = dbc.Card([
            dbc.CardHeader(
                dbc.Row([
                    dbc.Col("Add datasets"),
                    dbc.Col([
                        daq.BooleanSwitch(
                            id = "hdf5_upload_mode_toggle",
                            on = False,
                            label="Upload mode",
                            persistence=False
                        ),
                    ])
                ]),
            ),
            dbc.CardBody([
                html.Div(
                    id="hdf5_upload_div",
                    children=[
                        du.Upload(
                            id="hdf5_upload",
                            text="Upload a file. Drag and Drop or click to browse",
                            filetypes=["zip", "h5", "hdf5", "HIS", "dat", "jpg", "jpeg", "png"],
                            upload_id="temp",
                        ),
                    ],
                    style={"display": "none"}
                ),
                html.Div(
                    id="hdf5_select_div",
                    children=[
                        html.Div(id="hdf5_select",
                                 children="Select a file or folder. Click to browse"),
                    ],
                    className="module-box"),
                html.Div(
                    id="hdf5_dataset_input",
                    children=[
                        html.Label("Dataset Name"),
                        dbc.Input(
                            id="hdf5_dataset_name",
                            type="text",
                            placeholder="Dataset Name",
                            value=None
                        ),
                        dbc.Input(
                            id="hdf5_manual_1",
                            style={'display': 'none'}
                        ),
                        dbc.Input(
                            id="hdf5_manual_2",
                            style={'display': 'none'}
                        ),
                        dbc.Input(
                            id="hdf5_manual_3",
                            style={'display': 'none'}
                        ),
                    ]
                )
            ]),
            dbc.CardFooter([
                dbc.Container([
                    dbc.Row([
                        dbc.Col(
                            dbc.Button(id="hdf5_add_button", children="Add measurement", n_clicks=0),
                            width=3
                        ),
                        dbc.Col(
                            dbc.Select(id="hdf5_measurement_type",
                                       options=[
                                           "EDX", "PROFIL", "MOKE", "XRD", "ESRF", "XRD results", "Annealing",
                                           "Magnetron", "Triode", "SQUID", "Picture", "HT hdf5"],
                                       value=None),
                            width=9
                        )
                    ])
                ], fluid=True),
            ])
        ], className="h-100")
    return card

def top_middle_card():
    card = dbc.Card([
        dbc.CardHeader(html.H5(id="hdf5_path_box", children="Current File:", n_clicks=0)),
        dbc.CardBody([
            html.H5(id="hdf5_text_box")
        ]),
        dbc.CardFooter([
            dbc.ButtonGroup([
                dbc.Button(id="hdf5_update", children="Update HDF5", n_clicks=0),
                dbc.Button(id="hdf5_export", children="Export to CSV", n_clicks=0),
                dbc.Button(id="hdf5_new_file_button", children="Create new HDF5", n_clicks=0),
            ], className="w-100")
        ])
    ], className="h-100")
    return card

def top_right_card():
    card = dbc.Card([
        dbc.CardHeader(),
        dbc.CardBody([])
    ], className="h-100")

    return card

def layer_stack_card():
    card = dbc.Card([
        dbc.CardHeader([
            html.H5(children="Wafer layer structure")
        ]),
        dbc.CardBody([

        ]),
        dbc.CardFooter([
            dbc.Button(id="layer_card_open_button", children="Edit", color="primary", n_clicks=0),
        ])
    ])

    return card

def hdf5_stores(upload_folder_root):
    stores = html.Div(
        children=[
            dcc.Store(id="hdf5_upload_folder_path", data=None),
            dcc.Store(id="hdf5_upload_folder_root", data=upload_folder_root),
            dcc.Store(id="hdf5_layer_count_store", data=None),
        ]
    )
    return stores

def make_hdf5_tab(upload_folder_root):
    hdf5_tab = dbc.Tab(
        id="hdf5",
        label="HDF5",
        children=[html.Div(children=[
            dcc.Loading(
                id="loading-hdf5",
                type="default",
                delay_show=500,
                children=[
                    dbc.Row([
                        dbc.Col(top_left_card(), width=4, className="d-flex flex-column"),
                        dbc.Col(top_middle_card(), width=4, className="d-flex flex-column"),
                        dbc.Col(top_right_card(), width=4, className="d-flex flex-column"),
                    ], className="align-items-stretch"),
                    dbc.Row([
                        dbc.Col(layer_stack_card(), width=4, className="ms-auto")
                    ]),
                    hdf5_stores(upload_folder_root)
                ]
            )
        ])]
    )

    return hdf5_tab




