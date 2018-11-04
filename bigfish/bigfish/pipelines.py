# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.utils.project import get_project_settings
from bigfish.utils.ExcelUtils import ExcelUtils


class BigfishPipeline(object):
    def process_item(self, item, spider):
        return item

class taobaoSFPipeline(object):
    def process_item(self,item,spider):
        if spider.name == 'tb_sifa':
            ExcelUtils.default(excelFile=spider.excel_file,encoding='utf-8').writeXcl(rowData=list(dict(item).values()))

            return
        
