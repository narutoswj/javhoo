#!/usr/bin/python
#-*-coding:utf-8-*-
__author__ = 'Joey'


import pymongo
import random
import pyquery
import socket
import time
import urllib
import threading

from pymongo import MongoClient
from pyquery import PyQuery as pq


def Download_20_Cover(skip):
    client = MongoClient()
    # connect se
    client = MongoClient("127.0.0.1", 27017)
    # define db
    db = client.javhoo
    # define collection
    collection = db.censored_list
    try:
        for item in collection.find({"cover_downloaded": None}).limit(20).skip(skip):
            image = item["image"]
            series = item["series"]
            print(image)
            # print(series)
            path = 'D:/Cover/'
            path = path + series.__str__() + ".jpg"
            print(path)
            data = urllib.urlopen(image).read()
            f = file(path, "wb")
            f.write(data)
            f.flush()
            f.close()
            collection.update({"_id": item["_id"]}, {"$set": {"cover_downloaded": 1}})
    except Exception, e:
        print("Exception: ", e)

# Connect MongoDB Server
client = pymongo.MongoClient(host="127.0.0.1", port=27017)
# Connect Database
db = client.javhoo
# Use collection
collection = db['censored_list']
count = collection.find({"cover_downloaded":None}).count()
while count > 0:
    threads = []
    t1 = threading.Thread(target=Download_20_Cover,args=(0,))
    threads.append(t1)
    t2 = threading.Thread(target=Download_20_Cover,args=(20,))
    threads.append(t2)
    t3 = threading.Thread(target=Download_20_Cover,args=(40,))
    threads.append(t3)
    t4 = threading.Thread(target=Download_20_Cover,args=(60,))
    threads.append(t4)
    t5 = threading.Thread(target=Download_20_Cover,args=(80,))
    threads.append(t5)

    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    count = collection.find({"cover_downloaded":None}).count()