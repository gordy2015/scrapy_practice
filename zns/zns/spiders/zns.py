
from zns.items import ZnsItem
import scrapy,logging
from pyquery import PyQuery as pq
import os,json


class znsSpider(scrapy.Spider):
    name = "zns"
    # allowed_domains = ["link2sky.com"]
    base_url = "http://zhinengsuobaike.com/topic/innews/page/"
    
    start_urls = ['http://zhinengsuobaike.com/topic/innews']
    # for i in range(2, 11):
    #     burl = base_url + str(i)
    #     start_urls.append(burl)
    # print(start_urls)

    # def make_requests_from_url(self, url):
    #     return scrapy.Request(url=url,meta={'download_timeout':10},callback=self.parse)
    #
    # def process_exception(self,request,exception,spider):
    #     self.logger.info("GET Exception")
    #     # request.meta['proxy'] = 'http://127.0.0.1:9891'
    #     return request

    def parse(self, response):
        # print(response.url)
        # print(type(response.body.decode()), type(response.body))
        html = response.body
        doc = pq(html.decode())
        ta = doc('.entry-title a')
        tc = ta.length
        # print('length: %s' % tc)
        # t = ta.attr('href')
        item = ZnsItem()

        # self.logger.info('A response from %s just arrived!', response.url)

        for i in range(0, tc):
            ti = doc(ta[i])
            url = ti.attr('href')
            item['url'] = url
            title = ti.text()
            item['title'] = title
            fdate = ti.parent().parent().siblings().eq(2).children().eq(2).text()
            if fdate == 'NEW':
                fdate = ti.parent().parent().siblings().eq(
                    2).children().eq(3).children().eq(0).text()
            else:
                fdate = ti.parent().parent().siblings().eq(
                    2).children().eq(2).children().eq(0).text()
            item['date'] = fdate
            # print('%s: fdate: %s %s' % (i,type(fdate),fdate))

            yield item


