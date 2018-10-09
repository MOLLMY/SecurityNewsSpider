# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SecuritynewsspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field(）
    pass
class freebufItem(scrapy.Item):
    """
    freebuf漏洞爬虫，Item的定义
    """
    url = scrapy.Field()            #文章链接
    title = scrapy.Field()          #标题
    title_img = scrapy.Field()      #缩略图链接
    release_date = scrapy.Field()   #发布时间
    tag = scrapy.Field()            #分类标签
    author = scrapy.Field()         #作者
    summary = scrapy.Field()        #摘要
    content_html = scrapy.Field()   #正文
    content_txt = scrapy.Field()    #正文文字
    image_urls = scrapy.Field()     #正文图片链接

class hackeyeItem(scrapy.Item):
    """
    黑客视界
    https://www.hackeye.net/
    """
    url = scrapy.Field()            #文章链接
    title = scrapy.Field()          #标题
    title_img = scrapy.Field()      #缩略图链接
    release_date = scrapy.Field()   #发布时间
    tag = scrapy.Field()            #分类标签
    author = scrapy.Field()         #作者
    summary = scrapy.Field()        #摘要
    content_html = scrapy.Field()   #正文
    content_txt = scrapy.Field()    #正文文字
    image_urls = scrapy.Field()     #正文图片链接

class ctoItem(scrapy.Item):
    '''
    红黑联盟 安全资讯
    https://www.2cto.com/news/safe/
    不常更新
    '''
    url = scrapy.Field()            #文章链接
    title = scrapy.Field()          #标题
    title_img = scrapy.Field()      #缩略图链接，有的没有缩略图
    release_date = scrapy.Field()   #发布时间
    keywords = scrapy.Field()       #分类标签，关键词
    author = scrapy.Field()         #作者
    summary = scrapy.Field()        #摘要
    content_html = scrapy.Field()   #正文
    content_txt = scrapy.Field()    #正文文字
    image_urls = scrapy.Field()     #正文图片链接

class hackbaseItem(scrapy.Item):
    '''
    黑基网 安全报
    http://www.hackbase.com/list-12-1.html
    安全攻防
    http://www.hackbase.com/list-70-1.html
    '''
    url = scrapy.Field()            #文章链接
    title = scrapy.Field()          #标题
    title_img = scrapy.Field()      #缩略图链接，有的没有缩略图
    release_date = scrapy.Field()   #发布时间
    tag = scrapy.Field()            ##没有标签
    author = scrapy.Field()         #作者
    summary = scrapy.Field()        #摘要
    content_html = scrapy.Field()   #正文
    content_txt = scrapy.Field()    #正文文字
    image_urls = scrapy.Field()     #正文图片链接

class xinhuasheItem(scrapy.Item):
    '''
    新华社 信息安全
    http://www.news.cn/info/xxaq.htm
    '''
    url = scrapy.Field()            #文章链接
    title = scrapy.Field()          #标题
    title_img = scrapy.Field()      #缩略图链接，有的没有缩略图
    release_date = scrapy.Field()   #发布时间
    tag = scrapy.Field()            ##没有分类
    author = scrapy.Field()         #来源
    summary = scrapy.Field()        #摘要，正文第一段
    content_html = scrapy.Field()   #正文标签等全部内容
    content_txt = scrapy.Field()    #正文文字
    image_urls = scrapy.Field()     #正文图片链接

class secfreeItem(scrapy.Item):
    '''
    指尖安全 网络安全模块
    https://www.secfree.com/article_cat-12.html
    '''
    url = scrapy.Field()            #文章链接
    title = scrapy.Field()          #标题
    title_img = scrapy.Field()      #缩略图链接
    release_date = scrapy.Field()   #发布时间
    tag = scrapy.Field()       #分类，只有大类
    author = scrapy.Field()         #来源
    summary = scrapy.Field()        #摘要，正文第一段
    content_html = scrapy.Field()   #正文
    content_txt = scrapy.Field()    #正文文字
    image_urls = scrapy.Field()     #正文图片链接

class cnbetaItem(scrapy.Item):
    '''
    cnbeta 安全模块
    https://www.cnbeta.com/topics/157.htm
    '''
    url = scrapy.Field()            #文章链接
    title = scrapy.Field()          #标题
    title_img = scrapy.Field()      #缩略图链接
    release_date = scrapy.Field()   #发布时间
    tag = scrapy.Field()            #分类，只有大类‘科技’
    author = scrapy.Field()         #作者
    summary = scrapy.Field()        #摘要
    content_html = scrapy.Field()   #正文
    content_txt = scrapy.Field()    #正文文字
    image_urls = scrapy.Field()     #正文图片链接

class leiphoneItem(scrapy.Item):
    '''
    雷锋网 网络安全模块
    https://www.leiphone.com/category/letshome
    '''
    url = scrapy.Field()            #文章链接
    title = scrapy.Field()          #标题
    title_img = scrapy.Field()      #缩略图链接
    release_date = scrapy.Field()   #发布时间
    tag = scrapy.Field()            #标签
    author = scrapy.Field()         #来源
    summary = scrapy.Field()        #导语，无摘要
    content_html = scrapy.Field()   #正文
    content_txt = scrapy.Field()    #正文文字
    image_urls = scrapy.Field()     #正文图片链接

class easyaqItem(scrapy.Item):
    '''
    E安全
    https://www.easyaq.com/
    '''
    url = scrapy.Field()            #文章链接
    title = scrapy.Field()          #标题
    title_img = scrapy.Field()      #缩略图链接
    release_date = scrapy.Field()   #发布时间
    tag = scrapy.Field()            #标签
    author = scrapy.Field()         #作者，没有作者
    summary = scrapy.Field()        #摘要
    content_html = scrapy.Field()   #正文
    content_txt = scrapy.Field()    #正文文字
    image_urls = scrapy.Field()     #正文图片链接