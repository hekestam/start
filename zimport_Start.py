import Import_rss as RSS
import time, datetime
import Import_vaderdata2 as Weather
import Import_namnsdag2 as Namn
import Import_tvdata6 as TVData
from html import escape

def importera_mall():
    filnamn = 'docs/startmall.htm'
    with open(filnamn,encoding='utf8') as fil:
        content = fil.read()
    return content

def exportera(content):
    filnamn = 'docs/start.htm'

    with open(filnamn,'w',encoding='utf8') as fil:
        fil.write(content)

def empty_dict():
    d = dict()
    d['name-text'] = 'Hej'
    d['name-title'] = 'Undefined'

    d['kalendergif'] = '1.gif'
    d['veckonr'] = '00'
    d['kalenderdag'] = '00'
    d['kalendermånad'] = 'Unknown'
    d['kalenderår'] = '1993'
    d['veckodag'] = 'Unknown'
    d['uppdaterad'] = 'Undefined'

    for i in range(1,4):
        d['winddir-text{i}'.format(i=i)] = 'Hej'
        d['winddir-temp-text{i}'.format(i=i)] = 'Hej'
        d['weatherdate{i}'.format(i=i)] = '00/0'
        d['weather-temp-text{i}'.format(i=i)] = 'Hej'
        d['sunrise{i}'.format(i=i)] = '-- : --'
        d['sunset{i}'.format(i=i)] = '-- : --'
        d['weathertype{i}'.format(i=i)] = 'Undefined'
        d['weatherdayname'] = 'Undefined'
        d['weathertemp{i}'.format(i=i)] = '0'
        d['winddirection{i}'.format(i=i)] = 'N'
        d['weathersymbol{i}'.format(i=i)] = '1'
        d['winddirtext{i}'.format(i=i)] = 'Hej'
        d['windspeed{i}'.format(i=i)] = '0.0'
        d['windtype{i}'.format(i=i)] = 'Undefined'

    for i in range(1,16):
        d['tv-title-active-text{i}'.format(i=i)] = 'Hej'
        d['tv-title-active-start{i}'.format(i=i)] = '-- : --'
        d['tv-title-active-name{i}'.format(i=i)] = 'Undefined'
        d['tv-title-text{i}'.format(i=i)] = 'Hej'
        d['tv-title-start{i}'.format(i=i)] = '-- : --'
        d['tv-title-name{i}'.format(i=i)] = 'Undefined'

    for i in range(1,4):
        for j in range(0,7):
            d['rubriktext{i}_{j}'.format(i=i,j=j+1)] = 'Tom beskrivning'
            d['rubriktitle{i}_{j}'.format(i=i,j=j+1)] = 'Tom rubrik'
            d['rubrikurl{i}_{j}'.format(i=i,j=j+1)] = '#'
            d['rubriktid{i}_{j}'.format(i=i,j=j+1)] = '-- : --'
    


    return d
    

def getRSS():
    rdict = dict()
    try:
        url1 = 'http://www.dn.se/nyheter/rss/'
        url2 = 'http://www.dn.se/ekonomi/rss/senaste-nytt'
        url3 = 'http://www.dn.se/kultur-noje/rss'#'http://www.dn.se/kultur-noje/rss/senaste-nytt'
        
        rsslista = [RSS.importera(url1),RSS.importera(url2),RSS.importera(url3)]

        for i,feed in enumerate(rsslista,1):
            for j in range(0,min([len(feed.itemlist),7])):
                textvalue = feed.itemlist[j].description.replace('\xad','').replace("'","\\'").replace('"','\\"').replace('\n',' ')
                rdict['rubriktext{i}_{j}'.format(i=i,j=j+1)] = escape(textvalue).replace('\r','').replace('\n','')
                if rdict['rubriktext{i}_{j}'.format(i=i,j=j+1)]=='': rdict['rubriktext{i}_{j}'.format(i=i,j=j+1)] = 'Odefinierad'

                rubrikvalue = feed.itemlist[j].title.replace('\xad','')
                rdict['rubriktitle{i}_{j}'.format(i=i,j=j+1)] = escape(rubrikvalue)

                urlvalue = feed.itemlist[j].link
                #print(repr(urlvalue))
                rdict['rubrikurl{i}_{j}'.format(i=i,j=j+1)] = urlvalue

                tidvalue = feed.itemlist[j].time[:5]
                rdict['rubriktid{i}_{j}'.format(i=i,j=j+1)] = tidvalue
    except:
       print('Rss-Error')
       #raise

    return rdict

