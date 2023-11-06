import json
import re
import unicodedata
import Levenshtein  as lvs

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


def normalize_name(name):
    #remove accents
    step1 = unicodedata.normalize("NFD",name)
    
    #remove special character and non alphabetical ones
    step2 = re.sub(r'[^a-zA-Z\s]','',step1)
    
    finalStep = step2.lower()
    return finalStep


def same_name(name1,name2,limite):
    #the idea is to join similar name together in order to normalize data and clear it
    

    if lvs.distance(name1,name2) < limite:
        # print(f"{name1} and {name2} are close enougth")
        return True
    else:
        # print(f"{name1} and {name2} are NOT close enougth")
        # print(lvs.distance(name1,name2))
        return False
    
    
def merge_same_name(mergeList,newName,limite):
    i = 0
    if len(mergeList) == 0:
        mergeList.append(newName)
    else:
        while not(same_name(mergeList[i],newName,limite)) and i<(len(mergeList)-1):
            i+=1
        if i>=(len(mergeList)-1):
            mergeList.append(newName)
            
    # print(mergeList)
            
def get_merge_name(mergeList,newName,limite):
    i=0
    while lvs.distance(mergeList[i],newName)>limite and i<(len(mergeList)):
        i+=1
    if i>=(len(mergeList)):
        print("====================================")
        print("ERROR")
        min=999
        minName=""
        for y in range(0,len(mergeList)):

            if lvs.distance(mergeList[y],newName)<min:
                min = lvs.distance(mergeList[y],newName)
                minName = mergeList[y]
            print(f"la distance est de {lvs.distance(mergeList[y],newName)} avec {mergeList[y]}")
            print(f"La plus petite valeur est {min} pour le mot :{minName}")
        print(newName)
        print("====================================")
    else:
        return mergeList[i]

    
if __name__ == '__main__':
    print(same_name("eric zemmour","zemmour",6))
    print(merge_same_name(["zemmour","camion","brouette","eric"],"eric zemmofsqdfr",6))
    print(merge_same_name([],"zemmour",6))
    print(get_merge_name(["camion","banane","zemmour","papeterie"],"eric zemmour",6))