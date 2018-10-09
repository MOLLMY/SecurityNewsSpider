# -*- coding: utf-8 -*-
import scrapy
from SecurityNewsSpider.items import secfreeItem
from scrapy.loader import ItemLoader    #用item loader更方便，利于后期维护和扩展新功能
from scrapy.selector import Selector
from scrapy.http.request import Request
import re
import datetime
from bs4 import BeautifulSoup
#指尖安全
class SecfreeSpider(scrapy.Spider):
    name = 'secfree'
    allowed_domains = ['secfree.com']
    start_urls = ['https://www.secfree.com/article_cat-12.html' #指尖安全 网络安全模块
            ]

    page = 1
    def parse(self, response):
        self.page+=1
        articles = response.xpath('//li[@class="animated fadeInUp"]')    #所有文章

        # from scrapy.shell import inspect_response
        # inspect_response(response,self)

        for article in articles:
            url = 'https://www.secfree.com'+article.xpath('.//a[@class="titlename"]/@href').extract_first()          #文章链接
            title = article.xpath('.//h3[@class="blogtitle"]/a/text()').extract_first()         #标题
            title_img = article.xpath('.//div[@class="bloginfo"]/span/a/img/@src').extract_first()    #缩略图链接  
            summary = article.xpath('.//div[@class="bloginfo"]/p/text()').extract_first()       #摘要
            author = article.xpath('.//div[@class="autor"]/span[1]/span/a/text()').extract_first()
            release_date = article.xpath('.//div[@class="autor"]/span[2]/label[1]/text()').extract_first()
            date = datetime.datetime.strptime(release_date,'%Y-%m-%d')
            #没有标签，全是网络安全
            secfree_item= secfreeItem(url = url, title = title, title_img = title_img, summary = summary, author = author, release_date = date)
            request = Request(url=url,callback=self.parse_body) #请求文章正文
            request.meta['item'] = secfree_item #将item暂存  meta属性具有传播性，无论发生重定向或重试都可以通过这个属性获取最原始的meta值
            yield request
        ##翻页 ____只有5页，57条新闻
        next_page = response.xpath('//a[@class="laypage-next"]/@href').extract_first()   #下一页url
        if next_page:
            yield Request(url='https://www.secfree.com/'+next_page, callback=self.parse)#回调方法用来指定由谁来解析此项Request请求的响应
        #或者爬取固定页数的
        # if self.page < 35:    #下一页  暂存34页,每页15条，共510条
        #     yield Request(url = 'https://www.2cto.com/news/safe/' + str(self.page)+'.html', callback = self.parse)

    def parse_body(self,response):      #secfree的正文比较规整，没有广告
        secfree_item = response.meta['item']
        contetn_html = response.xpath('//*[@class="detail-body photos"]').extract_first()
        secfree_item['content_html'] = contetn_html
        secfree_item['content_txt'] = BeautifulSoup(contetn_html).get_text()
        yield secfree_item 