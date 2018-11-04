#-*- coding:utf-8 -*-
import xlwt
from xlutils.copy import copy
import openpyxl
class ExcelUtils(object):
    excelFile=None
    rowIndex=0
    def __init__(self,excelFile,encoding='ascii'):
        self.excelFile=excelFile
        #self.xclBook = xlwt.Workbook(encoding=encoding)
        #self.sheet=self.xclBook.add_sheet('sheet1',cell_overwrite_ok=True)
        
        self.book = openpyxl.load_workbook(excelFile)
        self.wb = self.book.active

    
    @classmethod
    def default(cls,excelFile,encoding):

        return cls(excelFile=excelFile,encoding=encoding)
    
    #def writeXcl(self,rowData):
        #print(rowData)
        #columnSize=len(rowData)
        #for i in range(columnSize):
            
        #    self.sheet.write(r=self.rowIndex,c=i,label=rowData[i])
        #self.rowIndex+=1
        #book=copy(self.xclBook)
        #book.save(filename_or_stream=self.excelFile)
    def writeXcl(self,rowData):
        self.wb.append(rowData)
        self.book.save(self.excelFile)