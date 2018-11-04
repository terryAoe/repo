# -*- coding: utf-8 -*-
import re
import time
import datetime
import json
import scrapy
from scrapy.selector import Selector
from bigfish.items import SifaItem

class TbSifaSpider(scrapy.Spider):
    name = 'tb_sifa'
    page =1
    totalPage=None
    #allowed_domains = ['sifa.taobao.com']
    start_urls = ['https://sf.taobao.com/item_list.htm?province=%B1%B1%BE%A9&sorder=2']
    excel_file='d:/CODE/tb_sf.xlsx'
    custom_settings={
        # 'ITEM_PIPELINES':{
        #     'bigfish.pipelines.taobaoSFPipeline':301
        # }
        
    }
    def parse(self, response):
        if  response.url.startswith('https://sf.taobao.com/item_list'):
            print('scrapyed url:%s' % response.url)
            selector = Selector(response=response)
            item_list = selector.css('#sf-item-list-data::text').extract()
            item_json = json.loads(item_list[0])
            if self.totalPage is None:

                self.totalPage = int(int(selector.xpath('//li[@class="block"]/em[@class="count"]/text()').get()   )/8) + 1
            
            if self.page < self.totalPage:
                yield scrapy.Request(self.start_urls[0]  + '&page=' + str(self.page), method='GET' )
            for item in item_json['data']:
                yield scrapy.Request('https:'+item['itemUrl'],method='GET',meta=item)
            self.page+=1
        if response.url.startswith('https://sf-item.taobao.com/sf_item'):
            
            extractors = Selector(response=response)
            meta = response.request.meta
            if meta:
                item = SifaItem()
                item['_id']=meta['id']
                item['title']=meta['title']
                item['url'] = 'https' + meta['itemUrl']
                item['status']=meta['status']
                item['isSale'] =str(meta['sellOff'])
                detail_title=str(extractors.xpath('//h1/text()').get()).strip()
                item['saleTimes']=re.match('【([^】]*?)】.*',detail_title).group(1)
                item['evaluatePrice']=meta['consultPrice']
                item['startAuctionPrice']=meta['initialPrice']
                item['transctionPrice']=meta['currentPrice']
                item['signupNum']=meta['applyCount']
                item['observer']=meta['viewerCount']
                item['auctionTimes']=meta['bidCount']
                item['deferTimes']=meta['delayCount']
                item['startTime']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(meta['start']/1000))
                item['endTime']=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(meta['end']/1000))
                city_area=extractors.xpath('//div[@id="itemAddress"]/text()').get().split(' ')
                item['city']=city_area[1]
                item['area']=city_area[2]
                yield item

                #item['_id']=extractors.css('#J_ItemId::attr(value)').extract()[0]
                #item['title']=str(extractors.xpath('//h1/text()').get()).strip()
                #item['url'] =response.url
                #item['isSale'] ='false'
                # evaluatePrice=re.search(r'评 估 价.*\s*.*<span class="J_Price">(.*?)</span>',response.text)
                # if evaluatePrice:
                #     item['evaluatePrice']=evaluatePrice.group(1)
                # else:
                #     pass
                #item['startAuctionPrice']=extractors.xpath('//tbody[@id="J_HoverShow"]/tr/td[1]/span[@class="pay-price"]/span[@class="J_Price"]/text()').get()
                #item['transctionPrice']=extractors.xpath('//tbody[@id="J_HoverShow"]/tr/td[1]/span[@class="pay-price"]/span[@class="J_Price"]/text()').get()
                #item['signupNum']=extractors.xpath('//span[@class="pm-reminder i-b"]/em/text()').get()
                #item['observer']=extractors.css('#J_Looker::text').get()
                #item['auctionTimes']=extractors.xpath('//li[@id="sf-countdown"]/@data-start').get()
                #item['deferTimes']=extractors.xpath('//td[@class="delay-td"]/span[2]/text()').get()
                #item['deferTimes']=extractors.xpath('//em[@class="delayCnt"]/text()').get()
                #item['startTime']=extractors.xpath('//li[@id="sf-countdown"]/@data-start').get()
                #item['endTime']=extractors.xpath('//li[@id="sf-countdown"]/@data-end').get()

