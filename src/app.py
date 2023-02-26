import dash
import dash_html_components as html
import dash_core_components as dcc
from main import prompt_df, page_numbers_lst
from gpt3_code import generate_text
from lite4 import  store_result

app = dash.Dash()
server = app.server

app.layout = html.Div([
    html.Button('Submit Page', id='submit-page-button'),
    html.Div(id='input-container', children=[
        html.Label('Page Number'),
        dcc.Dropdown(
            id='page-number-dropdown',
            options=[{'label': str(i), 'value': i} for i in prompt_df['page_number'].unique()],
            value=None
        )
#        dcc.Input(id='input-field', type='text', placeholder='Enter page number')

    ]),
    html.Button('Positive Things', id='positive-button'),
    html.Button('Negative Things', id='negative-button'),
    html.Div(id='output')
])

@app.callback(
    dash.dependencies.Output('output', 'children'),
    [dash.dependencies.Input('positive-button', 'n_clicks'),
     dash.dependencies.Input('negative-button', 'n_clicks'),
     dash.dependencies.Input('page-number-dropdown', 'value')],
    [dash.dependencies.State('output', 'children')]
)
def output(n_clicks_positive, n_clicks_negative, page_number, state):
    ctx = dash.callback_context
    if ctx.triggered:
        trigger = ctx.triggered[0]['prop_id']
    else:
        raise dash.exceptions.PreventUpdate

    if page_number is None:
        return state

    page_number = int(page_number)
    try:
        if 'positive-button' in trigger:
            prompt = prompt_df[prompt_df['page_number'] == page_number]['positive_prompt'].values[0]
        elif 'negative-button' in trigger:
            prompt = prompt_df[prompt_df['page_number'] == page_number]['negative_prompt'].values[0]
        else:
            prompt = None  # Set prompt to None if buttons are not clicked

        if prompt is not None:  # Check if prompt is defined
            text = generate_text(prompt)
            store_result(page_number, "positive" if "positive-button" in trigger else "negative", text)

            return html.Div([html.Pre(text)])
        else:
            return state

    except IndexError:
        return 'This page do not belong to Management Discussion and Analysis'

if __name__ == '__main__':
    app.run_server(debug=True)
