# -*- coding: utf-8 -*-
import scrapy
import re
import json
import jsonpath
import urllib
import pymongo
from lxml import etree

cnbeta_item = dict()
temp = dict()
with open('D:\\projects\\cnbetapage2.json','rb') as f:
    data = json.load(f)
    articles = jsonpath.jsonpath(data,'$..list')[0]
    
    def parse_json(articles):
        for article in articles:
            title = article['title']
            summary = article['hometext']
            title_img = article['thumb']
            url = article['url_show']
            if not re.findall(re.compile(r'http'),url):
                url = 'https:' + url
            release_date = re.match(re.compile(r'\d{4}-\d{2}-\d{2}'), article['inputtime']).group()
            
            res = urllib.request.urlopen(url).read().decode('utf-8') #请求文章正文
            response = etree.HTML(res)
            author = response.xpath('//span[@class="source"]/a/span/text()|//span[@class="source"]/span/text()')[0] if response.xpath('//span[@class="source"]/a/span/text()|//span[@class="source"]/span/text()') else None  #稿源
            content_html = response.xpath('//div[@id="artibody"]')[0]
            cnbeta_item={'url': url, 'title':title, 'title_img':title_img, 'summary':summary, 'release_date':release_date,'author':author,'content_html':content_html}
            yield cnbeta_item #将item暂存  meta属性具有传播性，无论发生重定向或重试都可以通过这个属性获取最原始的meta值

    parse_json(articles)

    client = pymongo.MongoClient('localhost', 27017)   #连接mongodb
    db_securitynews = client.securitynews    #连接数据库securitynews
    # self.coll_news = db.news  #选择集合news
    coll_cnbeta = db_securitynews.cnbeta     #cnbeta
    coll_cnbeta.insert_one(cnbeta_item)