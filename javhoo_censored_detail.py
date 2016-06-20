#!/usr/bin/python
#-*-coding:utf-8-
__author__ = 'Joey'


import pymongo
import random
import pyquery
import socket
import time
import threading

from pymongo import MongoClient
from pyquery import PyQuery as pq

timeout = 200
sleep_download_time = 0
ISOTIMEFORMAT='%Y-%m-%d %X'
socket.setdefaulttimeout(timeout)


def Get_detail_url(skip):
    client = MongoClient()
    # connect se
    client = MongoClient("127.0.0.1", 27017)
    # define db
    db = client.javhoo
    # define collection
    collection = db.censored_list
    for item in collection.find({"detail_url": None}).limit(20).skip(skip):
        url = item["page"]
        # time.sleep(sleep_download_time)
        success = False
        while not success:
            try:#
                from pyquery import PyQuery as pq
                print(url)
                doc = pq(url=url)
                # print(doc)
                print("Get Main")
                data = doc('#main').html()
                # print(data)
                print("Start saing")
                collection.update({"_id": item["_id"]}, {"$set": {"detail_url": data}})
                # initial client
                success = True
                print("Saving sucessfully")
            except Exception, e:
                print("Exception: ", e)
                collection.update({"_id": item["_id"]}, {"$set": {"detail_url": "Error"}})
                time.sleep(sleep_download_time)


# Connect MongoDB Server
client = pymongo.MongoClient(host="127.0.0.1", port=27017)
# Connect Databas
db = client.javhoo
# Use collection
collection = db['censored_list']
count = collection.find({"detail_url":None}).count()
while count > 0:
    threads = []
    t1 = threading.Thread(target=Get_detail_url,args=(0,))
    threads.append(t1)
    #t2 = threading.Thread(target=Get_detail_url,args=(20,))
    #threads.append(t2)
    #t3 = threading.Thread(target=Get_detail_url,args=(40,))
    #threads.append(t3)
    #t4 = threading.Thread(target=Get_detail_url,args=(60,))#
    #threads.append(t4)
    #t5 = threading.Thread(target=Get_detail_url,args=(80,))
    #threads.append(t5)
    #t6 = threading.Thread(target=Get_detail_url,args=(100,))
    #threads.append(t6)
    #t7 = threading.Thread(target=Get_detail_url,args=(120,))
    #threads.append(t7)
    #t8 = threading.Thread(target=Get_detail_url,args=(140,))
    #threads.append(t8)

    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
    count = collection.find({"detail_url":None}).count()