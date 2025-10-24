import zipfile
from dash import html, dcc, Input, Output, State, ctx

from ..functions.functions_edx import edx_make_results_dataframe_from_hdf5
from ..functions.functions_profil import profil_make_results_dataframe_from_hdf5
from ..functions.functions_xrd import xrd_make_results_dataframe_from_hdf5
from ..hdf5_compilers.hdf5compile_annealing import *
from ..hdf5_compilers.hdf5compile_deposition import *
from ..hdf5_compilers.hdf5compile_edx import *
from ..hdf5_compilers.hdf5compile_esrf import *
from ..hdf5_compilers.hdf5compile_moke import *
from ..hdf5_compilers.hdf5compile_profil import *
from ..hdf5_compilers.hdf5compile_squid import *
from ..hdf5_compilers.hdf5compile_xrd import *
from ..interface.widgets_base import *


def callbacks_hdf5(app):

    @app.callback(Output("hdf5_path_box", "children", allow_duplicate=True),
                  Input("hdf5_path_store", "data"),
                  prevent_initial_call=True)
    def display_current_hdf5_path(hdf5_path):
        return str(Path(hdf5_path))

    @app.callback([Output('hdf5_text_box', 'children'),
                   Output("hdf5_path_store", "data")],
                  Input('hdf5_create_button', 'n_clicks'),
                  State('data_path_store', 'data'),
                  State('hdf5_sample_name', 'value'),
                  State('hdf5_sample_date', 'value'),
                  State('hdf5_sample_operator', 'value'),
                  State("hdf5_path_store", "data"),
                  State("hdf5_create_type_dropdown", "value"),
                  )

    def create_new_hdf5_file(n_clicks, data_path, sample_name, sample_date, sample_operator, current_hdf5_path, hdf5_type):
        if n_clicks > 0:

            sample_dict = {
                'sample_name': sample_name,
                'fabrication_date': sample_date,
                'operator': sample_operator
            }

            if not all(sample_dict.values()):
                return 'All data entries must be filled to create a new hdf5 file', current_hdf5_path

            data_path = Path(data_path)
            hdf5_path = data_path / f'{sample_name}.hdf5'
            check = create_new_hdf5(hdf5_path, hdf5_type, sample_dict)

            if check:
                return f'Created new HDF5 file at {hdf5_path}', str(hdf5_path)
        else:
            raise PreventUpdate


    @app.callback(
        Output('hdf5_text_box', 'children', allow_duplicate=True),
        Input('hdf5_add_button', 'n_clicks'),
        State('hdf5_upload_folder_path', 'data'),
        State('hdf5_measurement_type', 'value'),
        State('hdf5_path_store', 'data'),
        State("hdf5_dataset_name", "value"),
        State("hdf5_manual_1", "value"),
        State("hdf5_manual_2", "value"),
        State("hdf5_manual_3", "value"),
        prevent_initial_call=True
    )

    def add_measurement_to_file(n_clicks, uploaded_folder_path, measurement_type, hdf5_path, dataset_name, manual_1, manual_2, manual_3):
        if n_clicks > 0:
            if uploaded_folder_path is not None:
                uploaded_folder_path = Path(uploaded_folder_path)
            hdf5_path = Path(hdf5_path)
            if measurement_type == "Magnetron":
                write_magnetron_to_hdf5(hdf5_path, uploaded_folder_path)
                return f'Added {measurement_type} measurement to {hdf5_path} as {dataset_name}.'
            if measurement_type == 'EDX':
                write_edx_to_hdf5(hdf5_path, uploaded_folder_path, dataset_name=dataset_name)
                return f'Added {measurement_type} measurement to {hdf5_path} as {dataset_name}.'
            if measurement_type =='MOKE':
                write_moke_to_hdf5(hdf5_path, uploaded_folder_path, dataset_name=dataset_name)
                return f'Added {measurement_type} measurement to {hdf5_path} as {dataset_name}.'
            if measurement_type == 'PROFIL':
                write_dektak_to_hdf5(hdf5_path, uploaded_folder_path, dataset_name=dataset_name)
                return f'Added {measurement_type} measurement to {hdf5_path} as {dataset_name}.'
            if measurement_type =='XRD':
                write_smartlab_to_hdf5(hdf5_path, uploaded_folder_path, dataset_name=dataset_name)
                return f'Added {measurement_type} measurement to {hdf5_path} as {dataset_name}.'
            if measurement_type == "ESRF":
                write_esrf_to_hdf5(hdf5_path, uploaded_folder_path, dataset_name=dataset_name)
                return f'Added {measurement_type} measurement to {hdf5_path} as {dataset_name}.'
            if measurement_type == "XRD results":
                write_xrd_results_to_hdf5(hdf5_path, uploaded_folder_path, target_dataset=dataset_name)
                return f'Added {measurement_type} measurement to {hdf5_path} as {dataset_name}.'
            if measurement_type == "Annealing":
                # In annealing mode:
                # manual 1 = int(temp, degC),
                # manual 2 = int(time, seconds),
                # manual 3 = str(RTA or Tubular)
                anneal_dict = {
                    "temperature": manual_1,
                    "time": manual_2,
                    "instrument": manual_3
                }
                if uploaded_folder_path is not None:
                    uploaded_file_path = uploaded_folder_path.with_suffix(".HIS")
                    write_annealing_to_hdf5(hdf5_path, uploaded_file_path, anneal_dict, dataset_name=dataset_name)
                    return f'Added {measurement_type} data to {hdf5_path}.'
                else:
                    manual_annealing_to_hdf5(hdf5_path, anneal_dict, dataset_name=dataset_name)
                    return f'Added {measurement_type} data to {hdf5_path}.'
            if measurement_type == "SQUID":
                # In squid mode:
                # manual 1 = float(x_pos, mm)
                # manual 2 = float(y_pos, mm)
                # manual 3 = float(surface_area, cm2)

                squid_dict = {
                    "x_pos": manual_1,
                    "y_pos": manual_2,
                    "surface_area": manual_3,
                }
                if uploaded_folder_path is not None:
                    uploaded_file_path = uploaded_folder_path.with_suffix(".dat")
                    write_squid_to_hdf5(hdf5_path, uploaded_file_path, squid_dict, dataset_name=dataset_name)
                    return f'Added {measurement_type} data to {hdf5_path}.'
            if measurement_type == "Picture":
                # In picture mode:
                #manual 1 = str(comment)
                #manual 2 = NaN
                #manual 3 = NaN
                if uploaded_folder_path is not None:
                    write_image_to_hdf5(hdf5_path, uploaded_folder_path, manual_1, dataset_name=dataset_name)
                    return f'Added {measurement_type} data to {hdf5_path}.'
            if measurement_type == "HT hdf5":
                # In HT hdf5 mode:
                # dataset_name = list(datasets to be copied)
                # manual 1 = str(copy mode)
                # manual 2 = NaN
                # manual 3 = NaN
                if uploaded_folder_path is not None:
                    copy_datasets_to_hdf5(hdf5_path, uploaded_folder_path, dataset_name, manual_1)

            return f'Failed to add measurement to {hdf5_path}.'


    @app.callback(
        [Output('hdf5_upload_folder_path', 'data'),
         Output('hdf5_measurement_type', 'value'),
         Output('hdf5_text_box', 'children', allow_duplicate=True)],
        Input('hdf5_upload', 'isCompleted'),
        State('hdf5_upload', 'fileNames'),
        State('hdf5_upload', 'upload_id'),
        State('hdf5_upload_folder_root', 'data'),
        prevent_initial_call=True
    )
    def unpack_uploaded_measurements(is_completed, uploaded_folder_path, upload_id, upload_folder_root):
        if not is_completed or not uploaded_folder_path:
            return None, None, "No file uploaded"

        uploaded_path = Path(upload_folder_root, upload_id, uploaded_folder_path[0])
        extract_dir = uploaded_path.parent / uploaded_path.stem

        if uploaded_path.name.endswith('.zip'):
            with zipfile.ZipFile(uploaded_path, 'r') as zip_file:
                filenames_list = zip_file.namelist()
                measurement_type, depth = detect_measurement(filenames_list)

                if not measurement_type:
                    output_message = f'Unable to detect measurement within {uploaded_folder_path}'
                    return None, measurement_type, output_message
                else:
                    output_message = f'{len(filenames_list)} {measurement_type} files detected in {uploaded_folder_path}'
                    zip_file.extractall(extract_dir)
                    return str(extract_dir), measurement_type, output_message

        elif uploaded_path.name.endswith('.HIS'):
            return str(extract_dir), "Annealing", f"1 Annealing file detected in {uploaded_folder_path}"

        elif uploaded_path.name.endswith('.dat'):
            return str(extract_dir), "SQUID", f"1 Squid file detected in {uploaded_folder_path}"

        elif uploaded_path.name.lower().endswith(('.png', ".jpg", ".jpeg")):
            return str(uploaded_path), "Picture", f"1 Picture file detected in {uploaded_folder_path}"

        elif uploaded_path.name.endswith(".hdf5"):
            with h5py.File(uploaded_path, "r") as hdf5_file:
                if hdf5_file.attrs["HT_class"] == "library":
                    return str(uploaded_path), "HT hdf5", f"HT library file detected in {uploaded_folder_path}"
                else:
                    raise PreventUpdate



    @app.callback(
        Output("hdf5_text_box", "children", allow_duplicate=True),
        Input("hdf5_export", "n_clicks"),
        State("hdf5_path_store", "data"),
        prevent_initial_call=True
    )
    def export_hdf5_results_to_csv(n_clicks, hdf5_path):
        if n_clicks > 0:
            hdf5_path = Path(hdf5_path)
            general_df = None
            with h5py.File(hdf5_path, "r") as hdf5_file:
                for dataset_name, dataset_group in hdf5_file.items():
                    if dataset_name == "sample":
                        continue
                    else:
                        if dataset_group.attrs["HT_type"] == "edx":
                            df = edx_make_results_dataframe_from_hdf5(dataset_group)
                        if dataset_group.attrs["HT_type"] == "moke":
                            df = moke_make_results_dataframe_from_hdf5(dataset_group)
                        if dataset_group.attrs["HT_type"] in ["esrf","xrd"]:
                            df = xrd_make_results_dataframe_from_hdf5(dataset_group)
                        if dataset_group.attrs["HT_type"] == "profil":
                            df = profil_make_results_dataframe_from_hdf5(dataset_group)

                    df = df.drop('ignored', axis=1, errors='ignore')
                    df = df.set_index(["x_pos (mm)", "y_pos (mm)"])
                    df = df.add_suffix(f"[{dataset_name}]")
                    if general_df is None:
                        general_df = df
                    else:
                        general_df = general_df.join(df, how='outer')

            general_df.to_csv(hdf5_path.with_suffix(".csv"), index=True)

            return f"Successfully exported HDF5 to {hdf5_path.with_suffix(".csv")}"



    @app.callback(
        Output("hdf5_text_box", "children", allow_duplicate=True),
        Input("hdf5_update", "n_clicks"),
        State("hdf5_path_store", "data"),
        prevent_initial_call=True
    )
    def update_hdf5_file(n_clicks, hdf5_path):
        if n_clicks > 0:
            hdf5_path = Path(hdf5_path)
            checklist = []
            with h5py.File(hdf5_path, "a") as hdf5_file:
                if "HT_type" not in hdf5_file.attrs or hdf5_file.attrs["HT_type"] == "library":
                    if update_library_hdf5(hdf5_file):
                        checklist.append("[ROOT]")
                for dataset_name, dataset_group in hdf5_file.items():
                    if dataset_name == "sample":
                        continue
                    if dataset_group.attrs["HT_type"] == "edx":
                        continue
                    if dataset_group.attrs["HT_type"] == "moke":
                        continue
                    if dataset_group.attrs["HT_type"] in ["esrf", "xrd"]:
                        continue
                    if dataset_group.attrs["HT_type"] == "profil":
                        if update_dektak_hdf5(dataset_group):
                            checklist.append(f"[PROFIL] {dataset_name}")
            if not checklist:
                return "All datasets are already up to date"
            return f"Successfully updated datasets {checklist}"



    @app.callback(
        Output("hdf5_deposition_info", "children"),
        Input("hdf5_path_store", "data"),
    )
    def update_deposition_info(hdf5_path):
        if hdf5_path is None:
            raise PreventUpdate

        widget_title = widget_title_card("Deposition")

        with h5py.File(hdf5_path, "r") as hdf5_file:
            if "deposition" not in hdf5_file.keys():
                return [
                    widget_title,
                    widget_measurement_missing()
                ]
            else:
                return [
                    widget_title,
                    widget_measurement_found(number = 1)
                ]


    @app.callback(
        Output("hdf5_annealing_info", "children"),
        Input("hdf5_path_store", "data"),
    )
    def update_annealing_info(hdf5_path):
        if hdf5_path is None:
            raise PreventUpdate

        widget_title = widget_title_card("Annealing")

        with h5py.File(hdf5_path, "r") as hdf5_file:
            annealing_groups = get_hdf5_datasets(hdf5_file, "annealing")
            number = len(annealing_groups)
            if number == 0:
                return [
                    widget_title,
                    widget_measurement_missing()
                ]

            else:
                if hdf5_file[annealing_groups[0]].attrs["data_source"] == "manual":
                    return [
                        widget_title,
                        widget_manual_data(number)
                    ]
                else:
                    return [
                        widget_title,
                        widget_measurement_found(number)
                    ]

    @app.callback(
        Output("hdf5_edx_info", "children"),
        Input("hdf5_path_store", "data"),
    )
    def update_edx_info(hdf5_path):
        if hdf5_path is None:
            raise PreventUpdate

        widget_title = widget_title_card("EDX")

        with h5py.File(hdf5_path, "r") as hdf5_file:
            edx_groups = get_hdf5_datasets(hdf5_file, "edx")
            number = len(edx_groups)
            if number == 0:
                return [
                    widget_title,
                    widget_measurement_missing()
                ]

            else:
                return [
                    widget_title,
                    widget_measurement_found(number)
                ]

    @app.callback(
        Output("hdf5_profil_info", "children"),
        Input("hdf5_path_store", "data"),
    )
    def update_profil_info(hdf5_path):
        if hdf5_path is None:
            raise PreventUpdate

        widget_title = widget_title_card("Profilometry")

        with h5py.File(hdf5_path, "r") as hdf5_file:
            profil_groups = get_hdf5_datasets(hdf5_file, "profil")
            number = len(profil_groups)
            if number == 0:
                return [
                    widget_title,
                    widget_measurement_missing()
                ]

            else:
                return [
                    widget_title,
                    widget_measurement_found(number)
                ]

    @app.callback(
        Output("hdf5_moke_info", "children"),
        Input("hdf5_path_store", "data"),
    )
    def update_moke_info(hdf5_path):
        if hdf5_path is None:
            raise PreventUpdate

        widget_title = widget_title_card("Moke")

        with h5py.File(hdf5_path, "r") as hdf5_file:
            moke_groups = get_hdf5_datasets(hdf5_file, "moke")
            number = len(moke_groups)
            if number == 0:
                return [
                    widget_title,
                    widget_measurement_missing()
                ]

            else:
                return [
                    widget_title,
                    widget_measurement_found(number)
                ]

    @app.callback(
        Output("hdf5_xrd_info", "children"),
        Input("hdf5_path_store", "data"),
    )
    def update_xrd_info(hdf5_path):
        if hdf5_path is None:
            raise PreventUpdate

        widget_title = widget_title_card("XRD")

        with h5py.File(hdf5_path, "r") as hdf5_file:
            xrd_groups = get_hdf5_datasets(hdf5_file, "xrd")
            number = len(xrd_groups)
            if number == 0:
                return [
                    widget_title,
                    widget_measurement_missing()
                ]

            else:
                return [
                    widget_title,
                    widget_measurement_found(number)
                ]


    @app.callback(
        [Output("hdf5_dataset_input", "children"),
         Output("hdf5_text_box", "children", allow_duplicate=True)],
        Input("hdf5_measurement_type", "value"),
        State("hdf5_path_store", "data"),
        prevent_initial_call=True
    )
    def switch_input_mode(measurement_type, hdf5_path):
        # Redefine the base children for fallback
        new_children = [
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

        if measurement_type == "XRD results":
            with h5py.File(hdf5_path, "r") as hdf5_file:
                datasets = get_hdf5_datasets(hdf5_file, "xrd")
            if not datasets:
                return new_children, "No ESRF or XRD datasets found in HDF5 file"
            else:
                new_children = [
                    html.Label("Dataset Name"),
                    dcc.Dropdown(
                        id="hdf5_dataset_name",
                        className="long-item",
                        options=datasets,
                        value=datasets[0],
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

        if measurement_type == "Annealing":
            new_children = [
                html.Label("Dataset Name"),
                dcc.Input(
                    id="hdf5_dataset_name",
                    className="long-item",
                    type="text",
                    placeholder="Dataset Name",
                    value=None,
                ),
                html.Label("Annealing temperature"),
                dcc.Input(
                    id="hdf5_manual_1",
                    className="long-item",
                    type="number",
                    placeholder="Annealing temperature",
                ),
                html.Label("Annealing time"),
                dcc.Input(
                    id="hdf5_manual_2",
                    className="long-item",
                    type="number",
                    placeholder="Annealing time",
                ),
                dcc.Dropdown(
                    id="hdf5_manual_3",
                    className="long-item",
                    placeholder="Furnace",
                    options=["JetFirst RTA", "UHV Tubular"]
                )
            ]

        if measurement_type == "SQUID":
            new_children = [
                html.Label("Dataset Name"),
                dcc.Input(
                    id="hdf5_dataset_name",
                    className="long-item",
                    type="text",
                    placeholder="Dataset Name",
                    value=None,
                ),
                html.Label("x_pos (mm)"),
                dcc.Input(
                    id="hdf5_manual_1",
                    className="long-item",
                    type="number",
                    placeholder="x_pos (mm)",
                ),
                html.Label("y_pos (mm)"),
                dcc.Input(
                    id="hdf5_manual_2",
                    className="long-item",
                    type="number",
                    placeholder="y_pos (mm)",
                ),
                html.Label("surface area (cm2)"),
                dcc.Input(
                    id="hdf5_manual_3",
                    className="long-item",
                    type="number",
                    placeholder="surface area (cm2)",
                ),
            ]

        if measurement_type == "Picture":
            new_children = [
                html.Label("Dataset Name"),
                dcc.Input(
                    id="hdf5_dataset_name",
                    className="long-item",
                    type="text",
                    placeholder="Dataset Name",
                    value=None,
                ),
                dcc.Input(
                    id="hdf5_manual_1",
                    className="long-item",
                    type="text",
                    placeholder="comment"
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

        if measurement_type == "HT hdf5":
            with h5py.File(hdf5_path, "r") as hdf5_file:
                datasets = get_hdf5_datasets(hdf5_file, "all")
            if not datasets:
                return new_children, "No datasets found in HDF5 file"
            new_children = [
                html.Label("Dataset Name"),
                dcc.Dropdown(
                    id="hdf5_dataset_name",
                    className="long-item",
                    options=datasets,
                    value=datasets[0],
                    multi=True
                ),
                dcc.Dropdown(
                    id="hdf5_manual_1",
                    className="long-item",
                    options=["hard copy", "soft copy"],
                    value="hard copy"
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

        return new_children, ""


    @app.callback(
        [Output("browser_popup", "is_open", allow_duplicate=True),
         Output("hdf5_path_store", "data", allow_duplicate=True)],
        Input("hdf5_path_box", "n_clicks"),
        Input("browser_select_button", "n_clicks"),
        State("browser_popup", "is_open"),
        State("hdf5_path_store", "data"),
        State("stored_cwd", "data"),
        prevent_initial_call=True,
    )
    def toggle_hdf5_browser(open_click, select_click, is_open, hdf5_path, stored_cwd):
        if ctx.triggered_id == "hdf5_path_box" and open_click > 0 and not is_open:
            return True, hdf5_path
        if ctx.triggered_id == "browser_select_button" and select_click > 0 and is_open:
            return False, stored_cwd

        return is_open, hdf5_path


    @app.callback(
        [Output("layer_editor_popup", "is_open", allow_duplicate=True),
         Output("layer_editor_index", "value")],
        Input("layer_card_open_button", "n_clicks"),
        State("layer_editor_popup", "is_open"),
        prevent_initial_call=True
    )
    def toggle_layer_popup(open_click, is_open):
        if not is_open and open_click > 0:
            return True, 1
        elif is_open:
            raise PreventUpdate


    @app.callback(
        [Output("layer_editor_element", "value"),
         Output("layer_editor_time", "value"),
         Output("layer_editor_thickness", "value"),
         Output("layer_editor_temperature", "value"),
         Output("layer_editor_power", "value"),
         Output("layer_editor_distance", "value"),
         Output("layer_editor_angle", "value"),
         Output("layer_editor_comment", "value")],
        Input("layer_editor_index", "value"),
        State("hdf5_path_store", "data"),
        State("layer_editor_popup", "is_open"),
        prevent_initial_call=True
    )
    def layer_editor_load_values(index, hdf5_path, is_open):
        if not is_open:
            raise PreventUpdate
        with h5py.File(hdf5_path, "r") as hdf5_file:
            layer_group = hdf5_file.get(f"sample/Layer {index}")
            if layer_group is None:
                return None, None, None, None, None, None, None, None
            elif layer_group is not None:
                element = layer_group.get("element")[()].decode()
                time = layer_group.get("time")[()].decode()
                thickness = layer_group.get("nominal_thickness")[()].decode()
                temperature = layer_group.get("temperature")[()].decode()
                power = layer_group.get("power")[()].decode()
                distance = layer_group.get("distance")[()].decode()
                angle = layer_group.get("angle")[()].decode()
                # comment = layer_group.get("comment")[()].decode()
                comment=None

        return element, time, thickness, temperature, power, distance, angle, comment


    @app.callback(
        Output("hdf5_text_box", "children", allow_duplicate=True),
        Input("layer_editor_save_button", "n_clicks"),
        State("hdf5_path_store", "data"),
        State("layer_editor_index", "value"),
        State("layer_editor_element", "value"),
        State("layer_editor_time", "value"),
        State("layer_editor_thickness", "value"),
        State("layer_editor_temperature", "value"),
        State("layer_editor_power", "value"),
        State("layer_editor_distance", "value"),
        State("layer_editor_angle", "value"),
        State("layer_editor_comment", "value"),
        State("layer_editor_popup", "is_open"),
        prevent_initial_call=True
    )
    def layer_editor_save_layer(save_click, hdf5_path, index, element, time, thickness,
                                temperature, power, distance, angle, comment, is_open):
        if not is_open:
            raise PreventUpdate
        if save_click > 0:
            with h5py.File(hdf5_path, "r") as hdf5_file:
                sample_group = hdf5_file.get("sample")
                if f"layer_{index}" in sample_group:
                    layer_group = sample_group[f"layer_{index}"]
                else:
                    layer_numbers = []
                    for subgroup in sample_group.keys():
                        match = re.match(r"^layer_(\d+)$", subgroup)
                        if match:
                            layer_numbers.append(int(match.group(1)))
                    highest_index = max(layer_numbers) if layer_numbers else 0
                    layer_group = sample_group.create_group(f"layer_{highest_index + 1}")

                layer_group["element"] = element
                layer_group["time"] = time
                layer_group["thickness"] = thickness
                layer_group["temperature"] = temperature
                layer_group["power"] = power
                layer_group["distance"] = distance
                layer_group["angle"] = angle
                layer_group["comment"] = comment

                layer_group["time"].attrs["units"] = "s"
                layer_group["thickness"].attrs["units"] = "nm"
                layer_group["temperature"].attrs["units"] = "°C"
                layer_group["power"].attrs["units"] = "W"
                layer_group["distance"].attrs["units"] = "mm"
                layer_group["angle"].attrs["units"] = "deg"

        return "Layer saved"




