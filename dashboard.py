import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import json

# DATA








app = dash.Dash(__name__)


app.layout = html.Div([
    html.H1("Dashboard"),

    # Choix journal
    html.Div([
        dcc.Dropdown(id='dropdown_1',
                     options=[{'label': "MALI_ER","value":"MALI_ER"},
                              {'label': "MALI_FP","value":"MALI_FP"},
                              {'label': "MALI_SN","value":"MALI_SN"},
                              {'label': "FRANCE_FdS","value":"FRANCE_FdS"},
                              {'label': "FRANCE_SN","value":"FRANCE_SN"},
                              {'label': "FRANCE_ER","value":"FRANCE_ER"},
                              {'label': "FRANCE_FP","value":"FRANCE_FP"}
                              ],
                     value='MALI_ER')  
    ]),

    # Choix personne
    html.Div([
        dcc.Dropdown(id='dropdown_2',
                     options=[], 
                     value='')      
    ]),
    # Histogramme 2D
    dcc.Graph(id='bar'),

    # Line chart
    dcc.Graph(id='line-chart'),

    # Carte
    dcc.Graph(id='map', config={'scrollZoom': False}),
    
    ])


#callback menu deroulant
@app.callback(
    dash.dependencies.Output('dropdown_2', 'options'),
    [dash.dependencies.Input('dropdown_1', 'value')]
)
def update_2_dropdown(selected_journal):
    # Votre logique pour mettre à jour le dropdown 2 en fonction de dropdown 1
    dfDictPers = pd.read_csv(f"PeopleSaves/{selected_journal}_Top10_People.csv")
    names = list(dfDictPers["Names"])
    options = [{'label': name, 'value': name} for name in names]
    return options

@app.callback(
    dash.dependencies.Output('bar', 'figure'),
    dash.dependencies.Output('line-chart', 'figure'),
    [dash.dependencies.Input('dropdown_1', 'value')]
)
def update_bar_line(selected_dropdown_value):
    
    bar_df = pd.read_csv(f"PeopleSaves/{selected_dropdown_value}_Top10_People.csv")
    bar_df_sorted = bar_df.sort_values(by='Values', ascending=False)
    bar_fig = px.bar(bar_df_sorted, x='Names', y='Values', labels={'Names': 'Nom', 'Values': 'Valeur'}, title='Histogramme des 10 personnes les plus fréquentes')

    with open(f"PeopleSaves/{selected_dropdown_value}_Top10_People_Evolution.json",'r') as f:
        line_dict = json.load(f)
        
    
    
    
    line_chart_fig = None
    for key, values in line_dict.items():
        dates = []
        values_list = []
        for entry in values:
            for date, value in entry.items():
                dates.append(date)
                values_list.append(value)
        if line_chart_fig is None:
            line_chart_fig = px.line(labels={'x': 'Date', 'y': 'Valeur'}, title='Evolution de la présence')
            line_chart_fig.add_scatter(x=dates, y=values_list, mode='lines', name=key)
        else:
            line_chart_fig.add_scatter(x=dates, y=values_list, mode='lines', name=key)
    return bar_fig, line_chart_fig

@app.callback(
    dash.dependencies.Output('map', 'figure'),
    [dash.dependencies.Input('dropdown_1', 'value'),
     dash.dependencies.Input('dropdown_2', 'value')]
)
def update_map(selected_dropdown_value_1, selected_dropdown_value_2):
    #use both parameter in order to create the mapping value_1 = journal value_2 = personne
    with open(f"CountriesSaves/{selected_dropdown_value_1}_top10_contries.json",'r')as f:
        contries_data = json.load(f)
    data_pers = contries_data[selected_dropdown_value_2]
    df_pers = pd.DataFrame(data_pers)
    min_value = df_pers['Value'].min()
    max_value = df_pers['Value'].min()
    map_fig = px.choropleth(df_pers,
                            locations="ISO-3", 
                            locationmode="ISO-3",
                            color="Value",  
                            color_continuous_scale="YlOrRd",  
                            range_color=(min_value, max_value),  
                            hover_name="Loc",  
                            projection="natural earth"  
                        )


    map_fig.update_geos(showcoastlines=True, coastlinecolor="Black", coastlinewidth=2)

    map_fig.update_layout(title_text=f'Heatmap of countries in {selected_dropdown_value_1} for {selected_dropdown_value_2}')  # Set the title
    return map_fig



if __name__ == '__main__':
        
    app.run_server(debug=True)
