import json
import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Input, Output


def firstbarchart():
    file_name = 'topaz-data732--mali--french.presstv.ir--20190101--20211231.json'
    with open(file_name,'r') as f:
        data = json.loads(f.read())
        
    articlesByMonth = {}
    for year in data["metadata-all"]["fr"]["month"]:
        # print(f"year : {year}")
        for month in data["metadata-all"]["fr"]["month"][year]:
            # print(f"month : {month}")
            if month not in articlesByMonth.keys():
                print(data["metadata-all"]["fr"]["month"][year][month]["num"])
                articlesByMonth[month] = data["metadata-all"]["fr"]["month"][year][month]["num"]
            else:
                articlesByMonth[month]+= data["metadata-all"]["fr"]["month"][year][month]["num"]
            
    print(articlesByMonth)
    #Trier dans l'ordre pour avoir les mois dans le bon ordre
    sortedArticlesByMonth = {str(k): v for k, v in sorted(articlesByMonth.items(), key=lambda item: int(item[0]))}
    print(sortedArticlesByMonth)
    df = pd.DataFrame(list(sortedArticlesByMonth.items()), columns=['Month', 'Value'])
    sorted
    fig = px.bar(df,x="Month",y="Value")
    fig.write_html("saves.html")
    
def secondbarchart():
    file_name = 'topaz-data732--mali--french.presstv.ir--20190101--20211231.json'
    with open(file_name,'r') as f:
        data = json.loads(f.read())
    
    
    keywords= data["metadata-all"]["fr"]["all"]["kws"]
    top10Keywords = dict(sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:10])
    df = pd.DataFrame(list(top10Keywords.items()), columns=['Keywords', 'Value'])
    fig = px.bar(df,x="Keywords",y="Value")
    fig.write_html("saves2.html")
    
def thirdbarchart():
    file_name = 'topaz-data732--mali--french.presstv.ir--20190101--20211231.json'
    with open(file_name,'r') as f:
        data = json.loads(f.read())
    
    
    year_data_list =[]
    for year in data["metadata-all"]["fr"]["year"]:
        data_years = {"Year" : year,
                      "Keywords"  : data["metadata-all"]["fr"]["year"][year]["kws"]}
        year_data_list.append(data_years)
    df = pd.DataFrame(year_data_list)
    print(df)

    
    app  = Dash(__name__)
    app.layout = html.Div([
        dcc.Dropdown(
            id='year-dropdown', #data qu'on envoie
            options=[{'label': str(year), 'value': year} for year in df['Year']],
            value=df['Year'].iloc[0] #Ce qu'on affiche
        ),
        dcc.Graph(id='bar-chart')
        ])
    
    @app.callback(
        Output('bar-chart', 'figure'),
        [Input('year-dropdown', 'value')] 
    )
    def update_bar_chart(selected_year):
        year_keywords = df[df['Year'] == selected_year]['Keywords'].iloc[0]
        keywords = pd.DataFrame.from_dict(year_keywords, orient='index', columns=['Count'])
        keywords = keywords.sort_values(by='Count', ascending=False).head(10)

        fig = px.bar(keywords, x=keywords.index, y='Count', title=f'Top 10 Keywords for {selected_year}')

        return fig

    app.run_server(debug=True)

    
    

    
if __name__ == "__main__":
    #print(firstbarchart())
    #print(secondbarchart())
    print(thirdbarchart())