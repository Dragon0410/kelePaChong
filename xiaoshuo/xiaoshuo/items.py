# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaoshuoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_name = scrapy.Field() # 书名
    book_author = scrapy.Field() # 作者
    book_author_link = scrapy.Field() # 作者链接
    book_name_link = scrapy.Field() # 书链接
    edit_status = scrapy.Field() # 编辑状态
    book_category = scrapy.Field() # 分类
    book_tags = scrapy.Field() # 标签
    book_total_words = scrapy.Field() # 总字数
    book_count_recommends = scrapy.Field() # 总推荐
    book_total_clicks = scrapy.Field() # 总点击
    book_summary = scrapy.Field() # 简介
    book_catalogue_link  = scrapy.Field() # 目录链接

