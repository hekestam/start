import urllib.request
from time import sleep

url = "http://www.start.se"

def citat():
    response = urllib.request.urlopen(url)
    html = response.read().decode('latin_1','ignore')
    html =  html.split('<span style="color: #666666;">')
    #print(len(html))
    html = html[1].split('</td>')[0].replace('</span>','').replace('\n','').replace('\t','')
    #print(html)
    html = html.replace('\r','')

    return html

#######################################################################
#fil = open('citat.txt','r')
#text = 

li = list()
blista = list()
b = 0
c= 0
while b < 500:
    a = citat()
    c += 1 
    print(c)
    #print(a,end='\n\n')
    sleep(0.1)
    if a not in li:
        li.append(a)
        if b != 0:
            blista.append(b)
            print('b = ' +  str(b))
            b = 0
    else:
        b += 1
    if c > 10800:
        break

blista.append(b)

filnamn = 'citat4.txt'
fil = open(filnamn,'a')
for i in range(len(li)):
    fil.write(li[i])
    fil.write('\n\n')
fil.close()
