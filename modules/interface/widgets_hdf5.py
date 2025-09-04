import dash_uploader as du
from dash import html, dcc
from datetime import datetime


class WidgetsHDF5:

    def __init__(self, upload_folder_root):
        self.upload_folder_root = upload_folder_root

        # Widget for the drag and drop
        self.hdf5_left = html.Div(
            className="card textbox top-1",
            children=[
                html.Div(
                    className="text-top",
                    children=[
                    du.Upload(
                        id="hdf5_upload",
                        text="Drag and Drop or click to browse",
                        filetypes=["zip", "h5", "hdf5", "HIS", "dat"],
                        upload_id="temp",
                    ),
                ]),
                html.Div(
                    className="text-mid",
                    id="hdf5_dataset_input",
                    children=[
                        html.Label("Dataset Name"),
                        dcc.Input(
                            id="hdf5_dataset_name",
                            className="long-item",
                            type="text",
                            placeholder="Dataset Name",
                            value=None
                        ),
                        dcc.Input(
                            id="hdf5_manual_1",
                            className="long-item",
                            style={'display': 'none'}
                        ),
                        dcc.Input(
                            id="hdf5_manual_2",
                            className="long-item",
                            style={'display': 'none'}
                        ),
                        dcc.Input(
                            id="hdf5_manual_3",
                            className="long-item",
                            style={'display': 'none'}
                        )
                    ]
                ),
                html.Div(
                    className="text-7",
                    children=[html.Button(id="hdf5_add_button", children="Add measurement", n_clicks=0)]
                ),
                html.Div(
                    className="text-9",
                    children=[dcc.Dropdown(className="long-item",
                                           id="hdf5_measurement_type",
                                           options=[
                                               "EDX",
                                                "PROFIL",
                                                "MOKE",
                                                "XRD",
                                                "ESRF",
                                                "XRD results",
                                                "Annealing",
                                                "Magnetron",
                                                "Triode",
                                                "SQUID"
                                            ],
                                           value=None)]
                )
            ],
        )

        # Widget for the center box (text box + database options)
        self.hdf5_center = html.Div(
            className="card textbox top-2",
            children=[
                html.Div(
                    className="text-top",
                    children=[html.Span(children="test", id="hdf5_path_box")],
                ),
                html.Div(
                    className="text-mid",
                    children=[html.Span(children="test", id="hdf5_text_box")],
                ),
                html.Div(
                    className="text-7",
                    children=[html.Button(id="hdf5_new", children="Create new HDF5", n_clicks=0)]
                ),
                html.Div(
                    className="text-8",
                    children=[html.Button(id="hdf5_update", children="Update HDF5 structure", n_clicks=0)]
                ),
                html.Div(
                    className="text-9",
                    children=[html.Button(id="hdf5_export", children="Export to CSV", n_clicks=0)]
                ),
            ],
        )

        # Widget for the right box (sample info)
        self.hdf5_right = html.Div(
            className="card subgrid top-3",
            children=[
                html.Div(
                    className="subgrid-1",
                    children=[
                        html.Label("Fabrication date dd/mm/yyyy"),
                        dcc.Input(
                            className="long-item",
                            id="hdf5_sample_date",
                            type="text",
                            placeholder="Fabrication date",
                            value=datetime.now().strftime("%d/%m/%Y")
                        ),
                        html.Label("Operator Name"),
                        dcc.Input(
                            className="long-item",
                            id="hdf5_sample_operator",
                            type="text",
                            placeholder="Operator name",
                            value="Batman"
                        ),
                        html.Label("Sample Name"),
                        dcc.Input(
                            className="long-item",
                            id="hdf5_sample_name",
                            type="text",
                            placeholder="Sample name"
                        ),
                    ]
                ),
                html.Div(
                    className="subgrid-3",
                    children=[
                            dcc.Dropdown(
                                className="long-item",
                                id="hdf5_layer_dropdown",
                                options=["New Layer"]
                            ),
                            dcc.Dropdown(
                                className="long-item",
                                id="hdf5_layer_info_dropdown",
                                options=[]
                            ),
                            dcc.Input(
                                className="long-item",
                                id="hdf5_layer_info_input",
                                type="text",
                                debounce=True,
                            ),
                            html.Button(
                                id="hdf5_layer_save_button",
                                children="Save",
                                n_clicks=0
                            )
                    ]
                )
            ]
        )

        self.hdf5_inventory = html.Div(
            className="hdf5-bottom-grid",
            children=[
                html.Div(
                    id="hdf5_deposition_info",
                    className="card split-6 row-1",
                    children = [
                        html.Div(
                            className="section-1",
                            children=["Deposition"]
                        ),
                        html.Div(
                            id="hdf5_deposition_state",
                            className="section-2",
                            children=["State"]
                        ),
                        html.Div(
                            id="hdf5_deposition_date",
                            className="section-3",
                            children=["Date"]
                        ),
                    ],
                ),
                html.Div(
                    id="hdf5_annealing_info",
                    className="card split-6 row-2",
                    children=[
                        html.Div(
                            className="section-1",
                            children=["Annealing"]
                        ),
                        html.Div(
                            id="hdf5_annealing_state",
                            className="section-2",
                            children=["State"]
                        ),
                        html.Div(
                            id="hdf5_date_date",
                            className="section-3",
                            children=["Date"]
                        ),
                    ],
                ),
                html.Div(
                    id="hdf5_edx_info",
                    className="card split-6 row-3",
                    children=[
                        html.Div(
                            className="section-1",
                            children=["EDX"]
                        ),
                        html.Div(
                            id="hdf5_edx_state",
                            className="section-2",
                            children=["State"]
                        ),
                        html.Div(
                            id="hdf5_edx_date",
                            className="section-3",
                            children=["Date"]
                        ),
                    ],
                ),
                html.Div(
                    id="hdf5_profil_info",
                    className="card split-6 row-4",
                    children=[
                        html.Div(
                            className="section-1",
                            children=["Profil"]
                        ),
                        html.Div(
                            id="hdf5_profil_state",
                            className="section-2",
                            children=["State"]
                        ),
                        html.Div(
                            id="hdf5_profil_date",
                            className="section-3",
                            children=["Date"]
                        ),
                    ],
                ),
                html.Div(
                    id="hdf5_moke_info",
                    className="card split-6 row-5",
                    children=[
                        html.Div(
                            className="section-1",
                            children=["Moke"]
                        ),
                        html.Div(
                            id="hdf5_moke_state",
                            className="section-2",
                            children=["State"]
                        ),
                        html.Div(
                            id="hdf5_moke_date",
                            className="section-3",
                            children=["Date"]
                        ),
                    ],
                ),
                html.Div(
                    id="hdf5_xrd_info",
                    className="card split-6 row-6",
                    children=[
                        html.Div(
                            className="section-1",
                            children=["XRD"]
                        ),
                        html.Div(
                            id="hdf5_xrd_state",
                            className="section-2",
                            children=["State"]
                        ),
                        html.Div(
                            id="hdf5_xrd_date",
                            className="section-3",
                            children=["Date"]
                        ),
                    ],
                ),
                html.Div(
                    id="hdf5_misc_info",
                    className="card split-6 row-7",
                    children=[
                        html.Div(
                            className="section-1",
                            children=["Misc"]
                        ),
                    ],
                ),
            ]
        )

        # Stored variables
        self.hdf5_stores = html.Div(
            children=[
                dcc.Store(id="hdf5_upload_folder_root", data=upload_folder_root),
                dcc.Store(id="hdf5_upload_folder_path", data=None),
                dcc.Store(id="sample_structure_store", data=None),
            ]
        )


    def make_tab_from_widgets(self):
        hdf5_tab = dcc.Tab(
            id="hdf5",
            label="HDF5",
            value="hdf5",
            children=[html.Div(children=[
                dcc.Loading(
                    id="loading-hdf5",
                    type="default",
                    delay_show=500,
                    children=[
                        html.Div(
                            className="hdf5-page",
                            children = [
                                html.Div(
                                    className="hdf5-top-grid",
                                    children = [
                                        self.hdf5_left,
                                        self.hdf5_center,
                                        self.hdf5_right,
                                    ]
                                ),
                                self.hdf5_inventory,
                                self.hdf5_stores,
                            ],
                        )
                    ]
                )
            ])]
        )

        return hdf5_tab