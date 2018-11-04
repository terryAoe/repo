# -*- coding: utf-8 -*-
import scrapy

from bigfish.items import SifaItem
from scrapy import linkextractors
from scrapy.selector import Selector
import json
import re
#from urllib.parse import urljoin
import datetime


class TaobaoSifaSpider(scrapy.Spider):
    name = 'taobao_sifa'
    #allowed_domains = ['www.taobao.com','sf-item.taobao.com','sf.taobao.com']
    start_urls = ['https://sf.taobao.com/item_list.htm?province=%B1%B1%BE%A9&sorder=2']
    page=1
    def parse(self, response):

        if response.url.startswith('https://sf.taobao.com/item_list'):
           
            print('scrapyed url:%s' % response.url)
            # for link in LinkExtractor().extract_links(response):
            #     url = link.url
            #     #if url.index('sf.taobao.com/item_list') > 0:
            #     print(url)
            selector = Selector(response=response)

            item_list = selector.css('#sf-item-list-data::text').extract()
           # item_list = selector.re('<script id="sf-item-list-data" type="text/json">(.*?)</script>')
            item_json=json.loads(item_list[0])
            self.page+=1
            if self.page < 150:
                yield scrapy.Request(self.start_urls[0] + '&page=' + str(self.page),method='GET')
            for item in item_json['data']:
                yield scrapy.Request('https:'+item['itemUrl'],)
        elif response.url.startswith('https://sf-item.taobao.com/sf_item'):
            extractors = Selector(response=response)

            item = SifaItem()
            item['_id']=extractors.css('#J_ItemId::attr(value)').extract()[0]
            item['title']=str(extractors.xpath('//h1/text()').get()).strip()
            item['url'] =response.url
            item['isSale'] ='false'
            item['saleTimes']=''
            evaluatePrice=re.search(r'评 估 价.*\s*.*<span class="J_Price">(.*?)</span>',response.text)
            if evaluatePrice:
                item['evaluatePrice']=evaluatePrice.group(1)
            else:
                pass
            item['startAuctionPrice']=extractors.xpath('//tbody[@id="J_HoverShow"]/tr/td[1]/span[@class="pay-price"]/span[@class="J_Price"]/text()').get()
            item['transctionPrice']=extractors.xpath('//tbody[@id="J_HoverShow"]/tr/td[1]/span[@class="pay-price"]/span[@class="J_Price"]/text()').get()
            item['signupNum']=extractors.xpath('//span[@class="pm-reminder i-b"]/em/text()').get()
            item['observer']=extractors.css('#J_Looker::text').get()
            item['auctionTimes']=extractors.xpath('//li[@id="sf-countdown"]/@data-start').get()
            #item['deferTimes']=extractors.xpath('//td[@class="delay-td"]/span[2]/text()').get()
            item['deferTimes']=extractors.xpath('//em[@class="delayCnt"]/text()').get()
            item['startTime']=extractors.xpath('//li[@id="sf-countdown"]/@data-start').get()
            item['endTime']=extractors.xpath('//li[@id="sf-countdown"]/@data-end').get()
            city_area=extractors.xpath('//div[@id="itemAddress"]/text()').get().split(' ')
            item['city']=city_area[1]
            item['area']=city_area[2]
            print(repr(item))
    def errorback(self, err):
        print(err)
        yield scrapy.Request(err.request.url)
