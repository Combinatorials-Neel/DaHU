from dash import html, dcc
import dash_bootstrap_components as dbc
import os
from datetime import datetime
import dash_uploader as du

def widget_title_card(title):
    widget = html.Div(
        className="section-1",
        children=[title]
    )
    return widget

def widget_measurement_missing():
    widget = html.Div(
        id="hdf5_deposition_state",
        className="section-2",
        children=["Missing measurement"],
        style = {
            "background-color": "#993D3D",
        }
    )
    return widget

def widget_manual_data(number):
    widget = html.Div(
        id="hdf5_deposition_state",
        className="section-2",
        children=[
            html.Div(f"{number} manual entries")
        ],
        style={
            "background-color": "#3D9499",
        }
    )
    return widget


def widget_measurement_found(number):
    widget = html.Div(
        id="hdf5_deposition_state",
        className="section-2",
        children=[
            html.Div(f"{number} measurements")
        ],
        style = {
            "background-color": "#3D994C",
        }
    )
    return widget


def widget_browser_modal():
    widget = dbc.Modal(
        id="browser_popup",
        is_open=False,
        centered=True,
        size="xl",
        children=[
        dbc.ModalHeader("Browser"),
        dbc.ModalBody([
            html.Div(
                dbc.Row(
                    [
                        dbc.Col(lg=1, sm=1, md=1),
                        dbc.Col(
                            [
                                dcc.Store(id="stored_cwd", data=os.getcwd()),
                                html.Hr(),
                                html.Br(),
                                html.H4(
                                    html.B(
                                        html.A(
                                            "⬆️ Parent directory",
                                            href="#",
                                            id="parent_dir",
                                        )
                                    )
                                ),
                                html.H3([html.Code(os.getcwd(), id="cwd")]),
                                html.Br(),
                                html.Br(),
                                html.Div(
                                    id="cwd_files",
                                    style={"height": 500, "overflow": "scroll"},
                                )
                            ],
                            width=12,
                            style={"position": "relative"},
                        ),
                    ]
                )
            )
        ]),
        dbc.ModalFooter([
            dbc.Button("Select", id="browser_select_button", color="success"),
        ])
    ])
    return widget

def widget_layer_modal():
    widget = dbc.Modal(
        id="layer_editor_popup",
        is_open=False,
        centered=True,
        size="m",
        children=[
        dbc.ModalHeader("Layer editor"),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Select(id="layer_editor_type", options=["buffer", "active", "capping"])
                ], width=8),
                dbc.Col([
                    dbc.Row(children=[
                        dbc.Col(html.Label("Position")),
                        dbc.Col(dbc.Input(id="layer_editor_index", type="number", value=0, min=1, step=1))
                    ], className="align-items-center mb-2")
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Row(children=[
                        dbc.Col(html.Label("Element")),
                        dbc.Col(dbc.Input(id="layer_editor_element", type="text", placeholder="Element"), width=6),
                        dbc.Col(html.Label(""))
                    ], className="align-items-center mb-2"),
                    dbc.Row(children=[
                        dbc.Col(html.Label("Time")),
                        dbc.Col(dbc.Input(id="layer_editor_time", type="number", placeholder="Time (s)"), width=6),
                        dbc.Col(html.Label("(s)"))
                    ], className="align-items-center mb-2"),
                    dbc.Row(children=[
                        dbc.Col(html.Label("Thickness")),
                        dbc.Col(dbc.Input(id="layer_editor_thickness", type="number", placeholder="Thickness (nm)"), width=6),
                        dbc.Col(html.Label("(nm)"))
                    ], className="align-items-center mb-2"),
                    dbc.Row(children=[
                        dbc.Col(html.Label("Temperature")),
                        dbc.Col(dbc.Input(id="layer_editor_temperature", type="number", placeholder="Temperature (°C)"), width=6),
                        dbc.Col(html.Label("°C"))
                    ], className="align-items-center mb-2"),
                    dbc.Row(children=[
                        dbc.Col(html.Label("Power")),
                        dbc.Col(dbc.Input(id="layer_editor_power", type="number", placeholder="Power (W)"), width=6),
                        dbc.Col(html.Label("(W)"))
                    ], className="align-items-center mb-2"),
                    dbc.Row(children=[
                        dbc.Col(html.Label("Distance")),
                        dbc.Col(dbc.Input(id="layer_editor_distance", type="number", placeholder="Distance (mm)"), width=6),
                        dbc.Col(html.Label("(mm)"))
                    ], className="align-items-center mb-2"),
                    dbc.Row(children=[
                        dbc.Col(html.Label("Angle")),
                        dbc.Col(dbc.Input(id="layer_editor_angle", type="number", placeholder="Angle (deg)"), width=6),
                        dbc.Col(html.Label("(deg)"))
                    ], className="align-items-center mb-2"),
                    dbc.Row(children=[
                        dbc.Col(html.Label("Comment")),
                        dbc.Col(dbc.Input(id="layer_editor_comment", type="text", placeholder="User comment"), width=9),
                    ], className="align-items-center mb-2"),
                ])
            ])
        ]),
        dbc.ModalFooter([
            dbc.Row([
                dbc.Col([
                    dbc.Button(id="layer_editor_save_button", children="Save", color="success", n_clicks=0),
                ], className="d-flex ms_auto")
            ])
        ])
    ])

    return widget

def widget_new_hdf5_modal():
    widget = dbc.Modal(
        id="new_hdf5_popup",
        is_open=False,
        centered=True,
        size="s",
        children=[
            dbc.ModalHeader(["Create new HDF5"]),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col(children=[
                        dbc.Select(
                            id="new_hdf5_type",
                            options=["Library", "Dataset"]
                        )
                    ], width=8),
                    dbc.Col(children=[
                        dbc.Select(
                            id="new_hdf5_instrument",
                            options=["Magnetron", "Triode"]
                        )
                    ], width=4)
                ]),
                dbc.Row([
                    dbc.Col([
                        html.Label("Sample Name"),
                        dbc.Input(
                            id="new_hdf5_name",
                            type="text",
                            placeholder="Sample name"
                        )
                    ]),
                ]),
                dbc.Row([
                    dbc.Col(children=[
                        html.Label("Fabrication date dd/mm/yyyy"),
                        dbc.Input(
                            id="new_hdf5_date",
                            type="text",
                            placeholder="Fabrication date",
                            value=datetime.now().strftime("%d/%m/%Y")
                        ),
                    ]),
                    dbc.Col([
                        html.Label("Operator"),
                        dbc.Input(
                            id="new_hdf5_operator",
                            type="text",
                            placeholder="Operator name",
                            value="Batman"
                        ),
                    ])
                ])
            ]),
            dbc.ModalFooter([
                dbc.Button(id="new_hdf5_create_button", children="Create", color="success", n_clicks=0),
            ])
        ]
    )
    return widget


def widget_layer_card():
    widget = dbc.Card([
        dbc.CardHeader(html.H5("Current layers")),
        dbc.CardBody([

        ]),
        dbc.CardFooter([
            dbc.Col([

            ])
        ])
    ])
    return widget