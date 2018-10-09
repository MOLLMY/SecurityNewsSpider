# -*- coding: utf-8 -*-
import scrapy
from SecurityNewsSpider.items import hackeyeItem
from scrapy.loader import ItemLoader    #用item loader更方便，利于后期维护和扩展新功能
from scrapy.selector import Selector
from scrapy.http.request import Request
import re
import datetime
from bs4 import BeautifulSoup
# from selenium import webdriverwebdriver

'''
黑客视界https://www.hackeye.net/
'''
class HackeyeSpider(scrapy.Spider):
    name = 'hackeye'
    allowed_domains = ['hackeye.net']
    start_urls = ['https://www.hackeye.net/']

    url_base = 'https://www.hackeye.net/page/'
    page = 1
    def parse(self, response):

        HackeyeSpider.page += 1     #页码加1，https://www.hackeye.net/page/2

        articles = response.xpath('//article[@class="excerpt ias_excerpt"]')    #所有文章

        # from scrapy.shell import inspect_response
        # inspect_response(response,self)

        for article in articles:        #解析文章列表中的每一个文章
            url = article.xpath('.//*[@class="title info_flow_news_title"]/@href').extract_first() #文章正文链接
            title = article.xpath('.//*[@class="title info_flow_news_title"]/text()').extract_first()    #文章标题
            # release_time = article.xpath('.//*[@class="timeago"]/@datetime').extract_first()  #发布日期
            # release_date = re.match(re.compile(r'\d{4}-\d{2}-\d{2}'),release_time).group()
            release_date = article.xpath('.//*[@class="timeago"]/@datetime').re(r'\d{4}-\d{2}-\d{2}')[0]
            date = datetime.datetime.strptime(release_date,'%Y-%m-%d')
            tag = article.xpath('.//*[@class="info_cat"]/text()').extract()  #分类标签,只有一个
            author = article.xpath('.//*[@class="name"]/text()').extract_first()    #作者
            title_img = article.xpath('.//a[1]/@data-lazyload').extract_first() 
            # print('-'*40+title_img)
            summary = article.xpath('.//div[@class="brief"]/text()').extract_first().replace('...','').replace('\r\n', '')  #摘要
            # if summary:
            #     summary = summary.replace('...','').replace('\r\n', '')
            hackeye_item = hackeyeItem(url=url,title=title,release_date=date,tag=tag,author=author,title_img=title_img,summary=summary) #首页列表爬到的数据存item

            request = Request(url=url,callback=self.parse_body) #请求文章正文
            request.meta['item'] = hackeye_item #将item暂存  meta属性具有传播性，无论发生重定向或重试都可以通过这个属性获取最原始的meta值
            yield request

        if HackeyeSpider.page < 51:    #下一页  暂存50页吧，每页10条，共500条
            yield Request(url = HackeyeSpider.url_base + str(HackeyeSpider.page), callback = self.parse)#回调方法用来指定由谁来解析此项Request请求的响应

    def parse_body(self,response):      #解析具体的文章内容
        hackeye_item=response.meta['item']
        content_html = response.xpath('.//section[@class="article"]').extract_first()   #'<section class="article">\r\n...         
        hackeye_item['content_html'] = content_html
        hackeye_item['content_txt'] = BeautifulSoup(content_html).get_text() 
        yield hackeye_item
