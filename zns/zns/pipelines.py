

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json,os
from pymongo import MongoClient

class ZnsJson(object):
    def __init__(self):
        filename = '爬取结果.txt'
        # /home/gordy/PycharmProjects/scrapy_study/zns/zns/zhinengsuobaike.txt
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


class ZnsMongo(object):
    def __init__(self):
        self.client = MongoClient('link.138.com',38999)
        self.db = self.client.pymo_test

    def process_item(self,item,spider):
        zntalbe = self.db.zntable2
        zntalbe.insert_one(dict(item))
        return item

class Zns_detail(object):
    def __init__(self):
        self.filename = '爬取结果.txt'

    def process_item(self,item,spider):
        with open(self.filename,'r',encoding='utf-8') as f:
            for line in f.readlines():
                w = json.loads(line)
                print('----here:%s %s' %(type(w),w))
        return item