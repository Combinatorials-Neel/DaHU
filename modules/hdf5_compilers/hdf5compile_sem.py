"""
Functions for SEM image parsing
"""

import stringcase
import xml.etree.ElementTree as et

from ..functions.functions_moke import *
from ..hdf5_compilers.hdf5compile_base import *

SEM_WRITER_VERSION = '0.1'

POSITION_DECIMAL_ROUND_NUMBER = 3


def get_position_from_path(filepath):
    """
    Extracts the scan numbers (x and y indices) from the filename of the given
    filepath.

    Args:
        filepath (str): Name of the file containing position information with the format (x, y)

    Returns:
        tuple: A tuple containing the x and y indices of the scan
    """
    if isinstance(filepath, Path):
        filepath = str(filepath)

    pattern = r".*\((\d+),(\d+)\).*"
    match = re.search(pattern, filepath)
    x_idx = match.group(1)
    y_idx = match.group(2)

    return int(x_idx), int(y_idx)


def find_max_idx(source_path):
    max_x = 0
    max_y = 0
    for file_name in safe_rglob(source_path, pattern="*.png"):
        file_path = source_path / file_name
        scan_numbers = get_position_from_path(file_path)
        if scan_numbers[0] > max_x:
            max_x = scan_numbers[0]
        if scan_numbers[1] > max_y:
            max_y = scan_numbers[1]

    return max_x, max_y


def calculate_wafer_positions(
    scan_numbers, start_x=-40, start_y=-40, end_x=40, end_y=40, max_idx_x=17, max_idx_y=17
):
    """
    Calculates the wafer positions based on scan numbers and specified step and start values.

    Args:
        scan_numbers (tuple): A tuple containing the x and y indices of the scan.
        start_x (int, optional): The starting position in the x direction. Defaults to -40.
        start_y (int, optional): The starting position in the y direction. Defaults to -40.
        end_x (int, optional): The ending position in the x direction. Defaults to 40.
        end_y (int, optional): The ending position in the y direction. Defaults to 40.

    Returns:
        tuple: A tuple containing the calculated x and y positions on the wafer.
    """
    # Only valid if +X +Y direction scan is selected in the EDX scan and motors axis are aligned with wafer axis
    x_idx, y_idx = scan_numbers
    step_x = (np.abs(start_x) + np.abs(end_x)) / (max_idx_x - 1)
    step_y = (np.abs(start_y) + np.abs(end_y)) / (max_idx_y - 1)

    x_pos, y_pos = -((x_idx - 1) * step_x + start_x), (y_idx - 1) * step_y + start_y

    return float(x_pos), float(y_pos)

def write_sem_to_hdf5(hdf5_path, source_path, dataset_name):
    if isinstance(hdf5_path, str):
        hdf5_path = Path(hdf5_path)
    if isinstance(source_path, str):
        source_path = Path(source_path)

    if dataset_name is None:
        dataset_name = source_path.stem

    with h5py.File(hdf5_path, "a") as hdf5_file:
        sem_group = hdf5_file.create_group(dataset_name)
        sem_group.attrs["HT_type"] = "sem"
        sem_group.attrs["instrument"] = "Zeiss Ultra Plus"
        sem_group.attrs["sem_writer"] = SEM_WRITER_VERSION

        initialize_dataset_group(sem_group)
        positions_group = sem_group.get("positions")

        max_x, max_y = find_max_idx(source_path)

        for file_name in safe_rglob(source_path, pattern="*.png"):
            file_path = source_path / file_name

            scan_numbers = get_position_from_path(file_path)
            wafer_positions = calculate_wafer_positions(scan_numbers, max_idx_x=max_x, max_idx_y=max_y)

            position_group = positions_group.create_group(
                f"({wafer_positions[0]},{wafer_positions[1]})"
            )
            position_group.attrs["index"] = scan_numbers
            position_group.attrs["ignored"] = False

            # Instrument group for metadata
            instrument = position_group.create_group("instrument")
            instrument.attrs["HT_class"] = "HT_instrument"

            instrument["x_pos"] = format_position_value(wafer_positions[0])
            instrument["y_pos"] = format_position_value(wafer_positions[1])
            instrument["x_pos"].attrs["units"] = "mm"
            instrument["y_pos"].attrs["units"] = "mm"

            # Measurement group
            measurement_group = position_group.create_group("measurement")
            measurement_group.attrs["HT_class"] = "HT_measurement"

            img = np.array(Image.open(file_path))
            measurement_group.create_dataset("image", data=img, compression="gzip")