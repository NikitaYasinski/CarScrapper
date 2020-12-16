# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class CarscrapperPipeline(object):
    
    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = self.conn['cars']
        self.collection = db['cars_tb']
    
    def process_item(self, item, spider):
        img = item['img']
        img = img.replace('");', '')
        img = img.replace('background-image: url("', '')
        item['img'] = img
        self.collection.insert(dict(item))
        return item
