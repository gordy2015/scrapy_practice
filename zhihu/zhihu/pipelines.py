# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
import logging
from zhihu import settings
import pymongo

class ZhihuPipeline(object):
    def process_item(self, item, spider):
        return item

class member_json(object):
    def __init__(self):
        filename = 'member_json.txt'
        w = os.path.exists(filename)
        # print('%s -----w is %s' %(os.getcwd(),bool(w)))
        if w:
            os.remove(filename)
        self.file = open(filename, 'w',encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False)  + '\n'
        # print('------%s,here:%s --------' %(type(dict(item)),dict(item)))
        self.file.write(line)
        return item

class member_mongodb(object):
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

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # 去重方法1) 这里通过mongodb进行了一个去重的操作，每次更新插入数据之前都会进行查询，判断要插入的url_token是否已经存在，如果不存在再进行数据插入，否则放弃数据
        self.db['member_detail'].update({'url_token': item["url_token"]}, {'$set': item}, True)
        # print(type(item))  #<class 'zhihu.items.ZhihuItem'>


        # 去重方法2) 通过查询，并在插入前查询是否已存在
        # di = {"url_token": item['url_token']} #url_token是唯一的,可用于查询 或直接用dict(item)查询
        # w = self.db.member_detail.find_one(di)
        # # print(type(w),bool(w),w)  #find_one如果查询到有结果会返回True, dict类型, 如到结果，返回False, 会是None类型
        # if w:
        #     logging.info("Duplicate item found: %s"%item['url_token'])
        # else:
        #     self.db['member_detail'].insert_one(dict(item))  # 这也是向db中插入数量，但没有对数据做去重操作


        return item


