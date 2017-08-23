# -*- coding: utf8 -*-
#time:2017/8/23 10:06
#VERSION:1.0
#__OUTHOR__:guangguang
#Email:kevinliu830829@163.com
import RoadWriteFile
import  DNS,IPy,re,xlrd
def CheckDomain(DomainList,CDNList):
    DNS.DiscoverNameServers()
    reqobj = DNS.Request()
    reqobj.defaults['server']=['113.215.2.222']
    Returndate=[]
    for domain in DomainList:
        domain=domain.strip('\n')
        try:
            answerobj = reqobj.req(name=domain,qtype = DNS.Type.A)
            x = answerobj.answers
        except Exception, e:
            print e
            continue
        for donequeries in x:
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
                    if len(A) != 0:
                        try:
                            if donequeries['data'] in IPy.IP("113.214.0.0/15"):
                                Returndate.append(Returndomain + "，" + "网内已经覆盖，")
                                break
                            elif donequeries['data'] in IPy.IP("43.247.232.0/22"):
                                Returndate.append(Returndomain + "，" + "网内已经覆盖，")
                                break
                            else:
                                Returndate.append(Returndomain + "，" + "域名出网，")
                                break
                        except Exception, e:
                            print e
                            break

    return Returndate
    pass




def ProcessData(cname,CDNList):
    for CDN in CDNList:
        if len(cname.split(CDN[0]))==2:
            return CDN[1]
        pass
    return False




#DEBUG
if __name__ == "__main__":
    DomainList=RoadWriteFile.ReadFile('jiangsu.txt')
    CDNList=RoadWriteFile.ReadFile('CDN域表.xls')
    check = CheckDomain(DomainList.ReturnData(),CDNList.ReturnData())
    pass