def getCalendar():
    rdict = dict()
    try:
        tid = time.localtime()
        month = {1:'Januari',
                 2:'Februari',
                 3:'Mars',
                 4:'April',
                 5:'Maj',
                 6:'Juni',
                 7:'Juli',
                 8:'Augusti',
                 9:'September',
                 10:'Oktober',
                 11:'November',
                 12:'December'}
        weekday = {0:'Måndag',1:'Tisdag',2:'Onsdag',3:'Torsdag',4:'Fredag',5:'Lördag',6:'Söndag'}
        
        rdict['kalendergif'] = str(time.localtime().tm_mday) + '.gif'
        rdict['veckonr'] = str(datetime.date(tid[0],tid[1],tid[2]).isocalendar()[1])
        rdict['kalenderdag'] = str(tid[2])
        rdict['kalendermånad'] = month.get(tid[1],'Unknown')
        rdict['kalenderår'] = str(tid[0])
        rdict['veckodag'] = weekday.get(tid[6],'Unknown')

        rdict['uppdaterad'] = time.strftime('%Y-%m-%d %H:%M')
    
    except:
        print('Calendar-Error')

    return rdict

def getWeather():
    rdict = dict()
    try:
        i = Weather.importera()

        datum1 = i[0].datum.split('-')
        datum2 = i[1].datum.split('-')
        datum3 = i[2].datum.split('-')

        rdict['weatherdate1'] = datum1[2].lstrip('0') + '/' + datum1[1].lstrip('0')
        rdict['weatherdate2'] = datum2[2].lstrip('0') + '/' + datum2[1].lstrip('0')
        rdict['weatherdate3'] = datum3[2].lstrip('0') + '/' + datum3[1].lstrip('0')

        rdict['sunrise1'] = i[0].soluppgång
        rdict['sunset1'] = i[0].solnedgång
        rdict['sunrise2'] = i[1].soluppgång
        rdict['sunset2'] = i[1].solnedgång
        rdict['sunrise3'] = i[2].soluppgång
        rdict['sunset3'] = i[2].solnedgång

        rdict['weathertype1'] = i[0].symbolnamn
        rdict['weathertype2'] = i[1].symbolnamn
        rdict['weathertype3'] = i[2].symbolnamn

        weekday = {0:'Måndag',1:'Tisdag',2:'Onsdag',3:'Torsdag',4:'Fredag',5:'Lördag',6:'Söndag'}
        rdict['weatherdayname'] = weekday.get(time.localtime(time.time()+3600*48).tm_wday,'Unknown')

        rdict['weathertemp1'] = i[0].temperatur
        rdict['weathertemp2'] = i[1].temperatur
        rdict['weathertemp3'] = i[2].temperatur

        rdict['windspeed1'] = i[0].vindhastighet
        rdict['windspeed2'] = i[1].vindhastighet
        rdict['windspeed3'] = i[2].vindhastighet

        rdict['winddirection1'] = i[0].vindriktning.replace('Ö','E').replace('V','W')
        rdict['winddirection2'] = i[1].vindriktning.replace('Ö','E').replace('V','W')
        rdict['winddirection3'] = i[2].vindriktning.replace('Ö','E').replace('V','W')

        rdict['winddegree1'] = i[0].vindgrad
        rdict['winddegree2'] = i[1].vindgrad
        rdict['winddegree3'] = i[2].vindgrad

        rdict['windtype1'] = i[0].vindtyp
        rdict['windtype2'] = i[1].vindtyp
        rdict['windtype3'] = i[2].vindtyp

        rdict['weathersymbol1'] = i[0].symbolnr
        rdict['weathersymbol2'] = i[1].symbolnr
        rdict['weathersymbol3'] = i[2].symbolnr

        rdict['weather-temp-text1'] = '<b>'+rdict['weathertype1']+'</b><br><br>Temperatur: '
        rdict['weather-temp-text1'] += rdict['weathertemp1']+' °C<br>Kyleffekt: '
        rdict['weather-temp-text1'] += i[0].kyleffekt+' °C<br>Lufttryck: '+i[0].tryck+' mbar<br>'
        rdict['weather-temp-text1'] += 'Nederbörd: '+ i[0].nederbörd+' mm'

        rdict['weather-temp-text2'] = '<b>'+rdict['weathertype2']+'</b><br><br>Temperatur: '
        rdict['weather-temp-text2'] += rdict['weathertemp2']+' °C<br>Kyleffekt: '
        rdict['weather-temp-text2'] += i[1].kyleffekt+' °C<br>Lufttryck: '+i[1].tryck+' mbar<br>'
        rdict['weather-temp-text2'] += 'Nederbörd: '+ i[1].nederbörd+' mm'

        rdict['weather-temp-text3'] = '<b>'+rdict['weathertype3']+'</b><br><br>Temperatur: '
        rdict['weather-temp-text3'] += rdict['weathertemp3']+' °C<br>Kyleffekt: '
        rdict['weather-temp-text3'] += i[2].kyleffekt+' °C<br>Lufttryck: '+i[2].tryck+' mbar<br>'
        rdict['weather-temp-text3'] += 'Nederbörd: '+ i[2].nederbörd+' mm'

        d['winddir-text1'] = '<b>'+i[0].vindtyp+'</b><br><br>Styrka: '
        d['winddir-text1'] += str(i[0].vindhastighet)+' m/s (~'+i[0].vindkmh+' km/h)'
        d['winddir-text1'] += '<br>Riktning: '+str(i[0].vindgrad)+'° ('+str(i[0].vindriktning)
        d['winddir-text1'] += ')<br><br>'
        d['winddir-text1'] += 'Index '+str(i[0].beaufort)+' av 12 på Beaufortskalan.'
        d['winddir-text1'] += '<br><br>'+i[0].beaufortverkan+'.'

        d['winddir-text2'] = '<b>'+i[1].vindtyp+'</b><br><br>Styrka: '
        d['winddir-text2'] += str(i[1].vindhastighet)+' m/s (~'+i[1].vindkmh+' km/h)'
        d['winddir-text2'] += '<br>Riktning: '+str(i[1].vindgrad)+'° ('+str(i[1].vindriktning)
        d['winddir-text2'] += ')<br><br>'
        d['winddir-text2'] += 'Index '+str(i[1].beaufort)+' av 12 på Beaufortskalan.'
        d['winddir-text2'] += '<br><br>'+i[1].beaufortverkan+'.'

        d['winddir-text3'] = '<b>'+i[2].vindtyp+'</b><br><br>Styrka: '
        d['winddir-text3'] += str(i[2].vindhastighet)+' m/s (~'+i[2].vindkmh+' km/h)'
        d['winddir-text3'] += '<br>Riktning: '+str(i[2].vindgrad)+'° ('+str(i[2].vindriktning)
        d['winddir-text3'] += ')<br><br>'
        d['winddir-text3'] += 'Index '+str(i[2].beaufort)+' av 12 på Beaufortskalan.'
        d['winddir-text3'] += '<br><br>'+i[2].beaufortverkan+'.'

    except:
        print('Weather-Error')
        raise
        
    return rdict

