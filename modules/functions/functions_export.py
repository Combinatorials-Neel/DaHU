import h5py
from pathlib import Path
import os
from PIL import Image, PngImagePlugin
import pandas as pd

from .functions_moke import moke_read_treatment_dict_from_hdf5, moke_get_measurement_from_hdf5, moke_treat_measurement_dataframe
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
                elif dataset_group.attrs["HT_type"] == "moke":
                    df = moke_make_results_dataframe_from_hdf5(dataset_group)
                elif dataset_group.attrs["HT_type"] in ["esrf", "xrd", "xrd_wafer"]:
                    df = xrd_make_results_dataframe_from_hdf5(dataset_group)
                elif dataset_group.attrs["HT_type"] == "profil":
                    df = profil_make_results_dataframe_from_hdf5(dataset_group)
                else:
                    continue

            df = df.drop('ignored', axis=1, errors='ignore')
            df = df.set_index(["x_pos (mm)", "y_pos (mm)"])
            df = df.add_suffix(f"[{dataset_name}]")
            if general_df is None:
                general_df = df
            else:
                general_df = general_df.join(df, how='outer')

        # if "sample" in hdf5_file:
        #     sample_group = hdf5_file["sample"]
        #     if not isinstance(sample_group, h5py.Group):
        #         return
        #
        #     sample_df = get_sample_dataframe_from_hdf5(sample_group)
        #     if general_df is None:
        #         return
        #     for col in sample_df.columns:
        #         general_df[col] = sample_df[col].iloc[0]  # Same value for all rows

    if general_df is not None:
        general_df.to_csv(hdf5_path.with_suffix(".csv"), index=True)


def hdf5_export_sem_images(sem_group, export_path, format="png"):
    dataset_name = str(sem_group.name)[1:]
    sample_name = sem_group["experiment_info/sample/sample_name"][()].decode()
    positions_group = sem_group["positions"]

    export_folder = export_path / dataset_name
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    for position, position_group in positions_group.items():
        index = str(position_group.attrs["index"])

        x_pos = position_group["instrument/x_pos"][()]
        y_pos = position_group["instrument/y_pos"][()]

        filename = f"x{str(x_pos).replace(".", ",")}_y{str(y_pos).replace(".", ",")}"
        file_path = (export_folder / filename).with_suffix(f".{format}")
        print(file_path)

        image_data = position_group.get("measurement/image")[()]
        image = Image.fromarray(image_data, "RGB")

        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("Sample", sample_name)
        metadata.add_text("Dataset", dataset_name)
        metadata.add_text("x_pos", str(x_pos))
        metadata.add_text("y_pos", str(y_pos))
        metadata.add_text("index", index)
        image.save(file_path, png_info=metadata)


def hdf5_export_moke_loops(moke_group, export_path):
    dataset_name = str(moke_group.name)[1:]
    sample_name = moke_group["experiment_info/sample/sample_name"][()].decode()
    positions_group = moke_group["positions"]

    export_folder = export_path / dataset_name
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    for position, position_group in positions_group.items():
        index = str(position_group.attrs["index"])

        x_pos = position_group["instrument/x_pos"][()]
        y_pos = position_group["instrument/y_pos"][()]

        filename = f"x{str(x_pos).replace(".", ",")}_y{str(y_pos).replace(".", ",")}"
        file_path = (export_folder / filename).with_suffix(".xy")
        print(file_path)

        treatment_dict = moke_read_treatment_dict_from_hdf5(position_group)

        df = moke_get_measurement_from_hdf5(moke_group, target_x=x_pos, target_y=y_pos, index=0)
        df = moke_treat_measurement_dataframe(df, treatment_dict)

        field_array = df["field"].values
        magnetization_array = df["magnetization"].values

        with open(file_path, "w") as export_file:
            export_file.write(f"#sample_name: {sample_name}\n")
            export_file.write(f"#dataset_name: {dataset_name}\n")
            export_file.write(f"#x_pos: {x_pos}\n")
            export_file.write(f"#y_pos: {y_pos}\n")
            export_file.write(f"#index: {index}\n")
            export_file.write(f"Applied Field (T)\tMoke Signal (V)\n")

            for x, y in zip(field_array, magnetization_array):
                export_file.write(f"{x}\t{y}\n")

            export_file.flush()


def get_sample_dataframe_from_hdf5(sample_group: h5py.Group, layer_key: str) -> pd.DataFrame:
    """
    Extract sample metadata from the HDF5 file.

    Args:
        sample_group (h5py.Group): Group where sample metadata is located in the HDF5 file.

    Returns:
        pd.DataFrame: DataFrame with metadata columns (single row, since metadata is sample-wide).
    """
    metadata = {}

    # Iterate through all subgroups in the sample group
    for subgroup_name, subgroup in sample_group.items():
        if isinstance(subgroup, h5py.Group):
            if "HT_type" in subgroup.attrs and subgroup.attrs["HT_type"] == "annealing":
                results_group = subgroup.get("results")
                if isinstance(results_group, h5py.Group):
                    if "temperature" in results_group.keys():
                        temp = results_group["temperature"]
                        if isinstance(temp, h5py.Dataset):
                            metadata["annealing_temperature (°C)"] = temp[()]
                    if "time" in results_group:
                        time = results_group["time"]
                        if isinstance(time, h5py.Dataset):
                            metadata["annealing_time (s)"] = time[()]

            # --- Layer metadata (e.g., layer_1, layer_2, ...) ---
            elif subgroup_name.startswith("layer_"):
                element = subgroup["element"][()].decode()

                if "element" in subgroup and element == layer_key:
                    if "distance" in subgroup.keys():
                        dist = subgroup["distance"][()]
                        metadata["target_distance (mm)"] = dist

                    #if "power" in subgroup.keys():
                    #    power = subgroup["power"][()]
                    #    metadata["magnetron_power"] = power

                    if "time" in subgroup.keys():
                        time = subgroup["time"][()]
                        metadata["deposition_time (s)"] = time

    # Return as a single-row DataFrame (metadata is sample-wide)
    return pd.DataFrame([metadata]) if metadata else pd.DataFrame()