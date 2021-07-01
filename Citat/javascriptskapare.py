import json

class Citat:

    def __init__(self,citat,citerad):
        self.citat = citat.rstrip(' -').replace("'",'&apos;').replace('"','&quot;')
        self.citerad = citerad.strip(' -').replace("'",'&apos;').replace('"','&quot;')

    def __hash__(self):
        return hash(self.citat+self.citerad)

    def __eq__(self,other):
        return hash(self)==hash(other) and type(self)==type(other)

    def __str__(self):
        return self.citat + ' - '+ self.citerad

def importera():
    filnamn = 'Total.txt'
    with open(filnamn,encoding='utf8') as fil:
        f = fil.read().strip().split('\n')
    l = list()
    for rad in f:
        l.append(Citat(**eval(rad)))
        #print(rad)
    return l

def exportera(lista1,lista2):
    text = std.format(lista1=lista1,lista2=lista2).replace('#','{').replace('!!','}')
    filnamn = 'citatscript.js'
    with open(filnamn,'w',encoding='utf8') as fil:
        fil.write(text)

def bearbeta(l):
    lista1 = ("'" + "','".join(map(lambda i: i.citat,l)) + "'").replace('"','&quot;')
    lista2 = ("'" + "','".join(map(lambda i: i.citerad,l)) + "'").replace('"','&quot;')
    return lista1,lista2
        

std = """function slumpacitat() #
    var arr = [{lista1}];
    var arr2 = [{lista2}]
    var rand = Math.floor(Math.random() * arr.length);
    document.getElementById('slumpcitat').innerHTML=arr[rand];
    document.getElementById('slumpciterad').innerHTML=arr2[rand];
    startTime()
    !!"""

if __name__ == '__main__':
    l = importera()
    exportera(*bearbeta(l))
    
