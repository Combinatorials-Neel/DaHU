"""
Functions for deposition parsing (RTA)
"""

from ..functions.functions_shared import *
from ..hdf5_compilers.hdf5compile_base import *

MAGNETRON_WRITER_VERSION = '0.1'
TRIODE_WRITER_VERSION = '0.1'

magnetron_measurement_units_dict = {
    "time" : "s",
    "MP11 pressure" : "mbar",
    "M11 pressure" : "mbar",
    "M21 pressure" : "mbar",
    "RF1 sputtering power" : "W",
    "RF1 reflected power" : "W",
    "RF1 voltage" : "V",
    "accord" : "%",
    "charge" : "%",
    "DC1 current" : "A",
    "DC1 power" : "W",
    "DC1 voltage" : "V",
    "DC2 current" : "A",
    "DC2 power" : "W",
    "DC2 voltage" : "V",
    "Substrate holder temperature" : "°C",
    "DG11 gaz flow" : "sccm",
    "DG12 gaz flow" : "sccm",
    "DG13 gaz flow" : "sccm",
}


def read_prp_line(prp_line):
    split = prp_line.split("\t")
    prp_dict = {
        "step number": split[0],
        "step type": split[1],
        "step name": split[2].split("-")[0].strip(),
        "step comment": split[3]
    }
    for index, entry in enumerate(split[4:-1], start=1):
        prp_dict[f"entry {index}"] = entry

    return prp_dict


def translate_prp_dict(prp_dict):
    # Assigning specific to pumping steps
    if prp_dict["step type"] == "1":
        prp_dict["target pressure (mbar)"] = prp_dict.pop(
            "step comment")  # pumping steps can't have comments, so index 3 is directly the value

    # Assigning specific to (pre)pulverisation steps
    pulverisation_dict = {
        "entry 1": "",
        "entry 2": "",
        "entry 3": "argon flow (sccm)",
        "entry 4": "",
        "entry 5": "sputtering time (s)",
        "entry 6": "",
        "entry 7": "",
        "entry 8": "substrate position",
        "entry 9": "",
        "entry 10": "",
        "entry 11": "",
        "entry 12": "target-substrate distance (mm)",
        "entry 13": "",
        "entry 14": "",
        "entry 15": "",
        "entry 16": "",
        "entry 17": "RF power (W)",
        "entry 18": "",
        "entry 19": "",
        "entry 20": "",
        "entry 21": "",
        "entry 22": "",
        "entry 23": "",
        "entry 24": "",
        "entry 25": "",
        "entry 26": "",
        "entry 27": "",
        "entry 28": "",
        "entry 29": "",
        "entry 30": "",
        "entry 31": "",
        "entry 32": "",
        "entry 33": "",
        "entry 34": "",
        "entry 35": "",
        "entry 36": "",
        "entry 37": "",
        "entry 38": "",
        "entry 39": "",
        "entry 40": ""
    }

    if prp_dict["step type"] in ["3", "4"]:
        for old_key, new_key in pulverisation_dict.items():
            if new_key != "":
                prp_dict[new_key] = prp_dict.pop(old_key)

    return prp_dict


def format_measurement_df_magnetron(df):
    df.drop("Date et heure", axis=1, inplace=True)
    df["time"] = df.index * 2

    translation_dict = {
        " Jauge MP11 (mbar)": "MP11 pressure",
        " Jauge M11 (mbar)": "M11 pressure",
        " Jauge MP21 (mbar)": "M21 pressure",
        " Puissance incidente RF1 (W)": "RF1 sputtering power",
        " Puissance reflechie RF1 (W)": "RF1 reflected power",
        " Tension RF1 (V)": "RF1 voltage",
        " Accord (%)": "accord",
        " Charge (%)": "charge ",
        " Courant DC1 (A)": "DC1 current",
        " Puissance DC1 (W)": "DC1 power",
        " Tension DC1 (V)": "DC1 voltage",
        " Courant DC2 (A)": "DC2 current",
        " Puissance DC2 (W)": "DC2 power",
        " Tension DC2 (V)": "DC2 voltage",
        " Temperature PS (°C)": "Substrate holder temperature",
        " Debit gaz DG11 (sccm)": "DG11 gaz flow",
        " Debit gaz DG12 (sccm)": "DG12 gaz flow",
        " Debit gaz DG13 (sccm)": "DG13 gaz flow",
        "Cache1": "target 1 cover",
        "Cache2": "target 2 cover",
        "Cache3": "target 3 cover",
        "Cache4": "target 4 cover",
        "Cache5": "target 5 cover",
        "Cache6": "target 6 cover",
        "Cache7": "target 7 cover",
        "Cache8": "target 8 cover",
    }

    df.rename(columns=translation_dict, inplace=True)

    return df


def read_measurement_df_magnetron(file_path):
    df = pd.read_csv(file_path, encoding="ANSI", skiprows=1)
    df = df.loc[:, (df != 0).any(axis=0)]
    df = remove_zero_columns(df)

    df = format_measurement_df_magnetron(df)

    return df


def read_prp_from_magnetron(prp_path):
    with open(prp_path, "r") as file:
        lines = file.readlines()

    final_dict = {}

    for line in lines:
        if line.startswith("STEP"):
            prp_dict = read_prp_line(line)
            prp_dict = translate_prp_dict(prp_dict)
            print(prp_dict)
            step_number = prp_dict.pop("step number")
            final_dict[step_number] = prp_dict

    return final_dict


def write_magnetron_to_hdf5(hdf5_path, source_path, deposition_dict):
    source_path = Path(source_path)
    for file_path in safe_glob(source_path, ".txt"):
        measurement_df = read_measurement_df_magnetron(file_path)
    for file_path in safe_glob(source_path, ".prp"):
        instrument_dict = read_prp_from_magnetron(file_path)

    with h5py.File(hdf5_path, "a") as hdf5_file:
        deposition_group = hdf5_file.create_group("deposition")
        deposition_group.attrs["HT_type"] = "magnetron"
        deposition_group.attrs["instrument"] = "AllianceConcept DP850"
        deposition_group.attrs["magnetron_writer"] = MAGNETRON_WRITER_VERSION

        instrument_group = deposition_group.create_group("instrument")
        save_dict_to_hdf5(instrument_group, instrument_dict)

        measurement_group = deposition_group.create_group("measurement")
        dataframe_to_hdf5(measurement_df, measurement_group)
        hdf5_units_from_dict(magnetron_measurement_units_dict, measurement_group)

    return True