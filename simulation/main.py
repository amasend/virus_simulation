import pandas as pd
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from simulation.individuals import Individual

import plotly.express as px

start = pd.DataFrame([[50.061, 19.923]], columns=['lat', 'lon'])
token = open("/home/amadeusz/PycharmProjects/virus_simulation/simulation/mapbox_token").read()
fig = px.scatter_mapbox(start, lat="lat", lon="lon",
                        color_discrete_sequence=["fuchsia"], zoom=3, height=300)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, autosize=True,
                  height=900, width=900)

individuals = [Individual(start_infection_probability=0.01, infection_probability=0.8) for i in range(200)]
infected = []
healthy = []

for individual in individuals:
    if individual.infected:
        infected.append(individual)

    else:
        healthy.append(individual)

graph_2_x = [0]
graph_2_y_infected = [len(infected)]
graph_2_y_healthy = [len(healthy)]

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app = dash.Dash(__name__)
app.layout = html.Div(
    style={'backgroundColor': colors['background']},
    children=html.Div([
        dcc.Interval(
            id='graph-update',
            interval=1 * 1000
        ),
        html.Div([
            html.H3('Column 1'),
            dcc.Graph(id='live-graph',
                      style={
                          'background-image': 'url(/home/amadeusz/PycharmProjects/virus_simulation/simulation/krakow_map.png)'},
                      animate=True,
                      figure={
                          'data': [
                              {'x': [individual.x for individual in infected],
                               'y': [individual.y for individual in infected],
                               'type': 'scatter',
                               'mode': 'markers',
                               'name': 'Infected',
                               'marker': {'color': 'red',
                                          'size': 10}
                               },
                              {'x': [individual.x for individual in healthy],
                               'y': [individual.y for individual in healthy],
                               'type': 'scatter',
                               'mode': 'markers',
                               'name': u'Healthy',
                               'marker': {'color': 'blue',
                                          'size': 5}
                               },
                          ],
                          'layout': {
                              # 'plot_bgcolor': colors['background'],
                              'plot_bgcolor': 'rgba(0,0,0,0)',
                              'paper_bgcolor': 'rgba(0,0,0,0)',
                              # 'paper_bgcolor': colors['background'],

                              'font': {
                                  'color': colors['text']
                              },
                              'autosize': True,
                              'height': 900,
                              'xaxis': dict(range=[0, 1000]),
                              'yaxis': dict(range=[0, 1000])
                          }
                      })
        ], className="six columns"),
        html.Div([
            html.H3('Column 2', style={'fontColor': colors['text']}),
            dcc.Graph(id='live-graph_2',
                      animate=True,
                      figure={
                          'data': [
                              {'x': graph_2_x,
                               'y': graph_2_y_infected,
                               'type': 'scatter',
                               'name': 'Infected count',
                               'marker': {'color': 'red'}
                               },
                              {'x': graph_2_x,
                               'y': graph_2_y_healthy,
                               'type': 'scatter',
                               'name': u'Healthy count',
                               'marker': {'color': 'blue'}
                               },
                          ],
                          'layout': {
                              'plot_bgcolor': colors['background'],
                              'paper_bgcolor': colors['background'],
                              'font': {
                                  'color': colors['text']
                              },
                              'autosize': True,
                              'height': 900,
                              'xaxis': dict(range=[0, len(graph_2_x)]),
                              'yaxis': dict(range=[0, graph_2_y_infected[0] + graph_2_y_healthy[0]])
                          }
                      })
        ], className="six columns"),
        html.Div([
            html.H3('Column 3', style={'fontColor': colors['text']}),
            dcc.Graph(id='live-graph_3',
                      animate=True,
                      figure={
                          'data': fig.data,
                          'layout': fig.layout
                      })
        ], className="six columns"),
    ], className='row', style={"columnCount": 2})
)


@app.callback(Output('live-graph_3', 'figure'), inputs=[Input('graph-update', 'n_intervals')])
def update_graph_map(interval):
    for individual in individuals:
        individual.move()
        if not individual.infected:
            individual.check_infection(individuals=individuals)

            if individual.infected:
                infected.append(individual)

    data_infected = pd.DataFrame(data={'lon': [individual.x for individual in infected],
                                       'lat': [individual.y for individual in infected]})

    data_healthy = pd.DataFrame(data={'lon': [individual.x for individual in healthy],
                                      'lat': [individual.y for individual in healthy]})

    fig_1 = px.scatter_mapbox(data_infected, lat="lat", lon="lon")
    fig_1.update_layout(mapbox_style="open-street-map")

    fig_2 = px.scatter_mapbox(data_healthy, lat="lat", lon="lon")
    fig_2.update_layout(mapbox_style="open-street-map")

    data = [
        fig_1.data[0],
        fig_2.data[0]
    ]

    return {'data': data}


@app.callback(Output('live-graph', 'figure'), inputs=[Input('graph-update', 'n_intervals')])
def update_graph_scatter(interval):
    for individual in individuals:
        individual.move()
        if not individual.infected:
            individual.check_infection(individuals=individuals)

            if individual.infected:
                infected.append(individual)

    data = [
        plotly.graph_objs.Scatter(
            x=[individual.x for individual in infected],
            y=[individual.y for individual in infected]
        ),
        plotly.graph_objs.Scatter(
            x=[individual.x for individual in healthy],
            y=[individual.y for individual in healthy]
        )]

    return {'data': data}


@app.callback(Output('live-graph_2', 'figure'), inputs=[Input('graph-update', 'n_intervals')])
def update_graph_2(interval):
    graph_2_x.append(graph_2_x[-1] + 1)
    graph_2_y_infected.append(len(infected))
    graph_2_y_healthy.append(graph_2_y_infected[0] + graph_2_y_healthy[0] - len(infected))

    data = [
        plotly.graph_objs.Scatter(
            x=graph_2_x,
            y=graph_2_y_infected,
            marker={'color': 'red'},
            name='Infected count',
        ),
        plotly.graph_objs.Scatter(
            x=graph_2_x,
            y=graph_2_y_healthy,
        )]

    return {'data': data,
            'layout': go.Layout(xaxis=dict(range=[0, len(graph_2_x)]),
                                )}


app.run_server(debug=True)

"""
50.097,19.822       50.097,20.033
49.885,19.822       49.885,20.033
"""
