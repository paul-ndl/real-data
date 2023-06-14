import numpy as np
import csv
import json
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from ast import literal_eval


# Create the app
app = dash.Dash(__name__)
server = app.server


def generate_fig():
    # Generate data based on the slider values
    with open('./items_map_embeddings.csv', 'r') as f:
        reader = csv.reader(f)
        data = np.array(list(reader))
        description = data[:, 2]
        description = [d.strip('"') for d in description]
        data = data[:, -1]
        data = [literal_eval(d) for d in data]
        data = np.array(data)

    
    fig = go.Figure(data=[go.Scatter3d(
        x=data[:, 0],
        y=data[:, 1],
        z=data[:, 2],
        mode='markers',
        marker=dict(
            size=5,
            opacity=0.8,
            colorscale='Viridis',
            color=data[:, 2],
            colorbar=dict(title='Z')
        ),
        hoverinfo='text',
        text=description,
    )])
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='X', tickmode='linear', dtick=0.5),
            yaxis=dict(title='Y', tickmode='linear', dtick=0.5),
            zaxis=dict(title='Z', tickmode='linear', dtick=0.5)
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    
    return fig

# Set up the layout
app.layout = html.Div([
    dcc.Graph(id='data-plot', style={'height': 'calc(100vh - 50px)'}, figure=generate_fig()),
], style={'padding': '20px'})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)