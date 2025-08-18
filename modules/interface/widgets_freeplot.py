"""
Class containing all Dash items and layout information for the freeplot tab
"""
from dash import html, dcc


class WidgetsFREEPLOT:
    def __init__(self):

        # Widget for the text box
        self.freeplot_center = (html.Div(
            className="textbox top-center",
            children=[
                html.Div(className="text-mid", children=[
                    html.Span(children="test", id="freeplot_text_box")
                ])
            ]))

        # Heatmap plot options
        self.freeplot_right = html.Div(className="subgrid top-right", children=[
            html.Div(
                className="subgrid-2",
                children=[
                    dcc.RadioItems(
                        id="freeplot_mode_select",
                        options=[
                            "measurement",
                            "results"
                        ],
                        value="Results",
                    ),
                ]
            ),
            html.Div(
                className="subgrid-4",
                children=[dcc.Dropdown(
                    id="freeplot_x_axis_dataset",
                    className="long-item",
                    options=[],
                    value=None,
                )
                ],
            ),
            html.Div(
                className="subgrid-7",
                children=[
                    html.Label("X axis"),
                    dcc.Dropdown(
                        id="freeplot_x_axis",
                        className="long-item",
                        options=[],
                        value=None,
                    ),
                ]
            ),
            html.Div(
                className="subgrid-5",
                children=[dcc.Dropdown(
                    id="freeplot_y_axis_dataset",
                    className="long-item",
                    options=[],
                    value=None,
                )
                ],
            ),
            html.Div(
                className="subgrid-8",
                children=[
                    html.Label("y axis"),
                    dcc.Dropdown(
                        id="freeplot_y_axis",
                        className="long-item",
                        options=[],
                        value=None,
                    ),
                ]
            ),
            html.Div(
                className="subgrid-9",
                children=[
                    html.Button(
                        id="freeplot_append_button",
                        className="long-item",
                        children="Append",
                        n_clicks=0,
                    ),
                    html.Button(
                        id="freeplot_replace_button",
                        className="long-item",
                        children="Replace",
                        n_clicks=0,
                    )

                ]
            )
        ])

        # Widget for fitting parameters and buttons
        self.freeplot_left = html.Div(className="subgrid top-left", children=[

        ])

        # EDX spectra graph that will be modified by user interaction
        self.freeplot_plot = html.Div(
            [dcc.Graph(id="freeplot_plot")], className="plot-right"
        )

        # EDX heatmap
        self.freeplot_heatmap = html.Div(
            [dcc.Graph(id="freeplot_heatmap")], className="plot-left"
        )

        # Stored variables
        self.freeplot_stores = html.Div(children=[
            dcc.Store(id="freeplot_position_store", data=(0, 0)),
            dcc.Store(id="freeplot_database_path_store", data=None),
            dcc.Store(id="freeplot_file_path_store", data=None),
            dcc.Store(id="freeplot_parameters_store", data=None),
            dcc.Store(id="freeplot_database_metadata_store", data=None)
        ])



    def make_tab_from_widgets(self):
        freeplot_tab = dcc.Tab(
            id="freeplot",
            label="FREEPLOT",
            value="freeplot",
            children=[html.Div(children=[
                dcc.Loading(
                    id="loading-freeplot",
                    type="default",
                    delay_show=500,
                    children=[
                        html.Div(
                            [
                                self.freeplot_left,
                                self.freeplot_center,
                                self.freeplot_right,
                                self.freeplot_heatmap,
                                self.freeplot_plot,
                                self.freeplot_stores
                            ],
                            className="grid-container",
                        )
                    ]
                )
            ])]
        )

        return freeplot_tab

