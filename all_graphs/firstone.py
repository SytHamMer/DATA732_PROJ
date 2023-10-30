import json
import plotly.express as px
import pandas as pd
import data
import numpy as np


COUNTRIES = {
    'afghanistan': 'AFG',
    'albanie': 'ALB',
    'algérie': 'DZA',
    'andorre': 'AND',
    'angola': 'AGO',
    'antigua-et-barbuda': 'ATG',
    'argentine': 'ARG',
    'arménie': 'ARM',
    'australie': 'AUS',
    'autriche': 'AUT',
    'azerbaïdjan': 'AZE',
    'bahamas': 'BHS',
    'bahreïn': 'BHR',
    'bangladesh': 'BGD',
    'barbade': 'BRB',
    'bélarus': 'BLR',
    'belgique': 'BEL',
    'belize': 'BLZ',
    'bénin': 'BEN',
    'bhoutan': 'BTN',
    'bolivie': 'BOL',
    'bosnie-herzégovine': 'BIH',
    'botswana': 'BWA',
    'brésil': 'BRA',
    'brunei': 'BRN',
    'bulgarie': 'BGR',
    'burkina faso': 'BFA',
    'burundi': 'BDI',
    'cambodge': 'KHM',
    'cameroun': 'CMR',
    'canada': 'CAN',
    'cap-vert': 'CPV',
    'centrafrique': 'CAF',
    'chili': 'CHL',
    'chine': 'CHN',
    'chypre': 'CYP',
    'colombie': 'COL',
    'comores': 'COM',
    'congo': 'COG',
    'corée du nord': 'PRK',
    'corée du sud': 'KOR',
    'costa rica': 'CRI',
    "côte d'ivoire": 'CIV',
    'croatie': 'HRV',
    'cuba': 'CUB',
    'danemark': 'DNK',
    'djibouti': 'DJI',
    'dominique': 'DMA',
    'égypte': 'EGY',
    'émirats arabes unis': 'ARE',
    'équateur': 'ECU',
    'érythrée': 'ERI',
    'espagne': 'ESP',
    'estonie': 'EST',
    'eswatini': 'SWZ',
    'états-unis': 'USA',
    'éthiopie': 'ETH',
    'fidji': 'FJI',
    'finlande': 'FIN',
    'france': 'FRA',
    'gabon': 'GAB',
    'gambie': 'GMB',
    'géorgie': 'GEO',
    'ghana': 'GHA',
    'grèce': 'GRC',
    'grenade': 'GRD',
    'guatemala': 'GTM',
    'guinée': 'GIN',
    'guinée équatoriale': 'GNQ',
    'guinée-bissau': 'GNB',
    'guyana': 'GUY',
    'haïti': 'HTI',
    'honduras': 'HND',
    'hongrie': 'HUN',
    'inde': 'IND',
    'indonésie': 'IDN',
    'irak': 'IRQ',
    'iran': 'IRN',
    'irlande': 'IRL',
    'islande': 'ISL',
    'israël': 'ISR',
    'italie': 'ITA',
    'jamaïque': 'JAM',
    'japon': 'JPN',
    'jordanie': 'JOR',
    'kazakhstan': 'KAZ',
    'kenya': 'KEN',
    'kirghizistan': 'KGZ',
    'kiribati': 'KIR',
    'kosovo': 'XKX',
    'koweït': 'KWT',
    'laos': 'LAO',
    'lesotho': 'LSO',
    'lettonie': 'LVA',
    'liban': 'LBN',
    'libéria': 'LBR',
    'libye': 'LBY',
    'liechtenstein': 'LIE',
    'lituanie': 'LTU',
    'luxembourg': 'LUX',
    'macédoine': 'MKD',
    'madagascar': 'MDG',
    'malaisie': 'MYS',
    'malawi': 'MWI',
    'maldives': 'MDV',
    'mali': 'MLI',
    'malte': 'MLT',
    'maroc': 'MAR',
    'marshall': 'MHL',
    'maurice': 'MUS',
    'mauritanie': 'MRT',
    'mexique': 'MEX',
    'micronésie': 'FSM',
    'moldavie': 'MDA',
    'monaco': 'MCO',
    'mongolie': 'MNG',
    'monténégro': 'MNE',
    'mozambique': 'MOZ',
    'namibie': 'NAM',
    'nauru': 'NRU',
    'népal': 'NPL',
    'nicaragua': 'NIC',
    'niger': 'NER',
    'nigeria': 'NGA',
    'niue': 'NIU',
    'norvège': 'NOR',
    'nouvelle-zélande': 'NZL',
    'oman': 'OMN',
    'ouganda': 'UGA',
    'ouzbékistan': 'UZB',
    'pakistan': 'PAK',
    'palaos': 'PLW',
    'palestine': 'PSE',
    'panama': 'PAN',
    'papouasie-nouvelle-guinée': 'PNG',
    'paraguay': 'PRY',
    'pays-bas': 'NLD',
    'pérou': 'PER',
    'philippines': 'PHL',
    'pologne': 'POL',
    'portugal': 'PRT',
    'qatar': 'QAT',
    'république centrafricaine': 'CAF',
    'république du congo': 'COG',
    'république dominicaine': 'DOM',
    'république tchèque': 'CZE',
    'roumanie': 'ROU',
    'royaume-uni': 'GBR',
    'russie': 'RUS',
    'rwanda': 'RWA',
    'saint-christophe-et-niévès': 'KNA',
    'saint-marin': 'SMR',
    'saint-vincent-et-les-grenadines': 'VCT',
    'sainte-lucie': 'LCA',
    'salomon': 'SLB',
    'salvador': 'SLV',
    'samoa': 'WSM',
    'sao tomé-et-principe': 'STP',
    'sénégal': 'SEN',
    'serbie': 'SRB',
    'seychelles': 'SYC',
    'sierra leone': 'SLE',
    'singapour': 'SGP',
    'slovaquie': 'SVK',
    'slovénie': 'SVN',
    'somalie': 'SOM',
    'soudan': 'SDN',
    'soudan du sud': 'SSD',
    'sri lanka': 'LKA',
    'suède': 'SWE',
    'suisse': 'CHE',
    'suriname': 'SUR',
    'syrie': 'SYR',
    'tadjikistan': 'TJK',
    'taïwan': 'TWN',
    'tanzanie': 'TZA',
    'tchad': 'TCD',
    'thaïlande': 'THA',
    'timor oriental': 'TLS',
    'togo': 'TGO',
    'tonga': 'TON',
    'trinité-et-tobago': 'TTO',
    'tunisie': 'TUN',
    'turkménistan': 'TKM',
    'turquie': 'TUR',
    'tuvalu': 'TUV',
    'ukraine': 'UKR',
    'uruguay': 'URY',
    'vanuatu': 'VUT',
    'vatican': 'VAT',
    'vénézuéla': 'VEN',
    'vietnam': 'VNM',
    'yémen': 'YEM',
    'zambie': 'ZMB',
    'zimbabwe': 'ZWE',
}

