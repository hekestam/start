import urllib.request
import urllib.parse
from time import sleep
import os
import datetime
import time
import json
from bs4 import BeautifulSoup
import sys

DEBUG = False

if 'idlelib' in sys.modules:DEBUG = True

def wikipedia(nurl):
    url = 'http://sv.wikipedia.org' + nurl
    response = urllib.request.urlopen(url).read().decode('utf-8')


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

def wikipedia2(nurl):
    url = 'http://sv.wikipedia.org' + nurl
    response = urllib.request.urlopen(url).read().decode('utf-8')

    s = BeautifulSoup(response,'html.parser')
    a = s.find("div", {"id": "mw-content-text"})
    sup = a.find_all('sup')
    [k.decompose() for k in sup]
    b=a.find_all('p')

    i = [k.text for k in b]
    res = '\n'.join(i)

    res = rensa_förtext(res,'(',')')
    res = rensa_förtext(res,'[',']')

    res = res.replace('&#160;',' ').replace('’','"').replace('”','"')
    res = res.replace('  ',' ').replace(' .','.')
    res = res.strip('.').strip('\n').rstrip('\n').replace(' ,',',').replace(',.','.')

    res = (res + '.').replace('.','. ').replace('.  ','. ').replace(',.','.')
    res = res.replace('. .','.').replace('. .','.').replace(', .','.')
    res = res.replace('\n\n\n','\n').replace('\n\n','\n')
    res = res.replace('\n','\n\n')
    
    if res.endswith('..') and not res.endswith('...'):
        res = res.rstrip('..') + '.'
    if res.endswith('. .'):
        res = res.strip('. .') + '.'



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

def namnsdag():
    url = 'https://sv.wikipedia.org/wiki/Lista_%C3%B6ver_namnsdagar_i_Sverige_i_datumordning'
    a = urllib.request.urlopen(url).read()
    c = BeautifulSoup(a,'html.parser')
    d = c.find_all('td')

    for i in range(len(d)):
        try:
            if d[i].a.text.upper() == idag().upper():#'5 Juli'.upper():
                break
        except:
            continue

    e = d[i+1].children
    r = []

    for i in e:
        if i.name == 'a':
            r.append((i.text,i['href']))
	
    return r#d[i+1].a.text

def idag():
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

    m = month[int(time.strftime('%m'))]

    r = str(int(time.strftime('%d'))) + ' ' + str(m)

    return r

def export(d):

    text = json.dumps(d)

    filnamn = 'zdata\\namnsdag.txt'
    with open(filnamn,'w',encoding = 'utf8') as fil:
        fil.write(text)

def gammal_tid():
    fil = 'zdata\\namnsdag.txt'
    try:
        t = os.path.getmtime(fil)
        s = datetime.datetime.fromtimestamp(t)
        r = str(s)[:10]
    except:
        r = False
    return r

def akt(dag = 0):
    tid = time.localtime(time.time() + dag*3600*24)
    år = str(tid.tm_year).zfill(2)
    månad = str(tid.tm_mon).zfill(2)
    dag = str(tid.tm_mday).zfill(2)

    r = år + '-' + månad + '-' + dag
    return r

def master_ny():
    try:
        ndag = namnsdag()
        dagar = [i[0] for i in ndag]
        #print(ndag)
        #print(dagar)
        
        w = wikipedia2(ndag[0][1])

        d = dict()
        d['ndag'] = dagar
        d['ntext'] = w
        export(d)
        
        return [[i[0] for i in ndag],w]
    except:
        #raise
        global t
        try:
            t = t+1
        except:
            t=1
        if t > 10:
            return [['Undefined'],'Collection failed.']
        else:
            return master_ny()

def master_gammal():
    filnamn = 'zdata\\namnsdag.txt'

    with open(filnamn,'r',encoding = 'utf8') as fil:
        d = json.loads(fil.read())

    return [d['ndag'],d['ntext']]

def master():
    if DEBUG:
        return master_ny()
    if gammal_tid() == akt():
        return master_gammal()
    else:
        return master_ny()
#-----------------------Huvudprogrammet--------------------------#
def main():
    m = master()
    try:
        print(m[1])
    except:
        print(m[1].encode('cp850','replace').decode('cp850'))

    input('\n\nTryck ENTER för att avsluta:')
    s = 0

if __name__ == '__main__':
    tid1 = time.time()
    main()
    tid2 = time.time() - tid1
    print(tid2)
