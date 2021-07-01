"""
Att göra lista:
    1. Fixa skapa_program(beskrivning)  Klar!
    2. svenska_bokstäver()
    3. Någon form av export
"""


import gzip
import urllib.request
import os
import datetime
import time
from bs4 import BeautifulSoup

class program:
    def __init__(self, startdatum, starttid, slutdatum, sluttid, namn, beskrivning, kategorier,kanal='',skådespelare=None,kategori='Okänd'):
        self.datum = startdatum
        self.start = starttid
        self.slut = sluttid
        self.startdatum = startdatum
        #self.starttid = starttid
        self.slutdatum = slutdatum
        #self.sluttid = sluttid
        self.namn = svenska_bokstäver(namn)
        self.beskrivning = svenska_bokstäver(beskrivning)
        self.kategorier = [svenska_bokstäver(k).capitalize() for k in kategorier]
        self.kategori = kategori
        self.kanal = kanal
        self.skådespelare = skådespelare

        if self.skådespelare == None:
            self.skådespelare = []

    def __str__(self):
        r = self.datum + '\t' + self.start + ' - ' + self.slut + '\t'
        r += self.namn + '\n' + self.beskrivning + '\n\n\n'
        return r

    def __hash__(self):
        r = hash(repr(self.__dict__))
        return r

    def __eq__(self,other):
        if hash(self) == hash(other):
            return True
        else:
            return False

    def __lt__(self,other):
        if self.starttid() < other.starttid():
            return True
        else:
            return False
    def __le__(self,other):
        if self.starttid() == other.starttid() or self.starttid() < other.starttid():
            return True
        else:
            return False

    def mejl_str(self):
        r = self.datum[:4] + '-' + self.datum[4:6] + '-' + self.datum[6:] + '   ' + self.start + ' - ' + self.slut + '    ' + self.namn  + '   ' + self.kanal + '\n' + self.anpassad_langd(self.beskrivning,60) + '\n\n\n'
        return r

    def mejl_html(self):
        div = '<div style="width:600px;font-family:Courier new;text-align:justify">'
        r = '<p><pre>' + self.datum[:4] + '-' + self.datum[4:6] + '-' + self.datum[6:] + '   ' + self.start + ' - ' + self.slut + '    ' + self.namn.ljust(24,' ')  + '   ' + self.kanal + '</pre>\n' + div + self.anpassad_langd(self.beskrivning,60) + '</p><br></div>' + '\n\n\n'
        return r

    def export_str(self):
        r = self.datum + '\t' + self.start + ' - ' + self.slut + '\t' + self.namn
        r += '\t' + self.kategori + '\t' + self.kanal  + '\t' + self.slutdatum
        r += '\t' + str(self.skådespelare) + '\t' + str(self.kategorier)
        r += '\n' + self.beskrivning + '\n\n\n'
        return r
    
    def anpassad_langd(self,text,langd=78):
        lista = text.split(' ')
        r = str()
        radlangd = 0

        for orden in lista:
            if radlangd + len(orden) < langd:
                r = r + orden + ' '
                radlangd += len(orden) + 1
            else:
                r = r + '\n' + orden + ' '
                radlangd = len(orden)

        return r

    def avslutad(self):

        if self.kanal == 'film.tv4.se':
            tid = time.localtime(self.starttid())
            veckodag = tid.tm_wday
            if veckodag not in [0,4,5,6]:
                return True
            elif veckodag in [0,4]:
                if veckodag == 0 and tid.tm_hour >= 8:
                    return True
                elif veckodag == 4 and tid.tm_hour < 21:
                    return True
        if self.kanal == 'tcmeurope.com':
            if int(self.start[:2])<21 and int(self.slut[:2])>6:
                return True

        if (self.sluttid() - time.time()) < 0:
            return True
        else:
            return False

    def starttid(self):
        år = int(self.startdatum[:4])
        mån = int(self.startdatum[4:6])
        dag = int(self.startdatum[6:])

        tim = int(self.start[:2])
        minut = int(self.start[2:])
        sek = int('00')

        dst = time.localtime().tm_isdst

        tup = '({},{},{},{},{},{},1,1,{})'.format(år,mån,dag,tim,minut,sek,dst)
        a = eval(tup)
        b = time.struct_time(a)
        c = time.mktime(b)

        return c

    def sluttid(self):
        år = int(self.slutdatum[:4])
        mån = int(self.slutdatum[4:6])
        dag = int(self.slutdatum[6:])

        tim = int(self.slut[:2])
        minut = int(self.slut[2:])
        sek = int('00')

        dst = time.localtime().tm_isdst

        tup = '({},{},{},{},{},{},1,1,{})'.format(år,mån,dag,tim,minut,sek,dst)
        a = eval(tup)
        b = time.struct_time(a)
        c = time.mktime(b)

        return c

    def andel(self):
        a = time.time()
        b = self.starttid()
        c = self.sluttid()
        if b - a > 0:
            return 0
        elif c - a < 0:
            return 1
        else:
            d = abs((b - a)/(b - c))
            return d
            
    