#Test, map with all country in all article of a certain date
#differents precision all,year,month,day

#for now only year precision
#Removing the country of the article (MALI OR FRANCE)
def all_countries_by_articles(article,y):
    d = data.open_file(data.get_data(article))["metadata-all"]["fr"]
    if y == 0:
        infos = d["all"]
    else:
        infos= d["year"][str(y)]
    locList=[]
    for loc in infos["loc"]:
        if (loc.lower() in COUNTRIES.keys()) and not(loc.lower() in article.lower()):
            dataLoc = {"Loc": loc,
                    "Value": infos["loc"][loc],
                    "ISO-3": COUNTRIES[loc.lower()]
                    }
            locList.append(dataLoc)
    df = pd.DataFrame(locList)
    print(df)
    min_value = df['Value'].min()
    max_value = df['Value'].max()
    print(min_value)
    print(max_value)
    fig = px.choropleth(df,
                        locations="ISO-3", 
                        locationmode="ISO-3",
                        color="Value",  
                        color_continuous_scale="YlOrRd",  
                        range_color=(min_value, max_value),  
                        hover_name="Loc",  
                        projection="natural earth"  
                    )

    fig.update_geos(showcoastlines=True, coastlinecolor="Black", coastlinewidth=2)

    fig.update_layout(title_text='Heatmap of Values by Country')  # Set the title

    fig.show()    
        




def firstclustering(article):
    d = data.open_file(data.get_data(article))
    
    
    #create the matrice
    




if __name__ == "__main__":
    
    all_countries_by_articles("MALI_ER",0)