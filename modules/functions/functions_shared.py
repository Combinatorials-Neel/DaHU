import functools
import os.path
import re
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
from scipy.stats import linregress
from io import StringIO


# Decorator function to check conditions before executing callbacks, preventing errors
def check_conditions(conditions_function, hdf5_path_index):
    def decorator(callback_function):
        @functools.wraps(callback_function)
        def wrapper(*args, **kwargs):
            args = list(args)
            args[hdf5_path_index] = Path(args[hdf5_path_index])
            hdf5_path = args[hdf5_path_index]
            if not conditions_function(hdf5_path, *args, **kwargs):
                raise PreventUpdate
            return callback_function(*args, **kwargs)
        return wrapper
    return decorator


def cleanup_file(path):
    try:
        os.remove(path)
    except OSError:
        pass


def cleanup_directory(folderpath):
    try:
        for folder in os.listdir(folderpath):
            full_path = os.path.join(folderpath, folder)
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
    except FileNotFoundError:
        os.makedirs(folderpath)


def safe_glob(directory, pattern="*"):
    return [
        f
        for f in directory.glob(pattern)
        if f.is_file() and not (f.name.startswith(".") or f.name.startswith("._"))
    ]


def safe_rglob(directory, pattern="*"):
    return [
        f
        for f in directory.rglob(pattern)
        if f.is_file() and not f.name.startswith(".") and not f.name.startswith("._")
    ]


def is_macos_system_file(file_path):
    if type(file_path) is str:
        print(file_path)
        if "/._" not in file_path and not file_path.startswith("._"):
            return False
        else:
            return True
    if type(file_path) is Path:
        print(file_path.name)
        if not file_path.name.startswith("._"):
            return False
        else:
            return True


def unpack_zip_directory(filename_list: list, depth: int, remove_directories=True):
    for filename in filename_list:
        if filename.count("/") != depth:
            filename_list.remove(filename)
        elif remove_directories and filename.endswith("/"):
            filename_list.remove(filename)

    return filename_list


def detect_measurement(filename_list: list):
    """
    Scan a folder to determine which type of measurement it is

    Parameters:
        filename_list (list): list containing all filenames to parse

    Returns:
        version (str): detected measurement type
    """
    measurement_dict = {
        "XRD": ["ras"],
        "MOKE": ["log"],
        "EDX": ["spx"],
        "PROFIL": ["asc2d"],
        "ESRF": ["h5"],
        "XRD results": ["lst"],
        "Annealing": ["HIS"],
        "Magnetron": ["prp"],
        "SQUID": ["dat"]
    }

    for measurement_type, file_type in measurement_dict.items():
        for filename in filename_list:
            if filename.startswith("."):  # Skip hidden files
                continue
            if (
                filename.split(".")[-1] in file_type
            ):  # Check extensions for correspondence to the dictionary spec
                depth = filename.count("/")
                return measurement_type, depth
    return None

def heatmap_layout(title=""):
    """
    Generates a standardized layout for all heatmaps.

    Parameters:
        title (str): The title of the plot.

    Returns:
        go.Layout(): layout object that can be passed to a figure
    """
    layout = go.Layout(
        title=dict(text=title, font=dict(size=24)),
        xaxis=dict(
            title="X (mm)",
            tickfont=dict(size=24),
            title_font=dict(size=20),
            range=[-43, 43],
            tickmode="linear",
            tick0=-40,
            dtick=10,
        ),
        yaxis=dict(
            title="Y (mm)",
            tickfont=dict(size=24),
            title_font=dict(size=20),
            range=[-43, 43],
            tickmode="linear",
            tick0=-40,
            dtick=10,
        ),
        height=800,
        width=850,
        margin=dict(r=100, t=100),
    )
    return layout


def plot_layout(title="", showlegend=False):
    """
    Generates a standardized layout for all plots.

    Parameters:
        title (str): The title of the plot.
        showlegend (bool): Whether to show the legend.

    Returns:
        go.Layout(): layout object that can be passed to a figure
    """
    layout = go.Layout(
        height=750,
        width=1100,
        title=dict(text=title, font=dict(size=24)),
        xaxis=dict(
            tickfont=dict(size=18),
            title_font=dict(size=20),
        ),
        yaxis=dict(
            tickfont=dict(size=18),
            title_font=dict(size=20),
        ),
        showlegend=showlegend,
    )
    return layout


def colorbar_layout(z_min, z_max, precision=0, title=""):
    """
    Generates a standardized colorbar.

    Parameters:
        z_min : minimum value on the colorbar
        z_max : maximum value on the colorbar
        precision: number of digits on the colorbar scale
        title (str): The title of the plot.

    Returns:
        colorbar (dict): dictionary of colorbar parameters that can be passed to a figure
    """
    z_mid = (z_min + z_max) / 2
    colorbar = dict(
        title=dict(text=f"{title} <br>&nbsp;<br>", font=dict(size=20)),
        tickfont=dict(size=22),
        tickvals=[
            z_min,
            (z_min + z_mid) / 2,
            z_mid,
            (z_max + z_mid) / 2,
            z_max,
        ],  # Tick values
        ticktext=[
            f"{z_min:.{precision}f}",
            f"{(z_min + z_mid) / 2:.{precision}f}",
            f"{z_mid:.{precision}f}",
            f"{(z_max + z_mid) / 2:.{precision}f}",
            f"{z_max:.{precision}f}",
        ],  # Tick text
    )
    return colorbar


