import pymysql

class PythonDB:
    def __init__(self):
        self.__DBname = "pythondb"
        self.__url = "rm-bp174t2q4533812a10o.mysql.rds.aliyuncs.com"
        self.__password = "@pythonDB"
        self.__username = "python"
        self.__port = '3306'
        self.__db = pymysql.connect(host=self.__url,user=self.__username,password=self.__password,database=self.__DBname)
        self.__cursor = self.__db.cursor()

    def delete(self):
        try:
            self.__cursor.execute('delete from type_movie')
            self.__db.commit()
        except:
            print('删除类型库发生错误')
            self.__db.rollback()
        try:
            self.__cursor.execute('delete from movie')
            self.__db.commit()
        except:
            print('删除数据库发生错误')
            self.__db.rollback()


    def close(self):

        self.__cursor.close()

    '''
    将数据插入到数据库中
    '''
    def insertDate(self,date):
        if isinstance(date,list):
            for i in date:
                id = self.__insertMovie(i['name'],i['picUrl'],i['score'])
                for j in i['tags']:
                    try:
                        self.__cursor.execute("INSERT INTO TYPE_MOVIE(type,movie_id)value('%s',%s)"%(j,id))
                        self.__db.commit()
                    except:
                        print('插入发生错误：'+"INSERT INTO TYPE_MOVIE(type,movie_id)value('%s',%s)"%(j,id))
                        self.__db.rollback()

    '''
    插入数据库
    '''
    def __insertMovie(self,name,picUrl,score):
        name=name.replace("'",'')
        insertSql="INSERT INTO MOVIE(name,score,Image)value('%s','%s','%s')"%(name,score,picUrl)

        try:
            self.__cursor.execute(insertSql)
            self.__db.commit()
        except:
            print('发生错误:'+insertSql)
            self.__db.rollback()
        self.__cursor.execute("select id from movie where name='%s'"%name)
        date = self.__cursor.fetchone()
        if isinstance(date,tuple):
            return date[0]