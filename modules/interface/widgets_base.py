from dash import html, dcc
import dash_bootstrap_components as dbc
import os

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
    widget = [
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
                            width=8,
                            style={"position": "relative"},
                        ),
                    ]
                )
            )
        ]),
        dbc.ModalFooter([
            dbc.Button("Return", id="return-btn", color="success"),
            dbc.Button("Cancel", id="close-btn", color="secondary")
        ])
    ]
    return widget