"""
Functions for annealing parsing (RTA)
"""

from ..functions.functions_shared import *
from ..hdf5_compilers.hdf5compile_base import *

ANNEALING_WRITER_VERSION = '0.1'

annealing_measurement_units_dict = {
    "Time": "s",
    "TC1": "°C",
    "TC3": "°C",
    "Pyro": "°C",
    "Setpoint": "°C",
    "Pyro_mV": "mV",
    "Pressure": "mbar",
    "Power": "%",
    "HighVacuum": "mbar",
}

annealing_results_units_dict = {
    "max_temperature": "°C",
    "time": "s",
    "temperature": "°C",
}


def read_header_from_annealing(file_path):
    valid_fields=["Date", "Recipe", "Pyrometer calibration table"]
    header_dict = {}

    with open(file_path, "r") as file:
        lines = file.readlines()

    for line in lines[0:7]:
        newline = line.replace('"', "")
        split = newline.strip().split(",")
        key, value = split[0].strip(":"), split[-1]
        if key in valid_fields:
            header_dict[key] = value
    return header_dict


def write_annealing_to_hdf5(hdf5_path, source_path, anneal_dict, dataset_name):
    df = pd.read_csv(source_path, skiprows=7)
    df = remove_zero_columns(df)

    header_dict = read_header_from_annealing(source_path)

    if dataset_name is None:
        dataset_name = source_path.stem
    
    with h5py.File(hdf5_path, "a") as hdf5_file:
        annealing_group = hdf5_file.create_group(f"{dataset_name}")
        annealing_group.attrs["HT_type"] = "annealing"
        annealing_group.attrs["instrument"] = "JetFirst RTA"
        annealing_group.attrs["data_source"] = source_path.name
        annealing_group.attrs["annealing_writer"] = ANNEALING_WRITER_VERSION
        
        instrument_group = annealing_group.create_group("instrument")
        save_dict_to_hdf5(instrument_group, header_dict)
        
        measurement_group = annealing_group.create_group("measurement")
        dataframe_to_hdf5(df, measurement_group)
        hdf5_units_from_dict(annealing_measurement_units_dict, measurement_group)

        results_group = annealing_group.create_group("results")
        if "temperature" in anneal_dict.keys():
            results_group.create_dataset("temperature", data=anneal_dict["temperature"])
        if "time" in anneal_dict.keys():
            results_group.create_dataset("time", data=anneal_dict["time"])
        hdf5_units_from_dict(annealing_results_units_dict, results_group)
        
        
def manual_annealing_to_hdf5(hdf5_path, anneal_dict, dataset_name):
    with h5py.File(hdf5_path, "a") as hdf5_file:
        annealing_group = hdf5_file.create_group(dataset_name)
        annealing_group.attrs["HT_type"] = "annealing"
        annealing_group.attrs["instrument"] = anneal_dict["instrument"]
        annealing_group.attrs["data_source"] = "manual"
        annealing_group.attrs["annealing_writer"] = ANNEALING_WRITER_VERSION

        instrument_group = annealing_group.create_group("instrument")
        if "date" in anneal_dict.keys():
            instrument_group.create_dataset("date", data=anneal_dict["date"])

        results_group = annealing_group.create_group("results")
        if "temperature" in anneal_dict.keys():
            results_group.create_dataset("temperature", data=anneal_dict["temperature"])
        if "time" in anneal_dict.keys():
            results_group.create_dataset("time", data=anneal_dict["time"])
        hdf5_units_from_dict(annealing_results_units_dict, results_group)

    return True
    
    
    
    
    