# -*- coding: utf-8 -*-
import scrapy
from SecurityNewsSpider.items import easyaqItem
from scrapy.loader import ItemLoader    #用item loader更方便，利于后期维护和扩展新功能
from scrapy.selector import Selector
from scrapy.http.request import Request
import re
import datetime
from bs4 import BeautifulSoup
#E安全
class EasyaqSpider(scrapy.Spider):
    name = 'easyaq'
    allowed_domains = ['easyaq.com']
    start_urls = ['http://easyaq.com/']

    page = 1
    def parse(self, response):
        self.page+=1
        articles = response.xpath('//div[@class="listnews bt"]')    #所有文章

        # from scrapy.shell import inspect_response
        # inspect_response(response,self)

        for article in articles:
            url = article.xpath('.//div[@class="listdeteal"]/h3/a/@href').extract_first()          #文章链接
            title = article.xpath('.//div[@class="listdeteal"]/h3/a/text()').extract_first()         #标题
            title_img = article.xpath('.//div[@class="listimg"]/a/img/@src').extract_first()    #缩略图链接  
            summary = article.xpath('.//div[@class="listdeteal"]/p/text()').extract_first()       #摘要
            tag = article.xpath('.//ul[@class="listword"]/li/a/text()').extract()         #标签
            date = article.xpath('.//div[@class="source"]/span/text()').re(r'\d{4}-\d{2}-\d{2}')[0]    #发布日期
            release_date = datetime.datetime.strptime(date,'%Y-%m-%d')
            easyaq_item= easyaqItem(url = url, title = title, title_img = title_img, tag = tag, release_date = release_date, summary = summary)
            request = Request(url=url,callback=self.parse_body) #请求文章正文
            request.meta['item'] = easyaq_item #将item暂存  meta属性具有传播性，无论发生重定向或重试都可以通过这个属性获取最原始的meta值
            yield request
        ##翻页  翻页部分是js加载的，所以只能自己构造了
        # next_page = response.xpath('').extract_first()   #下一页 
        # if next_page:
        #     yield Request(url=''+next_page, callback=self.parse)#回调方法用来指定由谁来解析此项Request请求的响应
        ## 或者爬取固定页数的
        if self.page < 21:    #下一页  每页20条
            yield Request(url = 'https://www.easyaq.com/' + str(self.page)+'.shtml', callback = self.parse)

    def parse_body(self,response):
        easyaq_item = response.meta['item']
        content_html = ''.join(response.xpath('//div[@class="content-text"]/p').extract())
        easyaq_item['content_html'] = content_html
        easyaq_item['content_txt'] = BeautifulSoup(content_html).get_text()
        yield easyaq_item 
