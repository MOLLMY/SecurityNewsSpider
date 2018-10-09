# -*- coding: utf-8 -*-
import scrapy
from SecurityNewsSpider.items import cnbetaItem
from scrapy.loader import ItemLoader    #用item loader更方便，利于后期维护和扩展新功能
from scrapy.selector import Selector
from scrapy.http.request import Request
import re
from bs4 import BeautifulSoup
import time
import urllib
import json
import jsonpath
import datetime

class CnbetaSpider(scrapy.Spider):
    name = 'cnbeta'
    allowed_domains = ['cnbeta.com']
    start_urls = ['https://www.cnbeta.com/topics/157.htm'   #安全
                ]
#下滑自动加载更多，每次加载35条
#未解决加载更多的问题

    page = 1
    url_base='https://www.cnbeta.com/home/more?&type=topic|157&page='
    num = round(time.time()*1000)

    def parse(self, response):
        self.page += 1
        self.num += 2
        articles = response.xpath('//*[@class="item"]')    #所有文章
        # csrf_token = response.xpath('//meta[@name="csrf-token"]/@content').extract_first()
        
        #检查response
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)

        for article in articles:
            url = article.xpath('.//dl/dt/a/@href').extract_first()          #文章链接
            if not re.findall(re.compile(r'http'),url):
                url = 'https:' + url
            title = article.xpath('.//dl/dt/a/text()').extract_first()         #标题
            title_img = article.xpath('.//dl/a/img/@src').extract_first()   #缩略图链接  
            summ = article.xpath('.//dl/dd/p').extract_first()       #摘要，摘要中有来源链接，需要去掉所有的尖括号
            summary = BeautifulSoup(summ.replace('\r\n','')).get_text()
            #没有作者，有稿源
            date = article.xpath('.//ul[@class="status"]/li[1]').re(r'\d{4}-\d{2}-\d{2}')[0]
            release_date=datetime.datetime.strptime(date,'%Y-%m-%d')#存为date格式
            #没有标签，全是科技
            cnbeta_item= cnbetaItem(url = url, title = title, title_img = title_img, summary = summary, release_date = release_date)
            request = Request(url=url,callback=self.parse_body) #请求文章正文
            request.meta['item'] = cnbeta_item #将item暂存  meta属性具有传播性，无论发生重定向或重试都可以通过这个属性获取最原始的meta值
            yield request

        ##翻页 下拉自动加载 在xhr中
        #page=2&_csrf=TxKIAi0gY9Y0ZlTpEFG9HYgab815th2-V4KSCopxwDEXdcd3VFFVh3EJM5ojP94tu3xCvk6Bd_U7zqZQ7j30Zw%3D%3D&_=1537145031999
        #https://www.cnbeta.com/home/more?&type=topic|157&page=4&_csrf=TxKIAi0gY9Y0ZlTpEFG9HYgab815th2-V4KSCopxwDEXdcd3VFFVh3EJM5ojP94tu3xCvk6Bd_U7zqZQ7j30Zw%3D%3D&_=1537145032003
        ###自己构造下一页地址
        # if self.page < 5:    #下一页  每页35条
        #     print(self.url_base + str(self.page)+'&_csrf='+csrf_token+'&_='+str(self.num))
        #     yield Request(url = self.url_base + str(self.page)+'&_csrf='+csrf_token+'&_='+str(self.num), callback = self.parse_json)

    def parse_body(self,response):      #cnbeta的正文比较规整，没有广告
        cnbeta_item = response.meta['item']
        #null的可能是<span class="source">稿源：<a href="http://www.cnbeta.com/" target="_blank">cnBeta.COM</a></span>
        # 也可能是<span class="source">稿源：央广网</span>
        cnbeta_item['author'] = response.xpath('//span[@class="source"]/a/span/text()|//span[@class="source"]/span/text()').extract_first()  #稿源
        content_html = response.xpath('//div[@id="artibody"]').extract_first()
        cnbeta_item['content_html'] = content_html
        cnbeta_item['content_txt'] = BeautifulSoup(content_html).get_text()
        yield cnbeta_item 

    
        
