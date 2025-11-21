from collections import defaultdict

import h5py

from modules.hdf5_compilers.hdf5compile_base import create_incremental_group, safe_create_new_subgroup


def write_library_to_dataset_hdf5(library_path, dataset_path, copy_type="soft"):
    with h5py.File(library_path, "r") as library_file:
        with h5py.File(dataset_path, "r+") as dataset_file:
            # Check provided filetypes
            if library_file.attrs["HT_type"] != "library":
                raise TypeError("Provided Library file is not of type 'library')")
            elif dataset_file.attrs["HT_type"] != "dataset":
                raise TypeError("Provided Dataset file is not of type 'dataset')")

            # Collect all datasets and their types
            dataset_dict = defaultdict(None)
            for dataset, dataset_group in library_file.items():
                dataset_dict[dataset_group.attrs["HT_type"]] = dataset

            # Assign datasets
            edx_group = library_file.get(dataset_dict["edx"])
            moke_group = library_file.get(dataset_dict["moke"])
            profil_group = library_file.get(dataset_dict["profil"])
            xrd_group = library_file.get(dataset_dict["xrd"])

            sample_group = library_file["sample"]
            sample_name = sample_group["sample_name"][()]

            # List all positions present in datasets
            edx_positions = edx_group.keys()
            moke_positions = moke_group.keys()
            profil_positions = profil_group.keys()
            xrd_positions = xrd_group.keys()

            # Return a list of positions that all have data points
            position_list = list(set(edx_positions) & set(moke_positions) & set(profil_positions) & set(xrd_positions))

            for position in position_list:
                edx_position_group = edx_group[position]
                moke_position_group = moke_group[position]
                profil_position_group = profil_group[position]
                xrd_position_group = xrd_group[position]

                position_group = create_incremental_group(dataset_file, f"[{sample_name}]")

                edx_position_group.copy(position_group)
                moke_position_group.copy(position_group)
                profil_position_group.copy(position_group)
                xrd_position_group.copy(position_group)

                position_group.create_group("sample")

            samples_group = dataset_file["samples"]
            sample_group.create_group(f"{sample_name}")

            dataset_file.flush()
        library_file.flush()






