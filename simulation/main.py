import pandas as pd
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from simulation.individuals import Individual

import plotly.graph_objects as gos

mapbox_access_token = open("/home/amadeusz/PycharmProjects/virus_simulation/simulation/.mapbox_token").read()

fig = gos.Figure(gos.Scattermapbox(
    lat=['50.064'],
    lon=['19.944'],
    mode='markers',
    marker=gos.scattermapbox.Marker(
        size=5
    )
))

fig.update_layout(
    autosize=True,
    paper_bgcolor='rgba(0,0,0,0)',
    hovermode='closest',
    margin=dict(l=0, r=0, t=0, b=0),
    width=1850,
    height=900,
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style='dark',
        bearing=0,
        center=dict(
            lat=50.05,
            lon=19.895
        ),
        pitch=0,
        zoom=12
    ),
)

individuals = [Individual(start_infection_probability=0.01, infection_probability=0.8) for i in range(1000)]
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
        dcc.Graph(id='live-graph',
                  # style={
                  #     'background-image': 'url(https://raw.githubusercontent.com/amasend/virus_simulation/master/simulation/krakow_map.png)',
                  #     'background-repeat': 'no-repeat',
                  #     'background-position': 'center',
                  #     'background-size': '1650px 800px',
                  # },
                  # animate=True,
                  figure=fig,
                  # figure={
                  #     'data': [
                  #         {'x': [individual.x for individual in infected],
                  #          'y': [individual.y for individual in infected],
                  #          'type': 'scatter',
                  #          'mode': 'markers',
                  #          'name': 'Infected',
                  #          'marker': {'color': 'red',
                  #                     'size': 10}
                  #          },
                  #         {'x': [individual.x for individual in healthy],
                  #          'y': [individual.y for individual in healthy],
                  #          'type': 'scatter',
                  #          'mode': 'markers',
                  #          'name': u'Healthy',
                  #          'marker': {'color': 'green',
                  #                     'size': 5}
                  #          },
                  #     ],
                  #     'layout': {
                  #         'plot_bgcolor': 'rgba(0,0,0,0)',
                  #         'paper_bgcolor': 'rgba(0,0,0,0)',
                  #         'font': {
                  #             'color': colors['text']
                  #         },
                  #         'autosize': True,
                  #         'height': 900,
                  #         'width': 1850,
                  #         'xaxis': dict(range=[0, 1000], showgrid=False, zeroline=False, tickmode="array",
                  #                       tickvals=[]),
                  #         'yaxis': dict(range=[0, 1000], showgrid=False, zeroline=False, tickmode="array",
                  #                       tickvals=[])
                  #     }
                  # }
                  )
        , dcc.Graph(id='live-graph_2',
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
                             'marker': {'color': 'green'}
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

    ], className='row', style={"columnCount": 1})
)


@app.callback(Output('live-graph', 'figure'), inputs=[Input('graph-update', 'n_intervals')])
def update_graph_scatter(interval):
    for individual in individuals:
        individual.move()
        if not individual.infected:
            individual.check_infection(individuals=individuals)

            if individual.infected:
                infected.append(individual)

    return {
        'data': [{
            'lat': [individual.lat for individual in healthy],
            'lon': [individual.lon for individual in healthy],
            'mode': 'markers',
            'marker': gos.scattermapbox.Marker(
                size=5,
                color='blue',
                symbol='circle'
            ),
            'type': 'scattermapbox'
        },
            {
                'lat': [individual.lat for individual in infected],
                'lon': [individual.lon for individual in infected],
                'mode': 'markers',
                'marker': gos.scattermapbox.Marker(
                    size=5,
                    color='red',
                    symbol='circle'
                ),
                'type': 'scattermapbox'
            }
        ],
        'layout': dict(autosize=True,
                       hovermode='closest',
                       paper_bgcolor='rgba(0,0,0,0)',
                       margin=dict(l=0, r=0, t=0, b=0),
                       width=1850,
                       height=900,
                       mapbox=dict(
                           accesstoken=mapbox_access_token,
                           style='dark',
                           center=dict(
                               lat=50.05,
                               lon=19.895
                           ),
                           bearing=0,
                           pitch=0,
                           zoom=12
                       ))
    }


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
