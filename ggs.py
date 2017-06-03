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

app = Flask(__name__)

RSS_FEEDS = {'bbc':'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn':'http://rss.cnn.com/rss/edition.rss',
             'fox':'http://feeds.foxnews.com/foxnews/latest',
             'iol':'http://iol.co.za/cmlink/1.640'}


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
def m4(c=[0,1,2,3,4,5,6,7,8,9],flg = 9):
    # set flg = 11 to apply -1 in 6,7,8 and -1 in 9,10,11
    # provide 11 members LT
    flg = request.args.get("flg")
    query = request.args.get("lt")
    #print(type(c))
    if query:
        c = query.split(',')
        c = [0]+c[:]
        c = [int(x) for x in c]
        #print(type(c))
    print('c=',c,type(flg))
    if flg == '11':
        p1 = c[6:9]
        p2 = c[9:12]
        px1 = random.sample(p1,1)
        px2 = random.sample(p2,1)
        #remove them from p1 and p2
        p1.remove(px1[0])
        p2.remove(px2[0])
        c = c[:6]+p1+p2
        print(c)
    # multis en 4 favos - c contient la liste type
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
    #return render_template("m4.html", combs = combs)


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
