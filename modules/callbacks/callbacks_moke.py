from dash import html, dcc, Input, Output, State, ctx

from ..hdf5_compilers.hdf5compile_moke import *

"""Callbacks for MOKE tab"""


def callbacks_moke(app):

    # Callback to update moke plot based on heatmap click position
    @app.callback(
        Output("moke_position_store", "data"),
        Input("moke_heatmap", "clickData"),
        prevent_initial_call=True,
    )
    def update_position(heatmap_click):
        if heatmap_click is None:
            return None
        target_x = heatmap_click["points"][0]["x"]
        target_y = heatmap_click["points"][0]["y"]

        position = (target_x, target_y)

        return position

    @app.callback(
        [
            Output("moke_select_dataset", "options"),
            Output("moke_select_dataset", "value"),
        ],
        Input("hdf5_path_store", "data"),
    )
    @check_conditions(moke_conditions, hdf5_path_index=0)
    def moke_scan_hdf5_for_datasets(hdf5_path):
        with h5py.File(hdf5_path, "r") as hdf5_file:
            dataset_list = get_hdf5_datasets(hdf5_file, dataset_type="moke")

        return dataset_list, dataset_list[0]
    
    # Reads the given dataset into a DataFrame, then serialize it to json.
    # Returns the json and the columns of the df as options for the plot selection
    @app.callback(
        [Output("moke_results_store", "data"),
         Output("moke_heatmap_select", "options"),
         Output("moke_heatmap_select", "value")],
        Input("moke_select_dataset", "value"),
        State("hdf5_path_store", "data"),
    )
    @check_conditions(moke_conditions, hdf5_path_index=1)
    def moke_read_dataset_into_store(selected_dataset, hdf5_path):
        with h5py.File(hdf5_path, "r") as hdf5_file:
            moke_group = hdf5_file.get(selected_dataset)
            moke_df = moke_make_results_dataframe_from_hdf5(moke_group)

            if moke_df is None:
                raise PreventUpdate

            moke_df_json = moke_df.to_json(orient="split")
            # First three columns are x_pos, y_pos and the ignored tag
            options = list(moke_df.columns[3:])

        return moke_df_json, options, None

    # Callback for heatmap selection
    @app.callback(
        [
            Output("moke_heatmap", "figure", allow_duplicate=True),
            Output("moke_heatmap_min", "value"),
            Output("moke_heatmap_max", "value"),
        ],
        Input("moke_heatmap_select", "value"),
        Input("moke_heatmap_min", "value"),
        Input("moke_heatmap_max", "value"),
        Input("moke_heatmap_precision", "value"),
        Input("moke_heatmap_edit", "value"),
        State("hdf5_path_store", "data"),
        State("moke_results_store", "data"),
        prevent_initial_call=True,
    )
    @check_conditions(moke_conditions, hdf5_path_index=5)
    def moke_update_heatmap(heatmap_select,z_min,z_max,precision,edit_toggle,hdf5_path,moke_df_json):
        moke_df = pd.read_json(StringIO(moke_df_json), orient="split")
        # Reset colorbar bounds when needed
        if ctx.triggered_id in [
            "moke_heatmap_select",
            "moke_heatmap_edit",
            "moke_heatmap_precision",
        ]:
            z_min = None
            z_max = None

        masking = True
        if edit_toggle in ["edit", "unfiltered"]:
            masking = False

        if heatmap_select is not None:
            name, unit = split_name_and_unit(heatmap_select)
            plot_title = f"{name} MOKE map"
            colorbar_title = f"{unit}"
        else:
            plot_title = ""
            colorbar_title = ""

        fig = make_heatmap_from_dataframe(
            moke_df,
            values=heatmap_select,
            z_min=z_min,
            z_max=z_max,
            plot_title=plot_title,
            colorbar_title=colorbar_title,
            precision=precision,
            masking=masking,
        )

        z_min = np.round(fig.data[0].zmin, precision)
        z_max = np.round(fig.data[0].zmax, precision)

        return fig, z_min, z_max

    # Profile plot
    @app.callback(
        Output("moke_plot", "figure"),
        Input("moke_position_store", "data"),
        Input("moke_plot_select", "value"),
        Input("moke_data_treatment_store", "data"),
        Input("moke_heatmap_select", "value"),
        Input("moke_select_dataset", "value"),
        State("hdf5_path_store", "data"),
    )
    @check_conditions(moke_conditions, hdf5_path_index=5)
    def moke_update_plot(
        position,
        plot_options,
        treatment_dict,
        heatmap_select,
        selected_dataset,
        hdf5_path,
    ):
        if position is None:
            raise PreventUpdate

        target_x = position[0]
        target_y = position[1]

        fig = go.Figure()

        with h5py.File(hdf5_path, "r") as hdf5_file:
            moke_group = hdf5_file[selected_dataset]
            measurement_df = moke_get_measurement_from_hdf5(
                moke_group, target_x, target_y
            )
            results_dict = moke_get_results_from_hdf5(moke_group, target_x, target_y)

        measurement_df = moke_treat_measurement_dataframe(
            measurement_df, treatment_dict
        )

        title_tag = ""
        if plot_options == "oscilloscope":
            fig = moke_plot_oscilloscope_from_dataframe(fig, measurement_df)
            title_tag = "oscilloscope plot"
        elif plot_options == "loop":
            fig = moke_plot_loop_from_dataframe(fig, measurement_df)
            title_tag = "hysteresis loop"
        elif plot_options == "stored_result":
            fig = moke_plot_loop_from_dataframe(fig, measurement_df)
            if heatmap_select == "coercivity_m0_(T)":
                fig = moke_plot_vlines(
                    fig,
                    values=[
                        results_dict["coercivity_m0"]["negative"],
                        results_dict["coercivity_m0"]["positive"],
                    ],
                )
            if heatmap_select == "coercivity_dmdh_(T)":
                fig = moke_plot_vlines(
                    fig,
                    values=[
                        results_dict["coercivity_dmdh"]["negative"],
                        results_dict["coercivity_dmdh"]["positive"],
                    ],
                )
            if heatmap_select == "intercept_field_(T)":
                print(results_dict["intercept_field"])
                fig = moke_plot_intercept(
                    fig, intercept_dict=results_dict["intercept_field"]
                )

        fig.update_layout(
            plot_layout(title=f"{title_tag} <br>x = {target_x}, y = {target_y}"),
        )

        return fig

    @app.callback(
        Output("moke_text_box", "children", allow_duplicate=True),
        Input("moke_make_database_button", "n_clicks"),
        State("hdf5_path_store", "data"),
        State("moke_data_treatment_store", "data"),
        State("moke_select_dataset", "value"),
        prevent_initial_call=True,
    )
    @check_conditions(moke_conditions, hdf5_path_index=1)
    def moke_make_database(n_clicks, hdf5_path, treatment_dict, selected_dataset):
        if n_clicks > 0:
            with h5py.File(hdf5_path, "a") as hdf5_file:
                moke_group = hdf5_file[selected_dataset]
                results_dict = moke_batch_fit(moke_group, treatment_dict)
                moke_results_dict_to_hdf5(moke_group, results_dict, treatment_dict)
                return "Great Success!"

    @app.callback(
        [
            Output("moke_data_treatment_store", "data"),
            Output("moke_coil_factor", "value"),
            Output("moke_smoothing_polyorder", "value"),
            Output("moke_smoothing_range", "value"),
        ],
        Input("moke_data_treatment_checklist", "value"),
        Input("moke_coil_factor", "value"),
        Input("moke_smoothing_polyorder", "value"),
        Input("moke_smoothing_range", "value"),
    )
    def store_data_treatment(
        treatment_checklist, coil_factor, smoothing_polyorder, smoothing_range
    ):
        default_coil_factor = 0.92667
        default_smoothing_polyorder = 1
        default_smoothing_range = 10
        if coil_factor is None:
            coil_factor = default_coil_factor
        if smoothing_polyorder is None:
            smoothing_polyorder = default_smoothing_polyorder
        if smoothing_range is None:
            smoothing_range = default_smoothing_range

        treatment_dict = {
            "coil_factor": coil_factor,
            "smoothing": False,
            "smoothing_polyorder": smoothing_polyorder,
            "smoothing_range": smoothing_range,
            "correct_offset": False,
            "filter_zero": False,
            "connect_loops": False,
            "pulse_voltage": 432,
            "shift_loops": False,
        }

        if "smoothing" in treatment_checklist:
            treatment_dict.update({"smoothing": True})
        if "correct_offset" in treatment_checklist:
            treatment_dict.update({"correct_offset": True})
        if "filter_zero" in treatment_checklist:
            treatment_dict.update({"filter_zero": True})
        if "connect_loops" in treatment_checklist:
            treatment_dict.update({"connect_loops": True})
        if "shift_loops" in treatment_checklist:
            treatment_dict.update({"shift_loops": True})

        return treatment_dict, coil_factor, smoothing_polyorder, smoothing_range

    @app.callback(
        Output("moke_loop_map_figure", "figure"),
        Input("moke_loop_map_button", "n_clicks"),
        State("hdf5_path_store", "data"),
        State("moke_data_treatment_store", "data"),
        State("moke_loop_map_checklist", "value"),
        State("moke_select_dataset", "value"),
        prevent_initial_call=True,
    )
    @check_conditions(moke_conditions, hdf5_path_index=1)
    def make_loop_map(n_clicks, hdf5_path, options_dict, checklist, dataset_select):
        normalize = False
        if "normalize" in checklist:
            normalize = True

        if n_clicks > 0:
            with h5py.File(hdf5_path, "a") as hdf5_file:
                moke_group = hdf5_file[dataset_select]
                fig = moke_plot_loop_map(moke_group, options_dict, normalize)
                return fig

    # Callback to deal with heatmap edit mode
    @app.callback(
        Output("moke_text_box", "children", allow_duplicate=True),
        Input("moke_heatmap", "clickData"),
        State("moke_heatmap_edit", "value"),
        State("hdf5_path_store", "data"),
        State("moke_select_dataset", "value"),
        prevent_initial_call=True,
    )
    @check_conditions(moke_conditions, hdf5_path_index=2)
    def heatmap_edit_mode(heatmap_click, edit_toggle, hdf5_path, selected_dataset):
        if edit_toggle != "edit":
            raise PreventUpdate

        target_x = heatmap_click["points"][0]["x"]
        target_y = heatmap_click["points"][0]["y"]

        with h5py.File(hdf5_path, "a") as hdf5_file:
            moke_group = hdf5_file[selected_dataset]
            position_group = get_target_position_group(moke_group, target_x, target_y)
            if not position_group.attrs["ignored"]:
                position_group.attrs["ignored"] = True
                return f"{target_x}, {target_y} ignore set to True"
            else:
                position_group.attrs["ignored"] = False
                return f"{target_x}, {target_y} ignore set to False"