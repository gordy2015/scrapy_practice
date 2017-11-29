import json,os

class Zns_detail(object):
    def __init__(self):
        self.filename = ".\zns\爬取结果.txt"
        # self.filename = "爬取结果.txt"
        w = os.path.exists(self.filename)
        print(w)
    def process_item(self):
        with open(self.filename,'r',encoding='utf-8') as f:
            for line in f.readlines():
                # print(line)
                w = json.loads(line)
                print(type(w),w)


q = Zns_detail()
q.process_item()