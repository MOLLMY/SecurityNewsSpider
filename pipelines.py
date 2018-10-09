# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from SecurityNewsSpider import settings
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from SecurityNewsSpider.items import freebufItem
from SecurityNewsSpider.items import hackeyeItem
from SecurityNewsSpider.items import ctoItem
from SecurityNewsSpider.items import hackbaseItem
from SecurityNewsSpider.items import xinhuasheItem
from SecurityNewsSpider.items import secfreeItem
from SecurityNewsSpider.items import leiphoneItem
from SecurityNewsSpider.items import easyaqItem
from SecurityNewsSpider.items import cnbetaItem

#完成item到mongodb的存储
class SecuritynewsspiderPipeline(object):

    def __init__(self):
        # db_name = settings['MONGO_DATABASE']   #数据库名称
        # mongo_uri = settings['MONGO_URI']  #mongodb uri
        client = pymongo.MongoClient('localhost', 27017)   #连接mongodb
        db_securitynews = client.securitynews    #连接数据库securitynews
        self.coll_news = db_securitynews.news  #选择集合news

        # self.coll_freebuf = db_securitynews.freebuf     #freebuf
        # self.coll_hackeye = db_securitynews.hackeye     #黑客视界
        # self.coll_cto = db_securitynews.cto             #红黑联盟
        # self.coll_hackbase = db_securitynews.hackbase   #黑基网
        # self.coll_xinhuashe = db_securitynews.xinhuashe #新华社
        # self.coll_secfree = db_securitynews.secfree     #指尖安全
        # self.coll_easyaq = db_securitynews.easyaq       #E安全
        # self.coll_leiphone = db_securitynews.leiphone   #雷锋网
        # self.coll_cnbeta = db_securitynews.cnbeta       #cnbeta

    # def open_spider(self, spider):  #启动爬虫时
    #     # self.client = pymongo.MongoClient(self.mongo_uri)
    #     self.db = self.client[self.db_name] #get a database
    #     self.freebuf = self.db["freebuf"] #get a collection

    # def close_spider(self, spider): #关闭爬虫时
    #     self.client.close()

    def process_item(self, item, spider):
        #统一存于news集合下
        self.coll_news.insert(dict(item))

#各网站新闻暂时分开存储
        # if isinstance(item, freebufItem):       #freebuf的新闻存入freebuf集合
        #     self.coll_freebuf.insert(dict(item))
        #     # pass
        # elif isinstance(item, hackeyeItem):     #黑客视界的新闻存入hackeye集合
        #     self.coll_hackeye.insert(dict(item))
        # elif isinstance(item, ctoItem):         #红黑联盟的新闻存入cto集合
        #     self.coll_cto.insert(dict(item))
        # elif isinstance(item, hackbaseItem):    #黑基网的新闻存入hackbase集合
        #     self.coll_hackbase.insert(dict(item))
        # elif isinstance(item, xinhuasheItem):   #新华社的新闻存入xinhuashe集合
        #     self.coll_xinhuashe.insert(dict(item))
        # elif isinstance(item, secfreeItem):     #指尖安全的新闻存入secfree集合__secfree的正文比较规整，没有广告
        #     self.coll_secfree.insert(dict(item))
        # elif isinstance(item, leiphoneItem):    #雷锋网的新闻存入leiphone集合
        #     self.coll_leiphone.insert(dict(item))
        # elif isinstance(item, easyaqItem):      #E安全的新闻存入easyaq集合
        #     self.coll_easyaq.insert(dict(item))
        # elif isinstance(item, cnbetaItem):      #cnbeta的新闻存入cnbeta集合
        #     self.coll_cnbeta.insert(dict(item))
        # else:
        #     print(item)    
        return item
        
    