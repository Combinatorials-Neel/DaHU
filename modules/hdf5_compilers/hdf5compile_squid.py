"""
Functions for VSM-Squid parsing
"""

from ..functions.functions_shared import *
from ..hdf5_compilers.hdf5compile_base import *

SQUID_WRITER_VERSION = "0.1"

def read_instrument_and_measurement_from_squid(file_path):
    squid_measurement_columns = ["Time Stamp (sec)", "Temperature (K)"]
    df = pd.read_csv(file_path, skiprows=44)

    instrument_df = df[[col for col in df.columns if col not in squid_measurement_columns]].copy()
    measurement_df = df[squid_measurement_columns].copy()

    # Conversion to SI units
    measurement_df["Magnetic Field (T)"] = instrument_df["Magnetic Field (Oe)"] * 1e-4
    measurement_df["Moment (A.m2)"] = instrument_df["Moment (emu)"] * 1e-3

    return instrument_df, measurement_df

def write_squid_to_hdf5(hdf5_path, source_path, info_dict, dataset_name=None, mode="a"):
    if isinstance(hdf5_path, str):
        hdf5_path = Path(hdf5_path)
    if isinstance(source_path, str):
        source_path = Path(source_path)

    if dataset_name is None:
        dataset_name = source_path.stem

    instrument_df, measurement_df = read_instrument_and_measurement_from_squid(source_path)

    with h5py.File(hdf5_path, mode) as hdf5_file:
        # Create the root group for the measurement
        if "squid" not in hdf5_file.keys():
            squid_group = hdf5_file.create_group("squid")
            squid_group.attrs["HT_type"] = "vsmsquid"
            squid_group.attrs["instrument"] = "Quantum Design MPMS3"
        else:
            squid_group = hdf5_file.get("squid")
            
        dataset_group = squid_group.create_group(f"{dataset_name}")
        dataset_group.attrs["squid_writer"] = SQUID_WRITER_VERSION

        # Sample group for sample information
        sample_group = dataset_group.create_group("sample")
        sample_group["x_pos"] = convertFloat(info_dict["x_pos"])
        sample_group["y_pos"] = convertFloat(info_dict["y_pos"])
        sample_group["surface_area"] = convertFloat(info_dict["surface_area"])
        sample_group["x_pos"].attrs["units"] = "mm"
        sample_group["y_pos"].attrs["units"] = "mm"
        sample_group["surface_area"].attrs["units"] = "cm2"

        # Instrument group for metadata
        instrument = dataset_group.create_group("instrument")
        instrument.attrs["NX_class"] = "HTinstrument"

        dataframe_to_hdf5(instrument_df, instrument, auto_units=True)

        # Measurement group for data
        measurement_group = dataset_group.create_group("measurement")
        measurement_group.attrs["NX_class"] = "HTmeasurement"

        dataframe_to_hdf5(measurement_df, measurement_group, auto_units=True)

        return None





        