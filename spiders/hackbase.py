# -*- coding: utf-8 -*-
import scrapy
from SecurityNewsSpider.items import hackbaseItem
from scrapy.loader import ItemLoader    #用item loader更方便，利于后期维护和扩展新功能
from scrapy.selector import Selector
from scrapy.http.request import Request
import re
import datetime
from bs4 import BeautifulSoup

class HackbaseSpider(scrapy.Spider):
    name = 'hackbase'
    allowed_domains = ['hackbase.com']
    start_urls = ['http://www.hackbase.com/list-25-1.html',     #黑基网 安全报
                # 'http://www.hackbase.com/list-70-1.html'  #存疑，主要介绍安全工具
            ]
    url_base = 'http://www.hackbase.com/'
    page = 1
    def parse(self, response):
        self.page+=1
        articles = response.xpath('//li[@class="sxp_picnews cl"]')    #文章列表

        # from scrapy.shell import inspect_response
        # inspect_response(response,self)

        for article in articles:
            url = article.xpath('.//h3/a/@href').extract_first()          #文章链接
            title = article.xpath('.//h3/a/text()').extract_first()       #标题
            title_img = self.url_base + article.xpath('.//img/@src').extract_first()    #缩略图链接  
            summary = article.xpath('.//*[@class="sxp_picnewsarea1"]/div/em/text()').extract_first()       #摘要
            release_date = article.xpath('.//*[@class="sxp_picnewsarea2"]/span/text()').re(r'\d{4}-\d{1,2}-\d{1,2}')[0]
            date = datetime.datetime.strptime(release_date,'%Y-%m-%d')
            hackbase_item= hackbaseItem(url = url, title = title, title_img = title_img, release_date = date, summary = summary)
            request = Request(url=url,callback=self.parse_body) #请求文章正文
            request.meta['item'] = hackbase_item #将item暂存  meta属性具有传播性，无论发生重定向或重试都可以通过这个属性获取最原始的meta值
            yield request
        ##翻页 
        selector = Selector(response)   #选择器
        next_page = selector.xpath('//a[@class="nxt"]/@href').extract_first()   #下一页的url
        if next_page:
            yield Request(url = next_page, callback = self.parse)#回调方法用来指定由谁来解析此项Request请求的响应
        #或者爬取固定页数的
        # if self.page < 35:    #下一页  暂存34页,每页15条，共510条
        #     yield Request(url = 'http://www.hackbase.com/list-25-' + str(self.page)+'.html', callback = self.parse)

    def parse_body(self,response):
        hackbase_item = response.meta['item']
        hackbase_item['author'] = response.xpath('//*[@class="xg1"]/a[1]/text()').extract_first()         #作者
        content_html = response.xpath('//*[@id="article_content"]').extract_first()
        hackbase_item['content_html'] = content_html
        hackbase_item['content_txt'] = BeautifulSoup(content_html).get_text()
        yield hackbase_item 