def getName():
    rdict = dict()
    try:
        name = Namn.master()
        rdict['name-text'] = name[1].replace('\n','<br>').replace('"','&quot;').replace("'","\\'")
        rdict['name-title'] = ' '.join(name[0]) 
    except:
        print('Name-Error')
    return rdict

def getTV():
    rdict = dict()
    try:
        def fix_title(text):
            if len(text)>=30:
                text = text[:27]+'...'
            return text
        
        date = TVData.akt()
        channelnamelist = ['svt1.svt.se','svt2.svt.se','tv3.se','tv4.se','kanal5.se','tv6.se','sjuan.se']
        channellist = list()

        for channel in channelnamelist:
        
            templist = TVData.master(channel,date)

            for i in range(len(templist)-1,-1,-1):
                if templist[i].avslutad():
                    del templist[i]
            channellist.append(templist)

        for i in range(len(channelnamelist)):
            j = str(i+1)
            templist = channellist[i]

            rdict['tv-title-active-text'+j] = '<b>'+templist[0].namn + '</b><br><br>'
            rdict['tv-title-active-text'+j] += templist[0].beskrivning
            rdict['tv-title-active-text'+j] = rdict['tv-title-active-text'+j].replace('"','&quot;').replace("'","&apos;")
            rdict['tv-title-active-start'+j] = templist[0].start[:2]+':'+templist[0].start[2:]
            rdict['tv-title-active-name'+j] = fix_title(templist[0].namn)
            andel = str(templist[0].andel()*100).split('.')[0]
            andeltext = '<br><br><img src=Images/lgray3.gif width={andel}%'
            andeltext += ' height=3px>'
            andeltext += '<img src=Images/lblack.gif width={andel2}%'
            andeltext += ' height=3px>'
            andeltext = andeltext.format(andel=andel,andel2=100-int(andel))
            rdict['tv-title-active-text'+j] += andeltext

            rdict['tv-title-text'+j] = '<b>'+templist[1].namn + '</b><br><br>'
            rdict['tv-title-text'+j] += templist[1].beskrivning
            rdict['tv-title-text'+j] = rdict['tv-title-text'+j].replace('"','&quot;').replace("'","&apos;")
            rdict['tv-title-start'+j] = templist[1].start[:2]+':'+templist[1].start[2:]
            rdict['tv-title-name'+j] = fix_title(templist[1].namn)

    except:
        print('TV-Error')
    return rdict

    

if __name__ == '__main__':
    d = empty_dict()
    d.update(getRSS());print('RSS')
    d.update(getCalendar());print('Calendar')
    d.update(getWeather());print('Weather')
    d.update(getName());print('Name')
    d.update(getTV());print('TV\n')
    try: print(d['rubriktext3_3'])
    except: print('Unicode :)')
    i = importera_mall()
    i = i.format(**d)
    exportera(i)
    time.sleep(1)
    
    
