import dash_uploader
import dash_bootstrap_components as dbc
from dash import Dash, dcc

from modules.callbacks import (
    callbacks_browser,
    callbacks_profil,
    callbacks_edx,
    callbacks_moke,
    callbacks_xrd,
    callbacks_hdf5,
)
from modules.functions.functions_shared import *

from modules.interface.widgets_base import widget_browser_modal, widget_layer_modal, widget_new_hdf5_modal
from modules.interface.widgets_edx import make_edx_tab
from modules.interface.widgets_hdf5 import make_hdf5_tab
from modules.interface.widgets_moke import make_moke_tab
from modules.interface.widgets_profil import make_profil_tab
from modules.interface.widgets_xrd import make_xrd_tab

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)

folderpath = None

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

PROGRAM_VERSION = "0.20"
UPLOAD_FOLDER_ROOT = os.path.join(script_dir, "uploads")

# Clean the upload folder
cleanup_directory(UPLOAD_FOLDER_ROOT)

# %%
app = Dash(suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.FLATLY])

dash_uploader.configure_upload(app, UPLOAD_FOLDER_ROOT)

hdf5_tab = make_hdf5_tab(UPLOAD_FOLDER_ROOT)
edx_tab = make_edx_tab(UPLOAD_FOLDER_ROOT)
profil_tab = make_profil_tab(UPLOAD_FOLDER_ROOT)
moke_tab = make_moke_tab(UPLOAD_FOLDER_ROOT)
xrd_tab = make_xrd_tab(UPLOAD_FOLDER_ROOT)

# Defining the main window layout
app.layout = dbc.Container(
    children=[
        dbc.Tabs(
            id="tabs",
            active_tab="hdf5",
            children=[hdf5_tab, edx_tab, profil_tab, moke_tab, xrd_tab],

        ),
        widget_browser_modal(),
        widget_layer_modal(),
        widget_new_hdf5_modal(),
        dcc.Store(id="hdf5_path_store", storage_type="local"),
        dcc.Store(id="data_path_store", storage_type="local"),
        dcc.Store(id="browser_source_id"),
    ],
    fluid=True,
)

callbacks_browser.callbacks_browser(app)
callbacks_hdf5.callbacks_hdf5(app)
callbacks_profil.callbacks_profil(app)
callbacks_edx.callbacks_edx(app)
callbacks_moke.callbacks_moke(app)
callbacks_xrd.callbacks_xrd(app)
# callbacks_freeplot.callbacks_freeplot(app)

if __name__ == "__main__":
    app.run(debug=True, port=8050)
