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

def widget_measurement_found(date, httype):
    widget = html.Div(
        id="hdf5_deposition_state",
        className="section-2",
        children=[
            html.Div(f"{httype}"),
            html.Div(f"{date}")
        ],
        style = {
            "background-color": "#3D994C",
        }
    )
    return widget