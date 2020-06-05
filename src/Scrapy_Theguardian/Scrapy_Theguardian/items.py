# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ArticleItem(scrapy.Item):
    # the author of the article
    author = scrapy.Field()
    # the headline of the article
    headline = scrapy.Field()
    # the text of the article
    text = scrapy.Field()
    # the url of the article
    url = scrapy.Field()
    pass