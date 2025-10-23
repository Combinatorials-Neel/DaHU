import dash_uploader as du
from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import datetime

def top_left_card():
    card = dbc.Card([
            dbc.CardHeader("Add datasets"),
            dbc.CardBody([
                du.Upload(
                    id="hdf5_upload",
                    text="Drag and Drop or click to browse",
                    filetypes=["zip", "h5", "hdf5", "HIS", "dat", "jpg", "jpeg", "png"],
                    upload_id="temp",
                ),
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
        dbc.CardHeader(html.H5(id="hdf5_path_box", children="Current File:")),
        dbc.CardBody([
            html.H5(id="hdf5_text_box")
        ]),
        dbc.CardFooter([
            dbc.ButtonGroup([
                dbc.Button(id="hdf5_update", children="Update HDF5", n_clicks=0),
                dbc.Button(id="hdf5_export", children="Export to CSV", n_clicks=0),
                dbc.Button(id="test_button", children="Test", n_clicks=0),
            ], className="w-100")
        ])
    ], className="h-100")
    return card

def top_right_card():
    card = dbc.Card([
        dbc.CardHeader(),
        dbc.CardBody([
            dbc.Col([
                html.Label("Fabrication date dd/mm/yyyy"),
                dbc.Input(
                    id="hdf5_sample_date",
                    type="text",
                    placeholder="Fabrication date",
                    value=datetime.now().strftime("%d/%m/%Y")
                ),
                html.Label("Operator Name"),
                dbc.Input(
                    id="hdf5_sample_operator",
                    type="text",
                    placeholder="Operator name",
                    value="Batman"
                ),
                html.Label("Sample Name"),
                dbc.Input(
                    id="hdf5_sample_name",
                    type="text",
                    placeholder="Sample name"
                )
            ], width=6),
            dbc.Col([
                dbc.Select(
                    id="hdf5_layer_dropdown",
                    options=["New Layer"]
                ),
                dbc.Select(
                    id="hdf5_layer_info_dropdown",
                    options=[]
                ),
                dbc.Input(
                    id="hdf5_layer_info_input",
                    type="text",
                    debounce=True,
                ),
                dbc.Button(
                    id="hdf5_layer_save_button",
                    children="Save",
                    n_clicks=0
                )
            ])
        ])
    ], className="h-100")

    return card


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
                        dbc.Col(top_left_card(), width=4, className="h-100"),
                        dbc.Col(top_middle_card(), width=4, className="h-100"),
                        dbc.Col(top_right_card(), width=4, className="h-100"),
                    ], className="align-items-stretch"),
                ]
            )
        ])]
    )

    return hdf5_tab




