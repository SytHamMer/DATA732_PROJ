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
    

    if lvs.distance(name1,name2.split(" ")[-1]) < limite:
        return True
    else:
        return False

def merge_same_name(mergeDict,newName,newNameValue,limite):
    i = 0
    split = newName.split(" ")
    if len(mergeDict) == 0:
        
        if(len(split)>1):
            
            mergeDict[split[-1]] = newNameValue
        else:
            mergeDict[newName] = newNameValue
    else:
        
        
        if(len(split)>1):
            while not(same_name(list(mergeDict.keys())[i],split[-1],limite)) and i<(len(mergeDict)-1):
                i+=1

            if i>=(len(mergeDict)-1):
            
                mergeDict[split[-1]] = newNameValue
            else:
                # print(i)
                # print(f"ICi :   {list(mergeDict.keys())[i]}")
                mergeDict[list(mergeDict.keys())[i]] =  mergeDict[list(mergeDict.keys())[i]] + newNameValue          
                
        else:
            
            while not(same_name(list(mergeDict.keys())[i],newName,limite)) and i<(len(mergeDict)-1):
                i+=1

            if i>=(len(mergeDict)-1):
            
                mergeDict[newName] = newNameValue
            else:
                # print(i)
                
                mergeDict[list(mergeDict.keys())[i]] =  mergeDict[list(mergeDict.keys())[i]] + newNameValue          
                         
            
            
def get_merge_name(mergeList,newName):
    split = newName.split(" ")
    if len(split)>0:
        i = 0 
        min =999
        minName = ""
        for name in mergeList:
            if lvs.distance(name,split[-1]) <min:
                min = lvs.distance(name,split[-1])
                minName = name
        
        return minName           
    else:
        
        i = 0 
        min =999
        minName = ""
        for name in mergeList:
            if lvs.distance(name,newName) <min:
                min = lvs.distance(name,newName)
                minName = name
        
        return minName
    
#Version plus opti ?    
# def get_merge_name(mergeList, newName):
#     if " " in newName:
#         last_word = newName.split()[-1]
#         return min(mergeList, key=lambda name: lvs.distance(name, last_word))
#     else:
#         return min(mergeList, key=lambda name: lvs.distance(name, newName))
    
if __name__ == '__main__':
    # print(same_name("zemmour","erkjihuugiic zemmour",3))
    
    liste = ['kabore', 'ouattara', 'macron', 'kebbab', 'shurkin', 'barkhane',
       'lelievre', 'barriere', 'conrad', 'soulages','terrafirma', 'sportolloni', 'richard', 'indoor', 'bardella',
       'bensussan', 'monsieur', 'zagury', 'bermandoa', 'idriss']
    #print(merge_same_name({"zemmour":1,"camion":2,"brouette":3,"eric":4},"zemmour",2,6))
    # print(merge_same_name({},"zemmour",2,6))
    print(get_merge_name(liste,"Soulages"))