import json

DICT = {"MALI_ER": "topaz-data732--mali--www.egaliteetreconciliation.fr--20190101--20211231.json",
        "MALI_FP":"topaz-data732--mali--french.presstv.ir--20190101--20211231.json",
        "MALI_SN":"topaz-data732--mali--fr.sputniknews.africa--20190101--20211231.json",
        "FRANCE_FdS":"topaz-data732--france--www.fdesouche.com--20190101--20211231.json",
        "FRANCE_ER":"topaz-data732--france--www.egaliteetreconciliation.fr--20190101--20211231.json",
        "FRANCE_FP":"topaz-data732--france--french.presstv.ir--20190101--20211231.json",
        "FRANCE_SN":"topaz-data732--france--fr.sputniknews.africa--20190101--20211231.json"}


def get_data(dataName):
    for c,v in DICT.items():
        if(dataName==c):
            return v
    print("This data doesn't exist")
    
    
def open_file(fileName):
    with open("../sources/" + fileName,'r') as f:
        data = json.loads(f.read())
        
    return data    