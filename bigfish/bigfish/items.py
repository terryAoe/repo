# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy import Field

class BigfishItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



class SifaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = Field()#拍卖品编号
    title=Field()#标题
    url = Field()#链接
    status=Field()#状态
    isSale = Field()#是否拍卖成功
    saleTimes = Field()#拍卖次数
    evaluatePrice=Field()#评估价
    startAuctionPrice =Field()#起拍价
    transctionPrice=Field() #成交价
    signupNum=Field()#报名人数
    observer=Field() #观察人数
    auctionTimes=Field()#出价次数
    deferTimes=Field() #延时次数
    startTime=Field()#开始时间
    endTime=Field()#结束时间
    city=Field()#城市
    area=Field()#地区
