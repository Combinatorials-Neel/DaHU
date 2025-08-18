from dash import html, dcc

def widget_title_card(title):
    widget = html.Div(
        className="section-1",
        children=[title]
    )
    return widget
def widget_measurement_missing():
    widget = html.Div(
        id="hdf5_deposition_state",
        className="section-2",
        children=["Missing measurement"],
        style = {
            "background-color": "#993D3D",
        }
    )
    return widget

def widget_manual_data(number):
    widget = html.Div(
        id="hdf5_deposition_state",
        className="section-2",
        children=[
            html.Div(f"{number} manual entries")
        ],
        style={
            "background-color": "#3D9499",
        }
    )
    return widget


def widget_measurement_found(number):
    widget = html.Div(
        id="hdf5_deposition_state",
        className="section-2",
        children=[
            html.Div(f"{number} measurements")
        ],
        style = {
            "background-color": "#3D994C",
        }
    )
    return widget