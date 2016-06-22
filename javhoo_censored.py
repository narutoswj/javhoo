#!/usr/bin/python
#-*-coding:utf-8-*-
__author__ = 'Joey'


import pymongo
import random
import pyquery
import socket
import time
import threading

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
            print(time.strftime( ISOTIMEFORMAT, time.localtime() ).__str__() + ' Start: ' + url)
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
                doc = pq(i).html()
                a = pq(i)('a:first')

                if collection.find({'URL':a.attr('href')}).count() == 0:
                    detail_page = pq(url = a.attr('href'))
                    #print(detail_page)
                    Big_Image = detail_page('.wf-container')('a').attr('href')
                    Project_Info = detail_page('.project_info').html()
                    Magnet_Table = detail_page('#magnet-table').html()
                    Sample_Images = detail_page('#sample-box').html()
                    Series = a.attr('title').split(' ')[0]
                    print(url + '   ' + Series)
                    collection.insert_one({"Series":Series,
                                           "URL":a.attr('href').encode('utf-8'),
                                           "Title":a.attr('title').encode('utf-8'),
                                           "Big_Image": Big_Image,
                                           'Project_Info': Project_Info,
                                           'Magnet_Table': Magnet_Table,
                                           "Sample_Images": Sample_Images,
                                           "CreateTime":time.strftime( ISOTIMEFORMAT, time.localtime() ),
                                           #"Detail_Page": detail_page.html()
                                           })
                #else:
                #    return False
            success = True
            print(time.strftime( ISOTIMEFORMAT, time.localtime() ).__str__() + ' End: ' + url)
            client.close()
        except Exception ,e:
            print(url + '   ' + Series + "Exception: ",e)
            time.sleep(sleep_download_time)
    #return True


def main(num):
    # count = 3100
    count = num
    goon = True
    # while((count <= 3097) & (goon)):
    while ((count >= 5)):
        threads = []
        t1 = threading.Thread(target=SaveToMongo, args=('https://www.javhoo.com/en/censored/page/', count,))
        threads.append(t1)
        count = count - 1
        t2 = threading.Thread(target=SaveToMongo, args=('https://www.javhoo.com/en/censored/page/', count,))
        threads.append(t2)
        count = count - 1
        t3 = threading.Thread(target=SaveToMongo, args=('https://www.javhoo.com/en/censored/page/', count,))
        threads.append(t3)
        count = count - 1
        t4 = threading.Thread(target=SaveToMongo, args=('https://www.javhoo.com/en/censored/page/', count,))
        threads.append(t4)
        count = count - 1
        t5 = threading.Thread(target=SaveToMongo, args=('https://www.javhoo.com/en/censored/page/', count,))
        threads.append(t5)
        count = count - 1

        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()
        print ('Next')


main(2695)


