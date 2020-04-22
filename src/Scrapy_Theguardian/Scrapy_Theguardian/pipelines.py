# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class CrawlertheguardianPipeline(object):

    collection_name = 'articles'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    

    def process_item(self, item, spider):
        bbcDict={}
        if item['text'] != []:
            bbcDict['headline']=item['headline']
            bbcDict['author']=item['author']
            bbcDict['text']=" ".join(item['text'])
            bbcDict['url']=item['url']
            self.db['articles'].insert_one(dict(bbcDict))
            return item
        
    
    def close_spider(self, spider):
        self.client.close()