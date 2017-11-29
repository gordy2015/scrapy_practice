from zhihu.items import ZhihuItem
import scrapy,logging
from pyquery import PyQuery as pq
import os,json


class zihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]

    start_urls = ['http://www.zhihu.com']
    start_user = 'canfire'
    member_urls = "https://www.zhihu.com/api/v4/members/{urltoken}?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics"
    member_detail = "https://www.zhihu.com/api/v4/members/{urltoken}?include=locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccolumns_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cincluded_answers_count%2Cincluded_articles_count%2Cincluded_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_bind_phone%2Cis_force_renamed%2Cis_bind_sina%2Cis_privacy_protected%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cis_org_createpin_white_user%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics"



    def start_requests(self):
        # url = "https://www.zhihu.com/api/v4/members/feagle0311/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20'"
        url = "https://www.zhihu.com/api/v4/members/{user}/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20"
        yield scrapy.Request(url.format(user=self.start_user),callback=self.parse_urltoken)

    def parse_urltoken(self, response):
        # print(type(response.text),response.text)
        w = response.text
        p = json.loads(w)
        # print(type(p),p)
        for k,v in p.items():
            # print('%s:%s' %(k,v))
            if k == "data":
                # print(type(v),v)
                nu = 1
                for i in v:
                    # print(type(i),i)
                    s = 1
                    for k,v in i.items():
                        # print('[{nu}-{s}] {k}:{v}'.format(nu=nu,k=k,v=v,s=s))
                        if k == 'url_token':
                            # print('[{nu}-{s}] {k}:{v}'.format(nu=nu,k=k,v=v,s=s))
                            yield scrapy.Request(self.member_detail.format(urltoken=v),callback=self.parse_member_url)
                        s += 1
                    nu += 1

    def parse_member_url(self,response):
        item = ZhihuItem()

        m = json.loads(response.text)
        # print(item)
        # print(m)

        # for k,v in m.items():
        #     # print("%s:%s" %(k,v))
        #     item[k] = v
        #     yield item


        for fields in item.fields:
            if fields in m.keys():
                item[fields] = m.get(fields)
        #         # print('[{mn}] {k}:{v}'.format(k=k,v=v,mn=mn))

        yield item