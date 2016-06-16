#!/usr/bin/python
#-*-coding:utf-8-*-
__author__ = 'Joey'


import pymongo
import random
import pyquery
import socket
import time

timeout = 200
sleep_download_time = 4
ISOTIMEFORMAT='%Y-%m-%d %X'
socket.setdefaulttimeout(timeout)

def SaveToMongo(url,page):
    success = False
    url = url + page.__str__() + "/"
    while not success:
        try:
            from pyquery import PyQuery as pq
            print(url)
            doc = pq(url=url)
            # print(doc)
            data = doc('.wf-cell')
            #print(data)
            # initial client
            from pymongo import MongoClient
            client = MongoClient()
            # connect server
            client = MongoClient("127.0.0.1", 27017)
            # define db
            db = client.javhoo
            # define collection
            collection = db.censored_list
            # write into collection
            for i in data:
             collection.insert_one({'url': url ,'pagenumber': page, 'doc': pq(i).html(),'createtime':time.strftime( ISOTIMEFORMAT, time.localtime() )})
            success = True
        except Exception ,e:
            print("Exception: ",e)
            time.sleep(sleep_download_time)
count = 1001
while(count<=3072):
 print(time.strftime( ISOTIMEFORMAT, time.localtime() ).__str__() +  " starting page: " + count.__str__() )
 SaveToMongo('https://www.javhoo.com/en/censored/page/', count)
 print(time.strftime( ISOTIMEFORMAT, time.localtime() ).__str__() +  "done")
 print(time.strftime( ISOTIMEFORMAT, time.localtime() ).__str__() +  "starting sleep: " )
 time.sleep(sleep_download_time)
 print(time.strftime( ISOTIMEFORMAT, time.localtime() ).__str__() +  " finished page: " + count.__str__() )
 count = count + 1


