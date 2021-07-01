class Citat:

    def __init__(self,citat,citerad):
        self.citat = citat.rstrip(' -')
        self.citerad = citerad.strip(' -')

    def __hash__(self):
        return hash(self.citat+self.citerad)

    def __eq__(self,other):
        return hash(self)==hash(other) and type(self)==type(other)

    def __str__(self):
        return self.citat + ' - '+ self.citerad

def importera(filnamn):
    with open(filnamn,'r') as fil:
        read = fil.read()
        read = read.split('\n\n\n')
        li = list()
        for i in range(0,len(read)-1,2):
            li.append(Citat(read[i],read[i+1]))

    return li

def konsolidera(lista):
    if type(lista[0]) != type(list()):
        lista = [lista]
    r = list()
    for i in lista:
        for j in i:
                r.append(j)
    r = list(set(r))

    return r

def exportera(lista):
    with open('Total.txt','w',encoding='utf8') as fil:
        for i in lista:
            fil.write(repr(i.__dict__)+'\n')

def hämta_gammal():
    li = list()
    for i in ['citat3.txt','citat5.txt','citat6.txt']:
        li.append(importera(i))
    r = konsolidera(li)
    print(r[0])
    return r

def importera_total():
    with open('Total.txt','r',encoding='utf8') as fil:
        read = fil.read().strip().split('\n')
        li = list()
        for rad in read:
            rad = eval(rad)
            li.append(Citat(**rad))
        li = konsolidera(li)
        print(li[0])
    return li

def fixa(lista):
    r=lista
    for j in range(len(r)):
        i = r[j]
        if i.citerad.lower()=='tove jansson'.lower():
            i.citat = i.citat.replace('igen','ingen')
            r[j]=i
            print(r[j])

        if i.citerad.lower()=='Ralph Waldo Emerson'.lower() and 'helvetet' in i.citat:
            i.citat = i.citat.replace('helvetet','till helvetet')
            r[j]=i
            print(r[j])
    return r

if __name__ == '__main__':
    r = importera_total()
    
