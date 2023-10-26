import json
import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Input, Output





app = Dash(__name__)
app.layout = html.Div([
    dcc.Dropdown(
        id="DROPDOWN ID", #id de la dropdown si y'a
        options=["LISTE DES OPTIONS POSSIBLES AFFICHER DANS LA DROPDOWN"],
        value= ["VALEUR DE CES OPTIONS POSSIBLES"]
    ),
    dcc.Graph(id='NOM DU GRAPHE')
])


@app.callback(
    Output("Ensemble des données outputs","ihhhhh"),
    [Input('ID_DRODOWN (par exemple)','value du dropdown')]
)

def update_any_graph(value):
    #voir tuto 
    return True

app.run_server(debug=True)
