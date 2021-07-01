import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import time
import html.parser
from datetime import datetime

class Feed:
    def __init__(self,link,title,description,itemlist):
        self.link = link
        self.title = title
        self.description = description
        self.itemlist = itemlist

    def __str__(self):
        r = '\n'.join([self.link,self.title,self.description])
        r += '\n\n' + ''.join([str(i) for i in self.itemlist][:7])
        r = self.fix_Unicode(r.strip())
        return r

    def fix_Unicode(self,text):
        fixlist = [('\u201d','"'),('\u2013','-')]
        for i in fixlist:
            text = text.replace(i[0],i[1])
        return text

class FeedItem:
    def __init__(self,title,link,description,date,time):
        self.title = title
        self.link = link
        self.description = description
        date,time = self.fix_GMT(date,time)
        self.date = date
        self.time = time

        if description == ' ' or description == '\xa0':
            self.description = 'Beskrivning saknas'

    def __str__(self):
        r = '\n'.join([self.title,self.link,self.description,self.date,self.time])
        return r + '\n\n'

    def fix_GMT(self,date,t):
        date = list(map(int,date.strip().split('-')))
        t = list(map(int,t[:5].split(':')))
        fixed = time.gmtime(time.mktime((date[0],date[1],date[2],t[0],t[1],0,0,0,-1))+7200)
        rdate = str(fixed.tm_year) + '-' + str(fixed.tm_mon) + '-' + str(fixed.tm_mday)
        rtime = str(fixed.tm_hour).zfill(2) + ':' + str(fixed.tm_min).zfill(2) + ':' + str(fixed.tm_sec).zfill(2)
        return rdate,rtime

def rensa_HTML(text):
    start = text.find('<')
    stopp = text.find('>')

    text = text.replace(text[start:stopp+1],'')
    
    if start != -1 and stopp != -1 and start < stopp:
        text = rensa_HTML(text)

    return text

def getXML(basurl):
    if basurl[:7] == 'http://':
        basurl = basurl[7:]
        
    url = 'http://' + urllib.parse.quote(basurl)    #Hanterar icke-Asciitecken

    response = urllib.request.urlopen(url)
    xml = response.read().decode('utf-8').strip('\ufeff')
    return xml

def importera(url):
    xml = getXML(url)
    soup = BeautifulSoup(xml,'html.parser')
    #unescape = html.parser.HTMLParser().unescape
    unescape = lambda x: x

    link = soup.find('link').text
    title = soup.find('title').text
    description = soup.find('description').text

    itemxmllist = soup.find_all('item')[:8]
    itemlist = list()

    for i in itemxmllist:
        #print(i)
        ititle = i.title.text
        ilink = unescape(i.guid.text)
        #breakpoint()
        idescription = unescape(rensa_HTML(i.description.text))
        #idate = i.find('dc:date').text[:10]
        #itime = i.find('dc:date').text[11:19]
        dt = i.pubdate.text.split(' +')[0]
        dt = datetime.strptime(dt,'%a, %d %b %Y %H:%M:%S')
        idate = str(dt)[:10]
        itime = str(dt)[11:]
        fi = FeedItem(ititle,ilink,idescription,idate,itime)
        itemlist.append(fi)


    r = Feed(link,title,description,itemlist)

    return r

if __name__ == '__main__':
    url = 'http://www.dn.se/kultur-noje/rss/senaste-nytt'
    i = importera(url)
    r = str(i).encode('cp850','replace').decode('cp850')
    print(r)
    

    print()

    input('Tryck ENTER för att avsluta:')
