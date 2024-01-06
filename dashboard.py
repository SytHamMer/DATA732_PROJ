import pandas as pd
import plotly.express as px
import dash
from dash import html,dcc
from dash.dependencies import Input,Output
import json

app = dash.Dash(__name__, external_stylesheets=['assets/styles.css'])
# app = dash.Dash(__name__, external_stylesheets=['assets/styles.css'], suppress_callback_exceptions=True)

#IMPORT DATA

first_df = pd.read_csv("PeopleSaves/MALI_ER_Top10_People.csv")
names = list(first_df["Names"])
options = [{'label': name, 'value': name} for name in names]
COLORS = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'white', 'cyan']




#APP LAYOUT

app.layout = html.Div(id="main_div",
                      children=[
    html.Div(id="title_div",children=[
            html.H1("DASHBOARD", id="title"),    
    ]),
    html.Div(id="dropdown_div",children=[
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
                 ),
        dcc.Dropdown(id="select_person",
                 options=options,
                 value = options[0]["value"],

                 ),
        
        
    ]),
    
    html.Div(id="all_graphs",children=[
        html.Div(id="left_graphs",children=[
                dcc.Graph(id='map',figure={}),
                # dcc.Graph(id="barchart_top10",figure={}),
                dcc.Graph(id='linechart_top10',figure={}),
                ]),
        html.Div(id="right_graphs",children=[
        # dcc.Graph(id='linechart_top10',figure={}),
        dcc.Graph(id="barchart_top10",figure={}),
        html.Div(id="svg_div")
        ]),
    ]),

    ]
)



# CALLBACKS
@app.callback(
    [Output(component_id="select_person",component_property='options'),
     Output(component_id="select_person",component_property='value'),
     Output(component_id="barchart_top10",component_property='figure'),
     Output(component_id="linechart_top10",component_property='figure'),
     Output(component_id="svg_div",component_property='children')],
    [Input(component_id="select_journal",component_property="value")]
)

def update_top_10(option_selected):
    options_df = pd.read_csv(f"PeopleSaves/{option_selected}_Top10_People.csv")
    names = list(options_df["Names"])
    pers_options = [{'label': name, 'value': name} for name in names]
    value = pers_options[0]["value"]
    bar_fig_df = pd.read_csv(f"PeopleSaves/{option_selected}_Top10_People.csv")
    bar_fig_df_sorted = bar_fig_df.sort_values(by='Values', ascending=False)
    bar_title = f"Histogramme des 10 personnes les plus citées dans le journal {option_selected}"
    
    
    color_dict = dict(zip(names, COLORS[:len(names)]))
    bar_fig = px.bar(bar_fig_df_sorted,
                     x='Names', 
                     y='Values', 
                     labels={'Names': 'Nom', 'Values': 'Valeur'},
                     title=bar_title,
                     template='plotly_dark',
                     color = 'Names',
                     color_discrete_map=color_dict)
    
    with open(f"PeopleSaves/{option_selected}_Top10_People_Evolution.json",'r') as f:
        line_dict = json.load(f)
    line_fig= None
    # print(line_dict)
    for index, key in enumerate(line_dict.keys()):
        values = line_dict[key]
        dates = []
        values_list = []
        for entry in values:
            for date, value in entry.items():
                dates.append(date)
                values_list.append(value)
        if line_fig is None:
            line_fig = px.line(labels={'x': 'Date', 'y': 'Valeur'}, 
                               title="Evolution de l'apparition des 10 personnes au fil du temps",
                               template="plotly_dark",
                               )
            line_fig.add_scatter(x=dates, y=values_list, mode='lines', name=key,line_color = COLORS[index])
        else:
            line_fig.add_scatter(x=dates, y=values_list, mode='lines', name=key,line_color = COLORS[index])
    
    svg_file = f"gephi/{option_selected}.svg"
    graph_title = f"Graphe relationelle des personnes se trouvant dans les articles de {option_selected}"
    child = [html.H3(graph_title, id="graph_title"),
            html.Div(id="svg_child_div",children=[
            html.Img(id="svg_image", src=dash.get_asset_url(svg_file)),
        ])]
         
    #return Output1 and Output2
    return pers_options,value, bar_fig,line_fig,child






@app.callback(
    Output(component_id="map",component_property='figure'),
    [Input(component_id="select_person",component_property="value"),
     Input(component_id="select_journal",component_property="value")]
)
def update_map(person_selected,journal_selected):
    with open(f"CountriesSaves/{journal_selected}_top10_contries.json",'r')as f:
        contries_data = json.load(f)
    # print(person_selected)
    #Cas ou y'a rien de séléctionner
    if type(person_selected) == int:
        #cas chargement de la page
        data_pers= contries_data["macron"]
        title = f"Carte des pays en lien avec macron dans les articles du journal  {journal_selected}."
    else:
        title = f"Carte des pays en lien avec {person_selected} dans les articles du journal  {journal_selected}."
        data_pers = contries_data[person_selected]
    df_map = pd.DataFrame(data_pers)    
    min_value  = df_map["Value"].min()
    max_value = df_map["Value"].max()
    fig = px.choropleth(
        data_frame=df_map,
        locationmode="ISO-3",
        locations="ISO-3",
        color="Value",
        hover_data=["Loc","Value"],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        range_color=(min_value,max_value),
        template="plotly_dark"
    )
    fig.update_layout(
        title_text=title,
        title_x=0.5,  

    )
    return fig






    
if __name__ == '__main__':
        
    app.run_server(debug=True)