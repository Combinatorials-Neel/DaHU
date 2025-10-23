from dash import ALL, Input, Output, State, ctx
import dash_bootstrap_components as dbc

from ..functions.functions_browser import *
from ..functions.functions_shared import *

"""Callbacks for file browser"""


def callbacks_browser(app):

    @app.callback(
        Output("stored_cwd", "data"),
        Input("data_path_store", "data")
    )
    def set_default_data_folder(data_path):
        if data_path is None:
            raise PreventUpdate
        return data_path

    @app.callback(
        Output("cwd", "children"),
        Input("stored_cwd", "data"),
        Input("parent_dir", "n_clicks"),
        Input("cwd", "children"),
        prevent_initial_call=True,
    )
    def get_parent_directory(stored_cwd, n_clicks, current_dir):
        triggered_id = ctx.triggered_id
        if triggered_id == "stored_cwd":
            return stored_cwd
        parent = Path(current_dir).parent.as_posix()
        return parent

    @app.callback(
        Output("cwd_files", "children"),
        Input("cwd", "children")
    )
    def list_cwd_files(cwd):
        path = Path(cwd)
        all_file_details = []
        if path.is_dir():
            files = sorted(os.listdir(path), key=str.lower)
            for i, file in enumerate(files):
                filepath = Path(file)
                full_path = os.path.join(cwd, filepath.as_posix())
                is_dir = Path(full_path).is_dir()
                link = html.A(
                    [
                        html.Span(
                            file,
                            id={"type": "listed_file", "index": i},
                            title=full_path,
                            style=(
                                {"fontWeight": "bold", "fontSize": 18} if is_dir else {}
                            ),
                        )
                    ],
                    href="#",
                )
                details = file_info(Path(full_path))
                details["filename"] = link
                if is_dir:
                    details["extension"] = html.Img(
                        src=app.get_asset_url("icons/default_folder.svg"),
                        width=25,
                        height=25,
                    )
                else:
                    details["extension"] = icon_file(app, details["extension"][1:])
                all_file_details.append(details)

        df = pd.DataFrame(all_file_details)
        df = df.rename(columns={"extension": ""})
        table = dbc.Table.from_dataframe(
            df, striped=False, bordered=False, hover=True, size="sm"
        )
        return html.Div(table)

    @app.callback(
        Output("stored_cwd", "data", allow_duplicate=True),
        Input({"type": "listed_file", "index": ALL}, "n_clicks"),
        State({"type": "listed_file", "index": ALL}, "title"),
        prevent_initial_call=True,
    )
    def store_clicked_file(n_clicks, title):
        if not n_clicks or set(n_clicks) == {None}:
            raise PreventUpdate
        index = ctx.triggered_id["index"]
        return title[index]

    # # Callback to set folder path
    # @app.callback(
    #     [
    #         Output("data_path_store", "data", allow_duplicate=True),
    #         Output("data_path_text", "children"),
    #     ],
    #     Input("data_path_button", "n_clicks"),
    #     Input("data_path_store", "data"),
    #     State("stored_cwd", "data"),
    #     prevent_initial_call=True,
    # )
    # def set_folder_path(n_clicks, stored_folder_path, current_folder_path):
    #     if not n_clicks:
    #         return stored_folder_path, str(stored_folder_path)
    #     elif n_clicks > 0:
    #         return current_folder_path, str(current_folder_path)
    #
    #
    # # Callback for hdf5 file path
    # @app.callback(
    #     [
    #         Output("hdf5_path_store", "data", allow_duplicate=True),
    #         Output("hdf5_path_text", "children"),
    #     ],
    #     Input("hdf5_path_button", "n_clicks"),
    #     Input("hdf5_path_store", "data"),
    #     State("stored_cwd", "data"),
    #     prevent_initial_call=True,
    # )
    # def set_folder_path(n_clicks, stored_folder_path, current_folder_path):
    #     if not n_clicks:
    #         return stored_folder_path, str(stored_folder_path)
    #     elif n_clicks > 0:
    #         return current_folder_path, str(current_folder_path)


    @app.callback(
        [Output("browser_popup", "is_open"),
         Output("hdf5_path_store", "data", allow_duplicate=True)],
        Input("hdf5_path_box", "n_clicks"),
        Input("browser_select_button", "n_clicks"),
        State("browser_popup", "is_open"),
        State("hdf5_path_store", "data"),
        State("stored_cwd", "data"),
        prevent_initial_call=True,
    )
    def toggle_browser(open_click, select_click, is_open, hdf5_path, stored_cwd):
        if ctx.triggered_id == "hdf5_path_box" and open_click > 0 and not is_open:
            return True, hdf5_path
        if ctx.triggered_id == "browser_select_button" and select_click > 0 and is_open:
            return False, stored_cwd

        return is_open, hdf5_path

