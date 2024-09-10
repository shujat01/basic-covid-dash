import numpy as np 
import pandas as pd 
import plotly.graph_objs as go 
import dash
from dash import html
from dash import dcc 
from dash.dependencies import Input,Output


external_stylesheets = [
    {
        "href": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH",
        "crossorigin": "anonymous"
    }
]

patients=pd.read_csv('IndividualDetails.csv')

total=patients.shape[0]
active=patients[patients['current_status']=='Hospitalized'].shape[0]
recovered=patients[patients['current_status']=='Recovered'].shape[0]
deaths=patients[patients['current_status']=='Deceased'].shape[0]

options=[
    {'label':'All','value':'All'},
    {'label':'Hospitalized','value':'Hospitalized'},
    {'label':'Recovered','value':'Recovered'},
    {'label':'Deceased', 'value':'Deceased'}
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server

app.layout=html.Div([
    html.H1("Corona Virus Pandemic",style={'color':'#fff','text-align':'center'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases",className='text-light'),
                    html.H4(total,className='text-light')
                ],className='card-body')
            ],className='card bg-danger')
        ],className='col-md-3'),
        html.Div([html.Div([
                html.Div([
                    html.H3("Active Cases",className='text-light'),
                    html.H4(active,className='text-light')
                ],className='card-body')
            ],className='card bg-info')],className='col-md-3'),
        html.Div([html.Div([
                html.Div([
                    html.H3("Recovered",className='text-light'),
                    html.H4(recovered,className='text-light')
                ],className='card-body')
            ],className='card bg-warning')],className='col-md-3'),
        html.Div([html.Div([
                html.Div([
                    html.H3("Death",className='text-light'),
                    html.H4(deaths,className='text-light')
                ],className='card-body')
            ],className='card bg-success')],className='col-md-3')
    ],className='row'),
    html.Div([],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker',options=options,value='All'),
                    dcc.Graph(id='bar')
                ],className='card-body')
            ],className='card')
        ],className='col-md-12')
    ],className='row')
],className='container')

@app.callback(Output('bar','figure'),[Input('picker','value')])  
def update_graph(type):
    if type=='All':
        pbar=patients['detected_state'].value_counts().reset_index()
        return {'data':[go.Bar(x=pbar['detected_state'],y=pbar['count'])],
             'layout':go.Layout(title='State Total Counts')}
    else:
        npat=patients[patients['current_status']==type]
        pbar=npat['detected_state'].value_counts().reset_index()
        return {'data':[go.Bar(x=pbar['detected_state'],y=pbar['count'])],
             'layout':go.Layout(title='State Total Counts')}





if __name__=="__main__":
    app.run_server(port=8052,debug=True)