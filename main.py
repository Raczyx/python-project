# -*- coding: utf-8 -*-
import time

import requests
import sys
from bs4 import BeautifulSoup as bs
from threading import Thread
from fake_useragent import UserAgent
from queue import Queue

import connectDB
import connectRedis

requests.packages.urllib3.disable_warnings()        #关闭安全警告

# #可用ip池，由于免费ip过于难找先不使用
# proxies={

# }
header = {
    'User-Agent':   UserAgent().random,
    'sec-ch-ua':'"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
    'Host':'ssr1.scrape.center',
    'Accept-Encoding':'gzip, deflate, br'
}

def getName(film):
    FnameBox = film.find_all(attrs={'class':'name'})
    name = FnameBox[0].h2.text
    return name

def getPic(film):
    img = film.find('img')
    picUrl = img['src']
    return picUrl

def getTag(film):
    categories = film.find_all(attrs={'class':'category'})
    tags = []
    for category in categories:
        tags.append(category.span.text)
    return tags

def getScore(film):
    FscoreBox = film.find_all(attrs={'class':'score'})
    score = FscoreBox[0].text.replace('\n','')
    return score.replace(' ','')



#获取到的全部数据
def spider(url,q):
    datas = []
    # for i in range(1,10):
    #     url = 'https://ssr1.scrape.center/page/'+str(i)
    r = requests.get(url,headers=header,verify=False)          #由于该网页没有安装证书，verify设置为False

    if r.status_code==200:
        #获取
        soup = bs(r.text,'lxml')
        film_list=soup.find_all(attrs={'class':'el-card__body'})
        for i in range(0,10):
            obj = {}
            film = film_list[i]
            name = getName(film)
            picUrl = getPic(film)
            score = getScore(film)
            tags = getTag(film)
            obj["name"]=name
            obj["tags"]=tags
            obj["picUrl"]=picUrl
            obj["score"]=score
            datas.append(obj)
    q.put(datas)

def openThreads(urls):
    q = Queue()
    threads=[]
    for url in urls:
        t=Thread(target=spider,args=(url,q))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    results = []
    for _ in range(len(urls)):
        results.append(q.get())
    return results


if __name__ == "__main__":
    # urls=["https://ssr1.scrape.center/page/1","https://ssr1.scrape.center/page/2"]

    urls=[]
    redispy = connectRedis.redisDB()
    db = connectDB.PythonDB()
    # redispy.putUrl('https://ssr1.scrape.center/page/1')
    # redispy.putUrl('https://ssr1.scrape.center/page/2')
    try:
        while True:
            if redispy.isListNULL():
                time.sleep(10)
                print('无任务')
                continue
            urls.append(redispy.getUrl())
            if not redispy.isListNULL():
                urls.append(redispy.getUrl())
            results = openThreads(urls)
            res = []
            for result in results:
                for obj in result:
                    res.append(obj)

            db.insertDate(res)

    except:
        print('退出中')
        redispy.close()
        db.close()
    print('已退出')



