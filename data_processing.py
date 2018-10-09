import pymongo
import datetime
client = pymongo.MongoClient('localhost', 27017)   #连接mongodb
db_securitynews = client.securitynews    #连接数据库securitynews
coll_test = db_securitynews.test

strdate = "2018-07-28"
date=datetime.datetime.strptime(strdate,'%Y-%m-%d')
# date = datetime.date.fromisoformat("2018-09-27")
print(date)
d = {'title':'test2','date':date}
coll_test.insert(d)
