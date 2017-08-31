# -*- coding: utf8 -*-
#time:2017/8/23 10:06
#VERSION:1.0
#__OUTHOR__:guangguang
#Email:kevinliu830829@163.com
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import RoadWriteFile
import  DNS,IPy,re,xlrd
def CheckDomain(DomainList,CDNList,IPList):
    DNS.DiscoverNameServers()
    reqobj = DNS.Request()
    reqobj.defaults['server']=['113.215.2.222']
    reg = 0
    Returndate = []
    MaxMum=len(IPList)
    for domain in DomainList:
        domain=domain.strip('\n')
        Returndomain=[]
        j = False
        try:
            answerobj = reqobj.req(name=domain,qtype = DNS.Type.A)
            x = answerobj.answers
            if not x:
                Returndate.append(str(domain) + "," + "无A记录" + "," + "域名出网,")
                continue
        except Exception, e:
            print e
            continue
        for donequeries in x:
            i = 1
            if j:
                break
            if donequeries['typename'] == "CNAME":  # 判断是否含有CNAME
                DomainCname = donequeries['data']
                CDN=ProcessData(DomainCname,CDNList)
                if CDN:
                    Returndomain=domain+','+CDN
                else:
                    Returndomain=domain+','+DomainCname
            elif donequeries['typename'] == "A":
                re_ip = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')  # 判断IP
                if re_ip.match(donequeries['data']):  # 直到IP停止
                    A = donequeries['data']
                    if Returndomain == []:
                        Returndomain=domain+','+'无CNAME'
                    if len(A) != 0:
                        try:
                            for LocalIp in IPList:
                                IP=str(LocalIp[1]).encode('utf-8')
                                if donequeries['data'] in IPy.IP(IP):
                                    Returndate.append(Returndomain + "," + "网内已经覆盖,")
                                    j=True
                                    break
                                elif i==MaxMum:
                                    Returndate.append(Returndomain + "," + "域名出网,")
                                    j=True
                                    break
                                i+=1

                        except Exception, e:
                            Returndate.append(str(Returndomain) + "," + "异常域名"+","+"域名出网,")
                            print e
                            break
            else:
                Returndate.append(str(Returndomain) + "," + "异常域名" + "," + "域名出网,")
        reg=reg+1
        if reg%100==0:
            print '正确域名'+':'+str('%d%%'%(reg/100))

    return Returndate
    pass




def ProcessData(cname,CDNList):
    for CDN in CDNList:
        if len(cname.split(CDN[1].encode('utf-8')))==2:
            return CDN[0].encode('utf-8')
        pass
    return False




#DEBUG
if __name__ == "__main__":
    DomainList=RoadWriteFile.ReadFile('jiangsu.txt')
    CDNList=RoadWriteFile.ReadFile('CDN.xls')
    IPList=RoadWriteFile.ReadFile('IPlist.xls')
    check = CheckDomain(DomainList.ReturnData(),CDNList.ReturnData(),IPList.ReturnData())
    f = open('jiangsucheckover.txt', 'w')
    for line in check:
        f.writelines(line+'\n')
    pass