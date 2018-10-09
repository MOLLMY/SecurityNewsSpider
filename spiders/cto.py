# -*- coding: utf-8 -*-
import scrapy
from SecurityNewsSpider.items import ctoItem
from scrapy.loader import ItemLoader    #用item loader更方便，利于后期维护和扩展新功能
from scrapy.selector import Selector
from scrapy.http.request import Request
import re
import datetime
from bs4 import BeautifulSoup

#红黑联盟安全资讯，--更新不及时
class CtoSpider(scrapy.Spider):
    name = 'cto'
    allowed_domains = ['2cto.com']
    start_urls = ['https://www.2cto.com/news/safe/',        #第11页500错误
        'https://www.2cto.com/news/safe/12.html']
    page = 1
    def parse(self, response):
        CtoSpider.page+=1
        articles = response.xpath('//li[@class="clearfix"]')    #所有文章

        # from scrapy.shell import inspect_response
        # inspect_response(response,self)

        for article in articles:
            url = article.xpath('.//a[@class="title"]/@href').extract_first()          #文章链接
            title = article.xpath('.//a[@class="title"]/text()').extract_first()         #标题
            #缩略图链接，有的没有缩略图
            title_img = 'https://www.2cto.com'+article.xpath('.//a[@class="thumb"]/img/@src').extract_first() if article.xpath('.//a[@class="thumb"]/img/@src') else None    #缩略图链接，有的没有缩略图
            keywords = article.xpath('.//p[@class="tags"]/a/text()').extract()        #分类标签，关键词   
            summary = article.xpath('.//p[@class="intro"]/text()').extract_first()       #摘要
            cto_item= ctoItem(url = url, title = title, title_img = title_img, keywords = keywords, summary = summary)
            request = Request(url=url,callback=self.parse_body) #请求文章正文
            request.meta['item'] = cto_item #将item暂存  meta属性具有传播性，无论发生重定向或重试都可以通过这个属性获取最原始的meta值
            yield request
        ##翻页 
        #只能爬到150条数据 因为第11页500爬虫自动关闭了，已解决
        selector = Selector(response)   #选择器
        next_page = selector.xpath('//*[@id="pages"]/a[13]/@href').extract_first()   #下一页  /news/safe/2.html
        if next_page:
            yield Request(url='https://www.2cto.com'+next_page, callback=self.parse)#回调方法用来指定由谁来解析此项Request请求的响应
        #或者爬取固定页数的
        # if CtoSpider.page < 35:    #下一页  暂存34页,每页15条，共510条
        #     yield Request(url = 'https://www.2cto.com/news/safe/' + str(CtoSpider.page)+'.html', callback = self.parse)

    def parse_body(self,response):
        cto_item = response.meta['item']
        # author         #作者，无作者
        # release_date_text = response.xpath('.//dd[@class="frinfo"]/text()[1]').extract_first()   #发布时间 index out of range
        # release_date = re.match(re.compile(r'\d{4}-\d{2}-\d{2}'),release_date_text).group() #发布时间
        date = response.xpath('.//dd[@class="frinfo"]/text()[1]').re(r'\d{4}-\d{2}-\d{2}')[0]
        cto_item['release_date'] = datetime.datetime.strptime(date,'%Y-%m-%d')  #存date格式
        content_html = response.xpath('//*[@id="Article"]').extract_first()
        cto_item['content_html'] = content_html
        cto_item['content_txt'] = BeautifulSoup(content_html).get_text()
        
        # item['image_urls']=body.xpath(".//img/@src").extract()  #提取图片链接
        yield cto_item                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

#  content_html    #正文