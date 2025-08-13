from dash import html, dcc, Input, Output, State, ctx
import dash_bootstrap_components as dbc


from ..functions.functions_hdf5 import *
from ..functions.functions_shared import *


def callbacks_freeplot(app):

    @app.callback(
        [
            Output("freeplot_select_dataset", "options"),
            Output("freeplot_select_dataset", "value"),
        ],
        Input("hdf5_path_store", "data"),
    )
    def freeplot_scan_for_datasets(hdf5_path):
        with h5py.File(hdf5_path, "r") as hdf5_file:
            dataset_list = get_hdf5_datasets(hdf5_file, dataset_type="all")

        return dataset_list, None


    @app.callback(
        [
            Output("freeplot_x_axis", "options"),
            Output("freeplot_x_axis", "value"),
            Output("freeplot_y_axis", "options"),
            Output("freeplot_y_axis", "value"),
        ],
        Input("freeplot_select_dataset", "value"),
        Input("freeplot_mode_select", "value"),
        State("hdf5_path_store", "data"),
        State("freeplot_position_store", "data"),
    )
    def freeplot_scan_for_axes(selected_dataset, mode_select, hdf5_path, position):
        if selected_dataset is None or position is None:
            raise PreventUpdate

        with h5py.File(hdf5_path, "r") as hdf5_file:
            selected_group = hdf5_file[selected_dataset]
            position_group = get_target_position_group(selected_group, position[0], position[1])
            target_group = position_group[mode_select]
            dataset_list = get_hdf5_datasets(target_group, dataset_type="all")

        return dataset_list, None, dataset_list, None


    @app.callback(
        [
            Output("freeplot_plot", "figure"),
        ],
        Input("freeplot_append_button", "n_clicks"),
        Input("freeplot_replace_button", "n_clicks"),
        State("freeplot_x_axis", "value"),
        State("freeplot_y_axis", "value"),
        State("freeplot_plot", "figure"),
        State("hdf5_path_store", "data"),
        State("freeplot_select_dataset", "value"),
    )
    def freeplot_update_plot(append_button, replace_button, x_axis, y_axis, fig, hdf5_path, selected_dataset):
        if x_axis is None or y_axis is None:
            raise PreventUpdate

        if ctx.triggered_id in ["freeplot_replace_button"]:
            fig = go.figure()
        with h5py.File(hdf5_path, "r") as hdf5_file:
            x_array = hdf5_file[selected_dataset][x_axis][()]
            y_array = hdf5_file[selected_dataset][y_axis][()]

        fig.add_trace(
            go.Scatter(
                x=x_array,
                y=y_array,
                mode="lines",
                line=dict(color="SlateBlue", width=3),
                name=y_axis
            )
        )

        fig.update_layout(plot_layout(showlegend=True))

        return fig
