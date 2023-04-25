import connectDB
import connectRedis




if __name__ =='__main__':
     db=connectDB.PythonDB()
     redispy=connectRedis.redisDB()
     mak=1
     while mak!=0:
          mak=int(input('请输入操作数：'))
          if mak==1:
               print('正在初始化数据库')
               db.delete()
               print('初始化成功')
          if mak==2:
               print('正在设置任务')
               for i in range(1,11):
                    redispy.putUrl('https://ssr1.scrape.center/page/'+str(i))
                    # print('')
               print('设置成功')


