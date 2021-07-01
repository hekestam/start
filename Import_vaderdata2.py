import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time

class Väder:
    def __init__(self,datum,plats,symbolnr,symbolnamn,vindriktning,vindgrad,
              vindtyp,vindhastighet,temperatur,tryck,nederbörd,uppgång,nedgång):
        self.datum = datum
        self.plats = plats
        self.symbolnr = symbolnr
        self.symbolnamn = self.fixa_symbolnamn(symbolnr,symbolnamn)
        self.vindriktning = vindriktning.replace('E','Ö').replace('W','V')
        self.vindgrad = vindgrad
        self.vindtyp = self.fixa_vindtyp(vindhastighet)
        self.vindhastighet = vindhastighet
        self.vindkmh = str(round(float(vindhastighet)*3.6))
        self.beaufort = self.fixa_beaufort(vindhastighet)
        self.beaufortverkan = self.fixa_beaufortverkan(self.beaufort) 
        self.temperatur = temperatur
        self.kyleffekt = self.fixa_kyleffekt(temperatur,vindhastighet)
        self.tryck = tryck
        self.nederbörd = nederbörd
        self.soluppgång = uppgång
        self.solnedgång = nedgång

    def __str__(self):
        r = 'Datum: ' + self.datum + '\nPlats: '+ self.plats
        r += '\nSymbolnr: ' + self.symbolnr + '\nSymbolnamn: ' + self.symbolnamn
        r += '\nVindriktning: '+ self.vindriktning
        r += '\nVindgrad: ' + self.vindgrad + '°\nVindhastighet: '+ self.vindhastighet
        r += ' m/s\nVindtyp: ' + self.vindtyp + '\nTemperatur: ' + self.temperatur
        r += ' °C\nLufttryck: ' + self.tryck + ' hPa\nNederbörd: ' + self.nederbörd
        r += ' mm\nSoluppgång: ' + self.soluppgång + '\nSolnedgång: ' + self.solnedgång
        r += '\n\n'
        return r

    def fixa_symbolnamn(self,nr,namn):
        dict = {'1':'Soligt',
                '2':'Lätt molnigt',
                '3':'Halvklart',
                '4':'Molnigt',
                '5':'Regnbyar',
                '6':'Regnbyar med åska',
                '7':'Snöblandat regn',
                '8':'Snöbyar',
                '9':'Regn',
                '10':'Kraftigt regn',
                '11':'Regn och åska',
                '12':'Snöblandat regn',
                '13':'Snö',
                '14':'Snö och åska',
                '15':'Dimma'
                }

        return dict.get(nr,namn)

    def fixa_vindtyp(self,hastighet):
        try:
            h = float(hastighet)
            if  h <= 0.2: r = 'Lugnt'
            elif  h <= 3.3: r = 'Svag vind'
            elif  h <= 7.9: r = 'Måttlig vind'
            elif  h <= 13.8: r = 'Frisk vind'
            elif  h <= 20.7: r = 'Hård vind'
            elif  h <= 24.4: r = 'Mycket hård vind'
            elif  h <= 28.4: r = 'Storm'
            elif  h <= 32.6: r = 'Svår storm'
            elif  h <= 100: r = 'Orkan'
            else: r = 'Oidentifierad'
        except ValueError:
            r = 'Okänd'
        return r

    def fixa_beaufort(self,hastighet):
        try:
            h = float(hastighet)
            if  h <= 0.2: r = 0
            elif  h <= 1.5: r = 1
            elif  h <= 3.3: r = 2
            elif  h <= 5.4: r = 3
            elif  h <= 7.9: r = 4
            elif  h <= 10.7: r = 5
            elif  h <= 13.8: r = 6
            elif  h <= 17.1: r = 7
            elif  h <= 20.7: r = 8
            elif  h <= 24.4: r = 9
            elif  h <= 28.4: r = 10
            elif  h <= 32.6: r = 11
            elif  h <= 100: r = 12
            else: r = 'Oidentifierad'
        except ValueError:
            r = -1
        return r

    def fixa_beaufortverkan(self,nr):
        dict = {0:'Rök stiger rätt upp, löv hänger stilla',
                1:'Knappt märkbar för känseln, löv rör sig sakta, skorstensrök driver i vindens riktning',
                2:'En vindflöjel visar vindens riktning',
                3:'Vinden sträcker en vimpel, sätter blad och tunna kvistar i oavbruten rörelse',
                4:'Kvistar och tunna grenar rör sig. Damm och lössnö virvlar upp',
                5:'Mindre lövträd börjar svaja. Vågor med utpräglade kammar på större insjöar',
                6:'Stora trädgrenar sätts i rörelse. Det viner i telegraf- och telefontrådar',
                7:'Hela träd börjar svaja. Man går ej obehindrat mot vinden',
                8:'Kvistar bryts från träden och det börjar bli besvärligt att gå i det fria',
                9:'Mindre skador på hus. Rökhuvar och taktegel blåser ner',
                10:'Sällsynt i inlandet. Träd ryckas upp med roten, betydande skador på hus',
                11:'På stora ytor i skog har alla träd fällts av vinden, stora fartyg som nyss synts försvinner bakom vågberg, havet helt vitt, skum i luften försvårar sikten',
                12:'Stora föremål flyger i luften, fönster blåser in, byggnadsställningar rasar, båtar kastas upp på land, allmän ödeläggelse'
                }

        return dict.get(nr,'Unknown, something went terribly wrong')

    def fixa_kyleffekt(self,temp,vind):
        #http://www.smhi.se/kunskapsbanken/meteorologi/vindens-kyleffekt-1.259
        try:
            T = float(temp)
            v = float(vind)**0.16
            kyl = 13.12+0.6215*T-13.956*v+0.487*T*v
            if kyl>T:kyl=T
            kyl = str(round(kyl)).split('.')[0]
        except:
            kyl = '-'
        return str(kyl)