def significant_round(num, sig_figs):
    """
    Rounds a number to a specified number of significant figures.

    Parameters:
        num (float): The number to round.
        sig_figs (int): The number of significant figures to round to.

    Returns:
        float: The rounded number.
    """
    # Handle 0 and nan
    if num == 0:
        return 0
    if np.isnan(num):
        return np.nan

    # Calculate the factor to shift the decimal point
    shift_factor = np.power(10, sig_figs - np.ceil(np.log10(abs(num))))

    # Shift number, round, and shift back
    return round(num * shift_factor) / shift_factor


def derivate_dataframe(df, column):
    """
    Add a column to a dataframe that is the discrete derivative of another column

    Parameters:
        df (pandas.DataFrame): dataframe to apply the function
        column (str): The name of the column from which to calculate the derivative

    Returns:
        pandas.DataFrame: The initial dataframe with an additional 'Derivative' column
    """
    # Ensure the DataFrame has the column 'Total Profile (nm)'
    if column not in df.columns:
        raise ValueError(f"The DataFrame must contain a 'f{column}' column.")
    # Calculate point to point derivative
    df["derivative"] = df[column].diff().fillna(0)
    return df


def calc_poly(coefficient_list, x_end, x_start=0, x_step=1):
    """
    Evaluate an n-degree polynomial using Horner's method. Works with arrays, returning P(x) for every x within
    range [x_start, x_end].

    Parameters:
        coefficient_list (list or numpy array): list of coefficients such that list[i] is the i-order coefficient
        x_end (int): end of the x_range on which to evaluate the polynomial
        x_start (int): start of the x_range on which to evaluate the polynomial
        x_step (int): step size of the x_range on which to evaluate the polynomial

    Returns:
        np.array: P(x) for every x within range [x_start, x_end]
    """
    x = np.arange(x_start, x_end, x_step)
    result = np.zeros_like(x, dtype=np.float64)

    for coefficient in reversed(coefficient_list):
        result = result * x + coefficient

    return result


def make_heatmap_from_dataframe(
    df,
    values=None,
    z_min=None,
    z_max=None,
    precision=2,
    plot_title="",
    colorbar_title="",
    masking=False,
    colorscale="Plasma",
    scaling=1,
):
    if values is None:
        df["default"] = df["x_pos (mm)"] + df["y_pos (mm)"]
        values = "default"
        plot_title = "No heatmap selected, default values"

    heatmap_data = df.pivot_table(
        index="y_pos (mm)",
        columns="x_pos (mm)",
        values=values,
    )

    if "default" in df.columns:
        df.drop("default", axis="columns", inplace=True)

    # If mask is set, hide points that have an ignore tag in the database
    if masking:
        # Create a mask to hide ignored points
        mask_data = df.pivot_table(
            index="y_pos (mm)", columns="x_pos (mm)", values="ignored"
        )
        # Ignore points
        mask = mask_data == False

        heatmap_data = heatmap_data.where(mask, np.nan)

    if z_min is None:
        z_min = np.nanmin(heatmap_data.values * scaling)
    if z_max is None:
        z_max = np.nanmax(heatmap_data.values * scaling)

    heatmap = go.Heatmap(
        x=heatmap_data.columns,
        y=heatmap_data.index,
        z=heatmap_data.values * scaling,
        colorscale=colorscale,
        # Set ticks for the colorbar
        colorbar=colorbar_layout(z_min, z_max, precision, title=colorbar_title),
    )

    # Make and show figure
    fig = go.Figure(data=[heatmap], layout=heatmap_layout(title=plot_title))

    if z_min is not None:
        fig.data[0].update(zmin=z_min)
    if z_max is not None:
        fig.data[0].update(zmax=z_max)

    return fig


def pairwise(list):
    a = iter(list)
    return zip(a, a)


def get_target_position_group(measurement_group, target_x, target_y):
    for position, position_group in measurement_group.items():
        instrument_group = position_group.get("instrument")
        if (
            instrument_group["x_pos"][()] == target_x
            and instrument_group["y_pos"][()] == target_y
        ):
            return position_group


def abs_mean(value_list):
    return np.mean(np.abs(value_list))


def convert_bytes(target):
    try:
        return float(target)
    except ValueError:
        return target.decode("utf-8")


def split_name_and_unit(name_str):
    split = name_str.split("_")
    name = "_".join(split[:-1])
    unit = split[-1]
    return name, unit

def remove_zero_columns(df):
    df = df.loc[:, (df != 0).any(axis=0)]
    return df


def extract_value_unit(str):
    """
    Use regex to extract values and units from a string, provided the format is 'value(unit)'
    If no unit is found, unit is returned as None
    """
    match = re.match(r'^(.*?)\s*(?:\(([^)]+)\))?$', str)
    if match:
        value = match.group(1).strip()
        unit = match.group(2)
        return {"value" : value, "units" : unit}

def linear_fit(df, x_col, y_col):
    x = df[x_col]
    y = df[y_col]
    result = linregress(x, y)
    print(f"Slope: {result.slope}")
    print(f"Intercept: {result.intercept}")
    print(f"R-squared: {result.rvalue**2}")
    return result