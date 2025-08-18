"""
"""
from ..functions.functions_hdf5 import *
from ..functions.functions_shared import *


def edx_conditions(hdf5_path, *args, **kwargs):
    if hdf5_path is None:
        return False
    if not h5py.is_hdf5(hdf5_path):
        return False
    with h5py.File(hdf5_path, "r") as hdf5_file:
        dataset_list = get_hdf5_datasets(hdf5_file, dataset_type="edx")
        if len(dataset_list) == 0:
            return False
    return True


def get_quantified_elements(edx_group):
    element_list = []

    for position, position_group in edx_group.items():
        results_group = position_group.get('results')

        if results_group is None:
            continue

        for element, element_group in results_group.items():
            if 'AtomPercent' in element_group and element not in element_list:
                element_list.append(element)

    return element_list


def edx_make_results_dataframe_from_hdf5(edx_group):
    data_dict_list = []

    for position, position_group in edx_group.items():
        instrument_group = position_group.get('instrument')
        # Exclude spots outside the wafer
        if np.abs(instrument_group["x_pos"][()]) + np.abs(instrument_group["y_pos"][()]) <= 60:

            results_group = position_group.get('results')

            data_dict = {"x_pos (mm)": instrument_group["x_pos"][()],
                         "y_pos (mm)": instrument_group["y_pos"][()],
                         "ignored": position_group.attrs["ignored"]}

            if results_group is None:
                continue

            for element, element_group in results_group.items():
                if 'AtomPercent' in element_group:
                    data_dict[element] = element_group['AtomPercent'][()]
            data_dict_list.append(data_dict)

    result_dataframe = pd.DataFrame(data_dict_list)

    return result_dataframe


def edx_get_measurement_from_hdf5(edx_group, target_x, target_y):
    position_group = get_target_position_group(edx_group, target_x, target_y)
    measurement_group = position_group.get('measurement')

    energy_array = measurement_group['energy'][()]
    counts_array = measurement_group['counts'][()]

    spectrum_dataframe = pd.DataFrame({"Energy (keV)": energy_array, "Counts": counts_array})

    return spectrum_dataframe


def edx_plot_measurement_from_dataframe(df):
    fig = go.Figure(layout = plot_layout(''))

    fig.update_xaxes(title_text="Energy (keV)")
    fig.update_yaxes(title_text="Counts")

    fig.add_trace(
        go.Scatter(
            x=df['Energy (keV)'],
            y=df['Counts'],
            mode='lines',
            line=dict(color="SlateBlue", width=3),
        )
    )

    return fig

def edx_plot_element_rays(fig, elements_dict):
    for element in elements_dict.keys():
        for energy in elements_dict[element]["energies"]:
            fig.add_vline(x=energy, line_width=3, line_color=elements_dict[element]["color"], line_dash="dash",
                          annotation_text=element, annotation_position="top right", annotation_font_size=20)

    return fig