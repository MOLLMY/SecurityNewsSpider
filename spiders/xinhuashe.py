# -*- coding: utf-8 -*-
import scrapy
from SecurityNewsSpider.items import xinhuasheItem
from scrapy.loader import ItemLoader    #用item loader更方便，利于后期维护和扩展新功能
from scrapy.selector import Selector
from scrapy.http.request import Request
import re
import datetime
from bs4 import BeautifulSoup

class XinhuasheSpider(scrapy.Spider):
    name = 'xinhuashe'
    allowed_domains = ['news.cn','xinhuanet.com']
    start_urls = ['http://www.news.cn/info/xxaq.htm']

    def parse(self, response):
        articles = response.xpath('//li[@class="clearfix"]')    #所有文章

        # from scrapy.shell import inspect_response
        # inspect_response(response,self)

        for article in articles:
            url = article.xpath('.//h3/a/@href').extract_first()          #文章链接
            title = article.xpath('.//h3/a/text()').extract_first()         #标题
            title_img = article.xpath('.//i/a/img/@data-original').extract_first()    #缩略图链接  只有十个，空的为 ""
            # title_img = img if img else None
            summary = article.xpath('.//p[@class="summary"]/text()').extract_first()       #摘要
            release_date = article.xpath('.//span[@class="time"]/text()').extract_first()    #发布日期
            date = datetime.datetime.strptime(release_date,'%Y-%m-%d')
            xinhuashe_item= xinhuasheItem(url = url, title_img = title_img, release_date = date, summary = summary, title=title)
            request = Request(url=url,callback=self.parse_body) #请求文章正文
            request.meta['item'] = xinhuashe_item #将item暂存  meta属性具有传播性，无论发生重定向或重试都可以通过这个属性获取最原始的meta值
            yield request
        ##翻页 ____无须翻页……一共就30条新闻，一次加载完，每次显示10条，剩下的隐藏，点三次加载更多就没了
        # selector = Selector(response)   #选择器
        # next_page = selector.xpath('').extract_first()   #下一页 
        # if next_page:
        #     yield Request(url=''+next_page, callback=self.parse)#回调方法用来指定由谁来解析此项Request请求的响应
        #或者爬取固定页数的
        # if self.page < 35:    #下一页  暂存34页,每页15条，共510条
        #     yield Request(url = 'https://www.2cto.com/news/safe/' + str(self.page)+'.html', callback = self.parse)

    def parse_body(self,response):
        xinhuashe_item = response.meta['item']
        # xinhuashe_item['title'] = ''.join(response.xpath('//*[@class="h-title"]/text()').re(r'\w'))#标题
        xinhuashe_item['author'] = ''.join(response.xpath('//em[@id="source"]/text()').re(r'\w'))      #来源
        content = response.xpath('//*[@id="p-detail"]/p').extract()
        if content:
            xinhuashe_item['content_html'] = ''.join(content)
            xinhuashe_item['content_txt'] = BeautifulSoup(''.join(content)).get_text()
        else:
            content_html = ''.join(response.xpath('//div[@class="article"]/p').extract())
            xinhuashe_item['content_html'] = content_html
            xinhuashe_item['content_txt'] =  BeautifulSoup(content_html).get_text()
        yield xinhuashe_item 