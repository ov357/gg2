# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 07:58:45 2017
@author: milal
"""

from flask import Flask
from flask import render_template
from flask import request
#import redis
import feedparser
import random
import requests
from bs4 import BeautifulSoup
import re
import operator


app = Flask(__name__)

RSS_FEEDS = {'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn':'http://rss.cnn.com/rss/edition.rss',
             'fox':'http://feeds.foxnews.com/foxnews/latest',
             'iol':'http://iol.co.za/cmlink/1.640'}


#def send_sms():
# send
#pass


@app.route("/gr", methods = ['GET', 'POST'])
def get_race(reu=1,crs=3):
    # from main page get all races details for url mapping
    api_root = 'http://www.turfoo.fr/programmes-courses/'
    api_root2 = 'http://www.turfoo.fr'
    api_url = api_root
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
    data = requests.get(api_url, headers = headers)
    soup = BeautifulSoup(data.content, 'html.parser')
    # print(data.text)
    z = soup.find_all('div', class_="programme_reunion")
    # programme reunion will contain tables of races for all differents reunions
    race_urls = []  #hold all races href  of the day
    for i in z:     #loop thru all reunions
        z1 = i.find_all('tr', class_="row")
        # loop on race of the reunion
        for j in z1:
            #for now we need to find qt - how ?
            #get all class = violet +href contain the url of races
            z2 = j.find_all('a', class_="violet")
            for k in z2[:1]:
                rc = k['href']    #this gives us the url of every race of the day
                print(k['href'])    #this gives us the url of every race of the day
                race_urls.append(rc)
            #print(len(z2),z2)
    # find the url requested by using r &c variables
    crs = 'course'+str(crs)
    reu = 'reunion'+str(reu)
    m = [s for s in race_urls if (crs in s) & (reu in s)]
    #print(m)
    #print(api_root2+m[0])
    # build reunion+r and course+c
    # find it in the race_urls array
    return str(api_root2+m[0])
    # now we get the page will all the races for the current day
    # build a list and detect the main one
    # in a dictionnary x = {'date' : 170612,
    #                       'reunion': '1',
    #                       'url' : 'urlreunion',
    #                       'urls' : [(1,urlcourse),(2,...)]
    #                       }
    #pass

#def savecotes_txt():
#pass


@app.route("/gc", methods = ['GET', 'POST'])
def get_cotes(dt='170612', reu=1, crs=1):
    reu = request.args.get("r")
    crs = request.args.get("c")
    # dt format = YYMMDD
    # here we need to get the cotes of the requested date/reunion/course
    api_root = 'http://www.turfoo.fr/programmes-courses/'
    api_url = api_root+'170612/reunion1-compiegne/course1-prix-major-fridolin/'
    api_url = str(get_race(reu,crs))
    print(api_url)
    #q={}&units=metric&appid=8a839a08492fc8191c3b9e02ddcf272b'
    #query = urllib.quote(query)
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
    payload = {}
    #url = api_url.format(query)
    #print(url)
    # data = urllib2.open(url).read() #urllib2 does not seem to exist for python3 try request instead
    data = requests.get(api_url, headers = headers, params = payload)
    #use bs4
    soup = BeautifulSoup(data.content, 'html.parser')
    # print(data.text)
    z = soup.find_all('div', class_="programme_partants")
    z1 = z[0].find_all('tr', class_="row")
    #z1 = z.find_all('tr', class_="row")
    # class="programme_partants"
    #print(len(z1))
    d1 = {}     #cotes1
    d2 = {}
    d3 = {}
    for e,i in enumerate(z1):
        #first regex to replace multiple \r\n by a space
        result = re.sub(r"(?sim)\r+|\n+", r"@", i.get_text())
        # replace multiple space by a ;
        result = re.sub(r"(?sim)@+", r";", result)
        t = result.split(';')
        # print(len(t),e+1,t[-5:-2])
        try:
            d1[e+1]=float(t[-5:-4][0])
        except:
            pass
        try:
            d2[e+1]=float(t[-4:-3][0])
        except:
            pass
        try:
            # d3 is normally containing zeturf cotes and may not be available
            d3[e+1]=float(t[-3:-2][0])
        except:
            pass
        #print(i.get_text())
    #print(z1)
    lt = sorted(d1.items(),key=operator.itemgetter(1))
    lt = [0]+[j for j,k in lt]
    lt1 = sorted(d2.items(),key=operator.itemgetter(1))
    lt1 = [0]+[j for j,k in lt1]
    try:
        lt2 = sorted(d3.items(),key=operator.itemgetter(1))
        lt2 = [0]+[j for j,k in lt2]
    except:
        pass
    print('Lt=',lt)
    print('Lt=1',lt1)
    try:
        print('Lt=2',lt2)
    except:
        print('looks like lt2/d3 are not available !')
    v = m4(lt,rt='raw',flg=11,rdm='n')
    #print(v)
    #return str(sorted(v))
    return render_template("m4.html", combs = sorted(v))


def storedb():
    # store somethin into redis DB and persist the data
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set('foo', 'bar')


def get_weather(query):
    api_url = 'http://api.openweathermap.org/data/2.5/weather'
    #q={}&units=metric&appid=8a839a08492fc8191c3b9e02ddcf272b'
    #query = urllib.quote(query)
    payload = {'q': query, 'appid': '8a839a08492fc8191c3b9e02ddcf272b'}
    #url = api_url.format(query)
    #print(url)
    # data = urllib2.open(url).read() #urllib2 does not seem to exist for python3 try request instead
    data = requests.get(api_url, params = payload)
    print(data.text)
    try:
        parsed = json.loads(data.text)
        weather = None
        if parsed.get("weather"):
            weather = {"description":parsed["weather"][0]["description"],
            "temperature":parsed["main"]["temp"],
            "city":parsed["name"]
            }
    except:
        weather = None
    return weather

DEFAULTS = {'publication' : 'bbc',
            'city' : 'LONDON,UK'
    }


@app.route("/", methods = ['GET', 'POST'])
def get_news():
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed=feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather("London,UK")
    #first_article = feed['entries'][0]
    #return render_template("home.html", articles = feed['entries'], weather = weather)

@app.route("/m4", methods = ['GET', 'POST'])
def m4(c=[0,1,2,3,4,5,6,7,8,9],flg = 9, rt = 'html', rdm='N'):
    # set flg = 11 to apply -1 in 6,7,8 and -1 in 9,10,11
    # provide 11 members LT
    # rt = html means that the routine will use the return render template
    # rt = raw will return combs as a list
    # rdm allow to shuffle the lt passed to m4 routine possible value = Y/N
    # rdm defaults to N
    dm = list(range(9,19))
    flg = request.args.get("flg")
    query = request.args.get("lt")
    #print(type(c))
    if query:
        c = query.split(',')
        c = [0]+c[:]
        c = [int(x) for x in c]
    if len(c) < 10:
        # complete lt with dummy numbers
        return ['not enough runners']
            #query += random.sample(dm,9)
        #print(type(c))
    if flg == '11':
        p1 = c[6:9]
        p2 = c[9:12]
        px1 = random.sample(p1,1)
        px2 = random.sample(p2,1)
        #remove them from p1 and p2
        p1.remove(px1[0])
        p2.remove(px2[0])
        c = c[:6]+p1+p2
        #print(c)
    # multis en 4 favos - c contient la liste type
    if rdm.upper() == 'Y':
        #print('entering rdm')
        c = [0]+random.sample(c[1:], len(c)-1)
        #print(random.shuffle(c[1:]))
    print('c=',c,' rdm = ',rdm)
    cbs = [
    		[1, 4, 2, 5],
    		[1, 4, 2, 9],
    		[1, 8, 2, 5],
    		[1, 8, 2, 9],
    		[1, 4, 2, 6],
    		[1, 4, 2, 7],
    		[1, 8, 2, 6],
    		[1, 8, 2, 7],
    		[2, 5, 3, 6],
    		[2, 5, 3, 7],
    		[2, 9, 3, 6],
    		[2, 9, 3, 7],
    		[2, 5, 3, 4],
    		[2, 5, 3, 8],
    		[2, 9, 3, 4],
    		[2, 9, 3, 8],
    		[3, 6, 1, 4],
    		[3, 6, 1, 8],
    		[3, 7, 1, 4],
    		[3, 7, 1, 8],
    		[3, 6, 1, 5],
    		[3, 6, 1, 9],
    		[3, 7, 1, 5],
    		[3, 7, 1, 9],
    	]
    l = [0,1,2]
    #print(r[:],c)
    combs = []
    for e1,i in enumerate(cbs):
        p = random.sample(l[:3],2)
        if (2 in p):
            c1 = []
            for j in i:
                #print(c[j], end='-')
                c1.append(c[j])
            #print()
            combs.append(c1)
    print(combs)
    if rt == 'html':
        return render_template("m4.html", combs = combs)
    else:
        return combs


@app.route("/eur", methods = ['GET', 'POST'])
def eur(c=[0,1,2,3,4,5,6,7,8,9],nb=10):
    #nb specifies the repetion number of 11's
    query = request.args.get("nb")
    if query:
        nb = int(query)
    # purpose :generate draws for euromillions
    # query = request.args.get("lt")
    #print(nb)
    l = list(range(1,51))
    s = list(range(1,13))
    s1 = random.sample(s,7)
    s2 = sorted(random.sample(s,3))
    x = random.sample(l,23)
    y =[]
    for q in range(nb):
        tmp = [0]+sorted(random.sample(x,11))
        y.append(tmp)
    #c = [0]+y
    #z = random.sample(y,7)
    #print(y)
    cbs = [
    		[ 1 , 2 , 4 , 6 , 9 ],
    		[ 1 , 2 , 4 , 6 , 10 ],
    		[ 1 , 2 , 4 , 6 , 11 ],
    		[ 1 , 2 , 4 , 7 , 9 ],
    		[ 1 , 2 , 4 , 7 , 10 ],
    		[ 1 , 2 , 4 , 7 , 11 ],
    		[ 1 , 2 , 4 , 8 , 9 ],
    		[ 1 , 2 , 4 , 8 , 10 ],
    		[ 1 , 2 , 4 , 8 , 11 ],
    		[ 1 , 2 , 5 , 6 , 9 ],
    		[ 1 , 2 , 5 , 6 , 10 ],
    		[ 1 , 2 , 5 , 6 , 11 ],
    		[ 1 , 2 , 5 , 7 , 9 ],
    		[ 1 , 2 , 5 , 7 , 10 ],
    		[ 1 , 2 , 5 , 7 , 11 ],
    		[ 1 , 2 , 5 , 8 , 9 ],
    		[ 1 , 2 , 5 , 8 , 10 ],
    		[ 1 , 2 , 5 , 8 , 11 ],
    		[ 1 , 3 , 4 , 6 , 9 ],
    		[ 1 , 3 , 4 , 6 , 10 ],
    		[ 1 , 3 , 4 , 6 , 11 ],
    		[ 1 , 3 , 4 , 7 , 9 ],
    		[ 1 , 3 , 4 , 7 , 10 ],
    		[ 1 , 3 , 4 , 7 , 11 ],
    		[ 1 , 3 , 4 , 8 , 9 ],
    		[ 1 , 3 , 4 , 8 , 10 ],
    		[ 1 , 3 , 4 , 8 , 11 ],
    		[ 1 , 3 , 5 , 6 , 9 ],
    		[ 1 , 3 , 5 , 6 , 10 ],
    		[ 1 , 3 , 5 , 6 , 11 ],
    		[ 1 , 3 , 5 , 7 , 9 ],
    		[ 1 , 3 , 5 , 7 , 10 ],
    		[ 1 , 3 , 5 , 7 , 11 ],
    		[ 1 , 3 , 5 , 8 , 9 ],
    		[ 1 , 3 , 5 , 8 , 10 ],
    		[ 1 , 3 , 5 , 8 , 11 ],
    		[ 2 , 3 , 4 , 6 , 9 ],
    		[ 2 , 3 , 4 , 6 , 10 ],
    		[ 2 , 3 , 4 , 6 , 11 ],
    		[ 2 , 3 , 4 , 7 , 9 ],
    		[ 2 , 3 , 4 , 7 , 10 ],
    		[ 2 , 3 , 4 , 7 , 11 ],
    		[ 2 , 3 , 4 , 8 , 9 ],
    		[ 2 , 3 , 4 , 8 , 10 ],
    		[ 2 , 3 , 4 , 8 , 11 ],
    		[ 2 , 3 , 5 , 6 , 9 ],
    		[ 2 , 3 , 5 , 6 , 10 ],
    		[ 2 , 3 , 5 , 6 , 11 ],
    		[ 2 , 3 , 5 , 7 , 9 ],
    		[ 2 , 3 , 5 , 7 , 10 ],
    		[ 2 , 3 , 5 , 7 , 11 ],
    		[ 2 , 3 , 5 , 8 , 9 ],
    		[ 2 , 3 , 5 , 8 , 10 ],
    		[ 2 , 3 , 5 , 8 , 11 ],
    	]
    l = [0,1,2]
    combs = []
    for c in y:
        print(c)
        for e1,i in enumerate(cbs):
            p = random.sample(l[:3],2)
            if (2 in p):
                c1 = []
                for j in i:
                    #print(c[j], end='-')
                    c1.append(c[j])
                combs.append(sorted(c1))
        #combs.append('======================')
    #combs = combs.sort()
    #print(combs)
    return render_template("eur.html", combs = combs, stars = s2, lcombs=len(combs))

# plan an help section
# with param /help to display all routes and possible parameters


def index():
    # storedb()
    return "Hello World!"


if __name__ == '__main__':
    app.run(port=8000, debug=True)
