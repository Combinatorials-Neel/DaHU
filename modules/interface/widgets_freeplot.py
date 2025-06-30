"""
Class containing all Dash items and layout information for the freeplot tab
"""
from dash import html, dcc


class WidgetsPROFIL:
    def __init__(self):

        # Widget for the text box
        self.freeplot_center = (html.Div(
            className="textbox top-center",
            children=[
                html.Div(
                    className="text-top",
                    children=[dcc.Dropdown(
                        id="freeplot_select_dataset",
                        className="long-item",
                        options=[],
                        value=None,
                    )
                    ],
                ),

                html.Div(className="text-mid", children=[
                    html.Span(children="test", id="freeplot_text_box")
                ])
            ]))

        # Heatmap plot options
        self.freeplot_left = html.Div(className="subgrid top-left", children=[
            html.Div(className="subgrid-2", children=[
                html.Label("Currently plotting:"),
                html.Br(),
                dcc.Dropdown(id="freeplot_heatmap_select", className="long-item", options=[])
            ]),
            html.Div(className="subgrid-7", children=[
                html.Label("Colorbar bounds"),
                dcc.Input(id="freeplot_heatmap_max", className="long-item", type="number", placeholder="maximum value",
                          value=None),
                dcc.Input(id="freeplot_heatmap_min", className="long-item", type="number", placeholder="minimum value",
                          value=None)
            ]),
            html.Div(
                className="subgrid-8",
                children=[
                    html.Label("Colorbar precision"),
                    dcc.Input(
                        id="freeplot_heatmap_precision",
                        className="long-item",
                        type="number",
                        placeholder="Colorbar precision",
                        value=1,
                    ),
                ]
            ),
            html.Div(className="subgrid-9", children=[
                html.Label(""),
                html.Br(),
                dcc.RadioItems(
                    id="freeplot_heatmap_edit",
                    options=[{"label": "Unfiltered", "value": "unfiltered"},
                             {"label": "Filtered", "value": "filter"},
                             {"label": "Edit mode", "value": "edit"}],
                    value="filter",
                    style={"display": "inline-block"}
                ),
            ])
        ])

        # Widget for fitting parameters and buttons
        self.freeplot_right = html.Div(className="subgrid top-right", children=[
            html.Div(className="subgrid-1", children=[
                html.Label("Select mode"),
                dcc.Dropdown(id="freeplot_select_fit_mode", className="long-item",
                             options=["Spot fitting", "Batch fitting", "Manual"], value="Spot fitting")
            ]),

            html.Div(className="subgrid-2", id="freeplot_fit_inputs", children=[

            ]),

            html.Div(
                className="subgrid-3", children=[
                    html.Button(children="Go", id="freeplot_fit_button", className="long-item", n_clicks=0)
                ]
            ),

            html.Div(className="subgrid-9", children=[
                html.Label("Plot Options"),
                html.Br(),
                dcc.Checklist(
                    id="freeplot_plot_select",
                    options=[{"label": "Adjusting Slope", "value": "adjusting_slope"},
                             {"label": "Profile Fits", "value": "fit_parameters"}],
                    value=["adjusting_slope", "freeplote_fits"],
                    style={"display": "inline-block"}
                ),
            ])
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
            dcc.Store(id="freeplot_position_store", data=None),
            dcc.Store(id="freeplot_database_path_store", data=None),
            dcc.Store(id="freeplot_file_path_store", data=None),
            dcc.Store(id="freeplot_parameters_store", data=None),
            dcc.Store(id="freeplot_database_metadata_store", data=None)
        ])



    def make_tab_from_widgets(self):
        freeplot_tab = dcc.Tab(
            id="freeplot",
            label="PROFIL",
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

