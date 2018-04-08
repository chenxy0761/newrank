# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WechatSubItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class WecatItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    click_count = scrapy.Field()
    likes_count = scrapy.Field()
    rank_date = scrapy.Field()
    pass
