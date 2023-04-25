import json

import redis

class redisDB:
    def __init__(self):
        self.__pool = redis.ConnectionPool(host='r-wz9f8p45uelr7mb2rupd.redis.rds.aliyuncs.com', port=6379, password='@PYTHONpasswd', decode_responses=True)

        self.__conn = redis.Redis(connection_pool=self.__pool)

    '''
    判断任务是否为空
    '''
    def isListNULL(self):
        return self.__conn.llen('pythonlist')==0


    '''
    可以选择将字典或字典数组传入redis中
    '''
    def pushDate(self,date):
        if isinstance(date,list):
            for i in date:
                self.__conn.sadd('date',str(json.dumps(i)))
        else:
            self.__conn.sadd('date',str(json.dumps(date)))

    '''
    按值或随机取出存入的值，返回值为json字符串
    '''
    def popSet(self,value='anyone'):
        if value=='anyone':
            return self.__conn.spop('date')
        else:
            return self.__conn.spop('date',value)

    '''
    获取任务url
    '''
    def getUrl(self):
        return self.__conn.lpop("pythonlist")


    def putUrl(self,url):
        self.__conn.rpush("pythonlist",url)

    def close(self):
        self.__conn.close()
