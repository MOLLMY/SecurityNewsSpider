# -*- coding: utf-8 -*-
import scrapy
from SecurityNewsSpider.items import freebufItem
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem
from scrapy.loader import ItemLoader    #用item loader更方便，利于后期维护和扩展新功能
import datetime
from bs4 import BeautifulSoup

#网站有问题，打开特别慢
class FreebufSpider(scrapy.Spider):
    name = 'freebuf'    #爬虫名字，唯一，用于启动爬虫
    allowed_domains = ['freebuf.com']   #用于限定爬虫爬去的url域名
    start_urls = ['http://www.freebuf.com/articles']    #用于创建开始的请求

    url_base = 'http://www.freebuf.com/articles/page/'
    page = 1

    def parse(self, response):      #网页解析
        FreebufSpider.page += 1
        articles = response.xpath("//div[@class='news_inner news-list']") #所有文章
        #查看response
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)

        for article in articles:    #从每篇文章中抽取数据
            url = article.xpath(".//*[@class='article-title']/@href").extract_first()  #文章正文链接 
            title = article.xpath(".//*[@class='article-title']/text()").extract_first()    #文章标题
            date = article.xpath(".//*[@class='time']/text()").extract_first()  #发布日期
            release_date = datetime.datetime.strptime(date,'%Y-%m-%d')  #存为时间格式
            tag = article.xpath(".//*[@class='tags']/a/text()").extract()  #分类标签,不止一个
            author = article.xpath(".//*[@class='name']/a/text()").extract_first()   #作者
            title_img = article.xpath(".//*[@class='news-img']/a/img/@src").extract_first()  #标题缩略图链接
            summary = article.xpath(".//dd[@class='text']/text()").extract_first()  #摘要
            freebuf_item = freebufItem(url=url,title=title,release_date=release_date,tag=tag,author=author,title_img=title_img,summary=summary) #首页列表爬到的数据存item

            request = Request(url=url,callback=self.parse_body) #请求文章正文
            request.meta['item'] = freebuf_item #将item暂存  meta属性具有传播性，无论发生重定向或重试都可以通过这个属性获取最原始的meta值
            yield request

        if FreebufSpider.page < 21:     #爬20页，每页16条 post方法，默认get
            yield Request(url = self.url_base + str(self.page), method = 'POST', callback=self.parse)#回调方法用来指定由谁来解析此项Request请求的响应
        
        # #测试师姐的翻页
        # urls = response.xpath('/html/body/div[2]/div[1]/div[1]/div/div[3]/a/@href').extract()    #查看更多 urls=[url]
        # print(urls)
        # print('='*40)
        # for url in urls:#每次只取到一个url，但可能为空,这样爬完可以自动停止，到page4
        #     print('#'*20+url)
        #     # url = "https://www.easyaq.com/news/" + url
        #     yield Request(url, callback=self.parse)


    def parse_body(self,response):
        freebuf_item = response.meta['item']
        content_html = response.xpath('//*[@id="contenttxt"]').extract() #为空
        freebuf_item['content_html'] = content_html
        freebuf_item['content_txt'] = BeautifulSoup(content_html).get_text()
        yield freebuf_item