def getXML(basurl):
    #basurl = 'www.yr.no/place/Sverige/Stockholm/Tyresö_Kommun/forecast.xml'
    url = 'http://' + urllib.parse.quote(basurl)    #Hanterar icke-Asciitecken

    response = urllib.request.urlopen(url)
    xml = response.read().decode('utf-8')
    return xml

def sun(lat,lon,start,stop):
    """Here comes the sun"""
    bas = 'http://api.yr.no/weatherapi/sunrise/1.1/?lat={};lon={};from={};to={}'
    basurl = bas.format(lat,lon,start,stop)
    response = urllib.request.urlopen(basurl)
    xml = response.read().decode('utf-8')
    soup = BeautifulSoup(xml,'html.parser')
    sunlist = []
    add = 1 + time.localtime().tm_isdst
    #sunlist = [(i['rise'].split('T')[1][:5],i['set'].split('T')[1][:5]) for i in soup.find_all('sun')]
    for i in soup.find_all('sun'):
        ri = i['rise'].split('T')[1][:5]
        ri = ri.split(':')
        ri = str(int(ri[0])+add).zfill(2) + ':' + ri[1]

        se = i['set'].split('T')[1][:5]
        se = se.split(':')
        se = str(int(se[0])+add).zfill(2) + ':' + se[1]
        sunlist.append((ri,se))
    return sunlist

def importera(plats='Sverige/Stockholm/Tyresö_Kommun'):
    try:xml = getXML('www.yr.no/place/' + plats + '/forecast.xml')
    except:
        time.sleep(0.1)
        xml = getXML('www.yr.no/place/' + plats + '/forecast.xml')
    soup = BeautifulSoup(xml,'html.parser')
    #return soup

    prognoser = soup.find_all('time')
    nu = prognoser[0]
    imorgon = [i for i in prognoser if i['from'][:10]==akt(1)][2]
    try:övermorgon = [i for i in prognoser if i['from'][:10]==akt(2)][2]
    except IndexError:
        övermorgon = [i for i in prognoser if i['from'][:10]==akt(2)]
        övermorgon = övermorgon[len(övermorgon)-1]
    proglist = [nu,imorgon,övermorgon]
    

    lat = soup.location.location['latitude']
    lon = soup.location.location['longitude']
    start = akt()
    stop = akt(2)
    plats = soup.location.find('name').text

    sunlist = sun(lat,lon,start,stop)


    väderlist = [skapa_väder(plats,proglist[i],sunlist[i]) for i in range(len(proglist))]
    return väderlist

def skapa_väder(plats,prog,sunprog):
    datum = prog['from'][:10]
    plats = plats
    symbolnr = prog.symbol['number']
    symbolnamn = prog.symbol['name']
    vindriktning = prog.winddirection['code']
    vindgrad = prog.winddirection['deg']
    vindhastighet = prog.windspeed['mps']
    vindtyp = prog.windspeed['name']
    temperatur = prog.temperature['value']
    tryck = prog.pressure['value']
    uppgång = sunprog[0]
    nedgång = sunprog[1]
    nederbörd = prog.precipitation['value']
    
    v = Väder(datum,plats,symbolnr,symbolnamn,vindriktning,vindgrad,
              vindtyp,vindhastighet,temperatur,tryck,nederbörd,uppgång,nedgång)

    return v


def akt(dag = 0):
    tid = time.localtime(time.time() + dag*3600*24)
    år = str(tid.tm_year).zfill(2)
    månad = str(tid.tm_mon).zfill(2)
    dag = str(tid.tm_mday).zfill(2)

    r = år + '-' + månad + '-' + dag
    return r

if __name__=='__main__':
    
    s=importera()
    for i in s:
        print(i)
    input('Tryck ENTER för att avsluta:')
