# -*- coding: utf-8 -*-
import scrapy
from SecurityNewsSpider.items import leiphoneItem
from scrapy.loader import ItemLoader    #用item loader更方便，利于后期维护和扩展新功能
from scrapy.selector import Selector
from scrapy.http.request import Request
import re
import datetime
from bs4 import BeautifulSoup

class LeiphoneSpider(scrapy.Spider):
    name = 'leiphone'
    allowed_domains = ['leiphone.com']
    start_urls = ['https://www.leiphone.com/category/letshome'  #雷锋网 网络安全板块
                    ]
    
    page = 1
    def parse(self, response):
        self.page+=1
        articles = response.xpath('//*[@class="list"]/ul/li/div[@class="box"]')    #所有文章

        # from scrapy.shell import inspect_response
        # inspect_response(response,self)

        for article in articles:
            url = article.xpath('.//div[@class="word"]/h3/a/@href').extract_first()
            title = ''.join(article.xpath('.//div[@class="word"]/h3/a/text()').re(r'\w'))
            summary = ''.join(article.xpath('.//div[@class="des"]/text()').re(r'\w'))
            author = ''.join(article.xpath('.//div[@class="msg clr"]/a/text()[2]').re(r'\w'))
            tag = article.xpath('.//div[@class="tags"]/a/text()').extract()
            title_img = article.xpath('.//div[@class="img"]/a[2]/img/@src').extract_first()
            
            leiphone_item= leiphoneItem(url = url, title = title, author = author, title_img = title_img, tag = tag, summary = summary)
            request = Request(url=url,callback=self.parse_body) #请求文章正文
            request.meta['item'] = leiphone_item #将item暂存  meta属性具有传播性，无论发生重定向或重试都可以通过这个属性获取最原始的meta值
            yield request
            
        ##翻页 
        next_page = response.xpath('.//a[@class="next"]/@href').extract_first()   #下一页 
        if next_page:
            yield Request(url = next_page, callback = self.parse)#回调方法用来指定由谁来解析此项Request请求的响应
        #或者爬取固定页数的
        # if self.page < 35:    #下一页  暂存34页,每页15条，共510条
        #     yield Request(url = 'https://www.leiphone.com/category/letshome/page/' + str(self.page), callback = self.parse)

    def parse_body(self,response):
        leiphone_item = response.meta['item']
        date = response.xpath('.//td[@class="time"]/text()').re(r'\d{4}-\d{2}-\d{2}')[0]
        leiphone_item['release_date'] = datetime.datetime.strptime(date,'%Y-%m-%d')
        content_html = response.xpath('.//div[@class="lph-article-comView"]').extract_first()        #最后一个a标签是广告
        leiphone_item['content_html'] = content_html
        leiphone_item['content_txt'] = BeautifulSoup(content_html).get_text()
        yield leiphone_item 