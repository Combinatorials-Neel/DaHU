import h5py
from pathlib import Path

from ..functions.functions_edx import edx_make_results_dataframe_from_hdf5
from ..functions.functions_profil import profil_make_results_dataframe_from_hdf5
from ..functions.functions_xrd import xrd_make_results_dataframe_from_hdf5
from ..functions.functions_moke import moke_make_results_dataframe_from_hdf5


def hdf5_export_results_to_csv(hdf5_path):
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
                if dataset_group.attrs["HT_type"] in ["esrf", "xrd"]:
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