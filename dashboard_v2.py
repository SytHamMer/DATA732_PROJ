import pandas as pd
import plotly.express as px
import dash
from dash import html,dcc
from dash.dependencies import Input,Output
import json

app = dash.Dash(__name__)

#IMPORT DATA

first_df = pd.read_csv("PeopleSaves/MALI_ER_Top10_People.csv")
names = list(first_df["Names"])
options = [{'label': name, 'value': name} for name in names]


#APP LAYOUT

app.layout = html.Div([
    html.H1("DASHBOARD",style={'text-align': 'center'}),
    
    dcc.Dropdown(id="select_journal",
                 options=[
                     {'label': "MALI_ER","value":"MALI_ER"},
                     {'label': "MALI_FP","value":"MALI_FP"},
                     {'label': "MALI_SN","value":"MALI_SN"},
                     {'label': "FRANCE_FdS","value":"FRANCE_FdS"},
                     {'label': "FRANCE_SN","value":"FRANCE_SN"},
                     {'label': "FRANCE_ER","value":"FRANCE_ER"},
                     {'label': "FRANCE_FP","value":"FRANCE_FP"}
                     ],
                 value='MALI_ER',
                 multi=False,
                 style={'background-color':'#111111',
                        'width':'300px'},
                 ),
    
    dcc.Graph(id="barchart_top10",figure={}),
    dcc.Graph(id='linechart_top10',figure={}),
    
    dcc.Dropdown(id="select_person",
                 options=options,
                 value = options[0]["value"],
                 style={'background-color':'#111111',
                        'backgroundColor' :'#111111',
                        'color':'white',
                        'width':'300px'
                        },
                 ),
    
    dcc.Graph(id='map',figure={}),
    
    html.Div(id="svg_image")
])



# CALLBACKS
@app.callback(
    [Output(component_id="select_person",component_property='options'),
     Output(component_id="select_person",component_property='value'),
     Output(component_id="barchart_top10",component_property='figure'),
     Output(component_id="linechart_top10",component_property='figure'),
     Output(component_id="svg_image",component_property='children')],
    [Input(component_id="select_journal",component_property="value")]
)

def update_top_10(option_selected):
    options_df = pd.read_csv(f"PeopleSaves/{option_selected}_Top10_People.csv")
    names = list(options_df["Names"])
    options = [{'label': name, 'value': name} for name in names]
    value = options[0]["value"]
    bar_fig_df = pd.read_csv(f"PeopleSaves/{option_selected}_Top10_People.csv")
    bar_fig_df_sorted = bar_fig_df.sort_values(by='Values', ascending=False)
    bar_title = f"Histogramme des 10 personnes les plus cités dans le journal {option_selected}"
    print(bar_title)
    bar_fig = px.bar(bar_fig_df_sorted,
                     x='Names', 
                     y='Values', 
                     labels={'Names': 'Nom', 'Values': 'Valeur'},
                     title=bar_title,
                     template='plotly_dark')
    
    with open(f"PeopleSaves/{option_selected}_Top10_People_Evolution.json",'r') as f:
        line_dict = json.load(f)
    line_fig= None
    for key, values in line_dict.items():
        dates = []
        values_list = []
        for entry in values:
            for date, value in entry.items():
                dates.append(date)
                values_list.append(value)
        if line_fig is None:
            line_fig = px.line(labels={'x': 'Date', 'y': 'Valeur'}, 
                               title="Evolution de l'apparition des 10 personnes au fil du temps",
                               template="plotly_dark")
            line_fig.add_scatter(x=dates, y=values_list, mode='lines', name=key)
        else:
            line_fig.add_scatter(x=dates, y=values_list, mode='lines', name=key)
    
    svg_file = f"{option_selected}.svg"
    child = html.Div([html.H3(f"Graphe relationelle des personnes se trouvant dans les articles de {option_selected}",
                              style = {'text-align': 'center'}),
                      html.Img(src=dash.get_asset_url(svg_file))],
                     style={'display':'flex',
                            'justify-content':'center'})
    
          
    #return Output1 and Output2
    return options,value, bar_fig,line_fig,child


@app.callback(
    Output(component_id="map",component_property='figure'),
    [Input(component_id="select_person",component_property="value"),
     Input(component_id="select_journal",component_property="value")]
)
def update_map(person_selected,journal_selected):
    with open(f"CountriesSaves/{journal_selected}_top10_contries.json",'r')as f:
        contries_data = json.load(f)
    data_pers = contries_data[person_selected]
    df_map = pd.DataFrame(data_pers)    
    
    fig = px.choropleth(
        data_frame=df_map,
        locationmode="ISO-3",
        locations="ISO-3",
        color="Value",
        hover_data=["Loc","Value"],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels = {"ICI"},
        template="plotly_dark"
    )
    return fig
    
if __name__ == '__main__':
        
    app.run_server(debug=True)