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

