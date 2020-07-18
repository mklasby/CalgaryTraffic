from dash.dependencies import Input, Output

from app import app


@app.callback(
    Output('content', 'children'),
    [Input('data_selection', 'value'),
     Input('year_selection', 'value'), ])
def display_selection(data, year):
    return f"You have selected {data} for {year}"


@ app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)


@ app.callback(
    Output('app-2-display-value', 'children'),
    [Input('app-2-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
