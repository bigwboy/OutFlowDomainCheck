# -*- coding: utf8 -*-
#time:2017/8/23 10:07
#VERSION:1.0
#__OUTHOR__:guangguang
#Email:kevinliu830829@163.com
import xlrd,re
import DNS
import IPy
class ReadFile():
    def __index__(self,Filename):
        self.Filename=Filename
        self.DomailList=[]
        pass
    def ReturnDate(self):
        FileType=self.Filename.stlit('.')[-1]
        if FileType=='txt':
            return self.ReadTxt()
        elif FileType=='xls' or FileType=='xlsx':
            return self.ReadExecL()
    def ReadTxt(self):
        data = open(self.Filename, 'r')
        for i in data.readlines():
            self.DomailList.append(i)
        return self.DomailList
        pass
    def ReadExecL(self):
        data = xlrd.open_workbook(self.Filename)
        table = data.sheet_by_index(0)
        nrows = table.nrows
        for i in range(nrows):
            self.DomailList.append(i)
        return self.DomailList
        pass
def WriteFile():
    pass
def CheckDomain(DomainList):
    return
    pass
#DEBUG
if __name__ == "__main__":
    DomainList=ReadFile('jiangsu.txt')
    WriteDate=CheckDomain(DomainList)
    WriteFile(WriteDate)