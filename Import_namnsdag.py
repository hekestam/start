import urllib.request
import urllib.parse
from time import sleep
import os
import datetime
import time
import json

def ladda(datum):
    url = 'http://api.dryg.net/dagar/v2/' + datum
    #print(url)

    response = urllib.request.urlopen(url).read()
    
    r = json.loads(response.decode('utf-8'))

    return r

def akt():
    tid = time.localtime(time.time())
    år = str(tid.tm_year)
    månad = str(tid.tm_mon)
    dag = str(tid.tm_mday)
    if len(månad) == 1:
        månad = '0' + månad
    if len(dag) == 1:
        dag = '0' + dag
    r = år + '-' + månad + '-' + dag
    return r

def dat():
    tid = time.localtime(time.time())
    år = str(tid.tm_year)
    månad = str(tid.tm_mon)
    dag = str(tid.tm_mday)
    if len(månad) == 1:
        månad = '0' + månad
    if len(dag) == 1:
        dag = '0' + dag
    r = år + '/' + månad + '/' + dag
    return r

def namnsdag(dic):
    #print(dic['dagar'][akt()])
    n = dic['dagar'][akt()]['namnsdag']
    if type(n) == type(list()):
        r = n
    elif type(n) == type(str()):
        r = [n]

    r = [i.capitalize() for i in r]

    return r

def wikipedia(namn):
    basurl = 'sv.wikipedia.org/wiki/' + namn
    url = 'http://' + urllib.parse.quote(basurl)    #Hanterar icke-Asciitecken
    response = urllib.request.urlopen(url).read().decode('utf-8')

    if 'förgreningssida' in response or 'För andra betydelser' or 'förteckning över artiklar':
        try:
            basurl = 'sv.wikipedia.org/wiki/' + namn + '_(namn)'
            url = 'http://' + urllib.parse.quote(basurl)    #Hanterar icke-Asciitecken
            response2 = urllib.request.urlopen(url).read().decode('utf-8')
            response = response2
        except:
            try:
                basurl = 'sv.wikipedia.org/wiki/' + namn + '_(förnamn)'
                url = 'http://' + urllib.parse.quote(basurl)    #Hanterar icke-Asciitecken
                response2 = urllib.request.urlopen(url).read().decode('utf-8')
                response = response2
            except:
                pass

    res = response.split('<div id="mw-content-text" lang="sv" dir="ltr" class="mw-content-ltr">')
    #res = rensa_förtext(res[1],'<p><i>','</i>.</p>',höger=True)
    res = rensa_förtext(res[1].replace('</i>.</p>','</i></p>'),'<p><i>','</i></p>',höger=True)
    resp = res.split('</p>')
    
    res = resp[0]
    #print(len(resp))
    if len(res) < 2100:
        try:
            #print(resp[0])
            res = res + resp[1]
            
        except:
            pass
        
    res = rensa_förtext(res,'<dl>','</dl>',True)
    res = rensa_förtext(res,'<dd><i>','</i></dd>')
    res = rensa_förtext(res,'<div class="thumb tright">','</di',höger = True)
    
    
    res = rensa_förtext(res,'<table','</table>',höger=True)
    res = rensa_förtext(res,'<p><i>','</i>',höger=True)
    
    res = rensa_HTML(res)
    res = rensa_förtext(res,'(',')')
    res = rensa_förtext(res,'[',']')
    res = res.replace('&#160;',' ').replace('’','"').replace('  ',' ').replace(' .','.')
    res = res.strip('.').strip('\n').rstrip('\n').replace('\n','\n\n').replace(' ,',',')
    res = (res + '.').replace('.','. ').replace('.  ','. ')
    if res.endswith('..') and not res.endswith('...'):
        res = res.rstrip('..') + '.'
    if res.endswith('. .'):
        res = res.strip('. .') + '.'

##    a = 0
##    while a != -1:
##        b = res.find('..',a+1)
##        c = res.find('...',a+1)
##        if c != b:
##            res = res.replace('..','.',1)
##        a = b
    return res

def rensa_HTML(text):
    start = text.find('<')
    stopp = text.find('>')

    #print(start,stopp)
    text = text.replace(text[start:stopp+1],'')
    #print(text)
    
    if start != -1 and stopp != -1 and start < stopp:
        text = rensa_HTML(text)


    return text

def rensa_förtext(text,sta,sto,höger = False):
    start = text.find(sta)
    if höger:
        stopp = text.rfind(sto)
    else:
        stopp = text.find(sto)

    if len(sto)==1:
        text = text.replace(sto,'',1)
    
    #print(start,stopp)
    if start != -1 and stopp != -1 and start < stopp:
        text = text.replace(text[start:stopp],'')
        text = rensa_förtext(text,sta,sto)
            


    return text

def master():
    try:
        datum = dat()
        dag = ladda(datum)
        ndag = namnsdag(dag)
        
        w = wikipedia(ndag[0])
        return [ndag,w]
    except:
        global t
        try:
            t = t+1
        except:
            t=1
        if t > 10:
            return [['Undefined'],'Collection failed.']
        else:
            return master()
#-----------------------Huvudprogrammet--------------------------#
if __name__ == '__main__':
    m = master()
    try:
        print(m[1])
    except:
        print(m[1].encode('cp850','replace').decode('cp850'))

    input('\n\nTryck ENTER för att avsluta:')
    s = 0