def ladda(kanal,datum):
    url = 'http://xmltv.xmltv.se/' + kanal + '_' + datum + '.xml.gz'
    #url = 'http://xmltv.tvsajten.com/xmltv/'+ kanal + '_' + datum + '.xml.gz'
    #print(url)
    
    response = urllib.request.urlopen(url)
    gzip_file = response.read()
    
    try:r = gzip.decompress(gzip_file)
    except OSError as e: r = gzip_file;print('xml')
    return r

def importera(kanal,content):

    soup = BeautifulSoup(content)
    programlista = soup.find_all('programme')
    returlista = list()

    for p in programlista:
        kanal = p.get('channel')
        startdatum = p.get('start')[:8]
        starttid = p.get('start')[8:12]
        slutdatum = p.get('stop')[:8]
        sluttid = p.get('stop')[8:12]
        namn = p.title.string
        kategorier = [i.string for i in p.find_all('category')]
        skådespelare = [i.string.strip().title() for i in p.find_all('actor')]
        try:
            beskrivning = p.desc.string
        except AttributeError:
            beskrivning = 'Beskrivning saknas'
        try:
            kategori = p.category.string.capitalize()
        except AttributeError:
            kategori = 'Okänd'
        returlista.append(program(startdatum,starttid,slutdatum,sluttid,namn,beskrivning,kategorier,kanal,skådespelare,kategori))

    return returlista


def svenska_bokstäver(text):
    r = text.replace('&quot;','"').replace('&amp;','&')
    r = r.replace('"sv">','').replace('"en">','').replace('"se">','')
    r = r.replace('\u200b','')  #Zero-width space
    return r

def export(lista,kanal,datum):
    filnamn = 'tvguide_' + kanal + '.txt'
    mapp = 'tvmapp'
    with open(os.path.join(mapp, filnamn),'w',encoding='utf8')as fil:
        for i in range(len(lista)):
            fil.write(lista[i].export_str())
    

#-------------------------------Huvudprogrammet--------------------------------#

def master_ny(kanal,dat):
    datumlista = [akt(i) for i in range(-1,2)]
    returlista = list()
    for datum in datumlista:
        gzip_file = ladda(kanal,datum)
        returlista.extend(importera(kanal,gzip_file))

    export(returlista,kanal,dat)

    return returlista

def master_gammal(kanal,datum):

    filnamn = 'tvmapp/tvguide_' + kanal + '.txt'
    
    with open(filnamn,'r',encoding='utf8') as fil:
        text = fil.read()

    filer = text.rstrip('\n').split('\n\n\n')
    li = list()
    
    for fil in filer:
        a = fil.split('\n')
        beskrivning = a[1]
        b = a[0].split('\t')
        if len(b) == 5:
            b.extend([b[0],str([]),str([b[3]])])
        startdatum = b[0]
        slutdatum = b[5]
        titel = b[2]
        kategori = b[3]
        kategorier = eval(b[7])
        skådespelare = eval(b[6])
        c = b[1].split(' - ')
        starttid = c[0]
        sluttid = c[1]
        tv = program(startdatum, starttid, slutdatum, sluttid, titel, beskrivning,kategorier,kanal,skådespelare,kategori)
        li.append(tv)

    return li
    

def master(kanal,datum):
    try:
        s = gammal_tid(kanal)
    except:
        s = False
    a = akt()
    if a == s:
        tablå = master_gammal(kanal,datum)
    else:
        tablå = master_ny(kanal,datum)
    return tablå

def akt(dag = 0):
    tid = time.localtime(time.time() + dag*3600*24)
    år = str(tid.tm_year).zfill(2)
    månad = str(tid.tm_mon).zfill(2)
    dag = str(tid.tm_mday).zfill(2)

    r = år + '-' + månad + '-' + dag
    return r

def gammal_tid(kanal):
    fil = 'tvmapp/tvguide_' + kanal + '.txt'
    t = os.path.getmtime(fil)
    with open(fil,errors='replace') as f:
        text = f.readline()
    if text == '':
        return False
    s = datetime.datetime.fromtimestamp(t)
    r = str(s)[:10]
    return r


if __name__ == '__main__':
    kanal = 'svt2.svt.se'
    datum = akt()
    programlista = master(kanal,datum)

    for prog in programlista:
        if not prog.avslutad():
            print(str(round(prog.andel(),4)*100)[:5] + ' %')
            print(prog.avslutad())
            print(str(prog).strip())
            break

    #p = programlista[0]

##    with gzip.open('output.gz')as fil:
##        f = fil.read().decode('utf8')
##    soup = BeautifulSoup(f)
##    programlista2 = soup.find_all('programme')
##    p = programlista2[0]
##    
