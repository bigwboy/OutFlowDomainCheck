# -*- coding: utf8 -*-
#time:2017/8/23 10:07
#VERSION:1.0
#__OUTHOR__:guangguang
#Email:kevinliu830829@163.com
import xlrd,re
import DNS
import IPy
class ReadFile():
    def __init__(self,Filename):
        self.Filename=Filename
        self.DomailList=[]
        pass
    def ReturnData(self):
        FileType=self.Filename.split(".")[-1]
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
                CDN=ProcessData(DomainCname)
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


def ProcessData(cname):
    types = {
        "蓝讯": ["ccgslb.net", "ccgslb.com", "ccgslb.com.cn", "chinacache.net", "chinacache.com.cn", "lxsvc.cn"],
        "网宿": ["glb0.lxdns.com", "ourdvs.com", "ourwebpic.com", "ourwebcdn.com", "ourglb0.com", "ourwebhttps.com",
               "ourwebat.com"],
        "快网": ["fastweb.com", "fastwebcdn.com", "cloudcdn.net", "cloudglb.com", "cachecn.com", "cachecn.net",
               "hadns.net", "hacdn.net"],
        "帝联": ["dnion.com", "ewcache.com", "globalcdn.cn", "tlgslb.com", "fastcdn.com"],
        "百度": ["jomodns.com"],
        "京东": ["jdcdn.com"],
                "淘宝":["alikunlun.com"
                        ,"alikunlun.net"
                        ,"kunlunaq.com"
                        ,"kunlunar.com"
                        ,"kunlunca.com"
                        ,"kunluncan.com"
                        ,"kunlunea.com"
                        ,"kunlungem.com"
                        ,"kunlungr.com"
                        ,"kunlunhuf.com"
                        ,"kunlunle.com"
                        ,"kunlunli.com"
                        ,"kunlunno.com"
                        ,"kunlunpi.com"
                        ,"kunlunra.com"
                        ,"kunlunsa.com"
                        ,"kunlunsc.com"
                        ,"kunlunsl.com"
                        ,"kunlunso.com"
                        ,"kunlunta.com"
                        ,"kunlunvi.com"
                        ,"kunlunwe.com"
                        ,"alicdn.com"
                        ,"tbcache.com"
                        ],
        "新浪": ["sinaedge.com"],
        "爱奇艺": ["dns.iqiyi.com"],
        "PPTV": ["cloudxns.pptv.com"],
        "腾讯":["tc.qq.com","tcdn.qq.com","myqcloud.com","dayugslb.com","tencent-cloud.net","tcdnvod.com","tcdnlive.com","cdntip.com"],
        "沙塔": ["satacdn.com", "sihuacdn.com.cn", "okeycdn.com"],
        "云帆": ["yflive.net", "yunfancdn.com"],
        "金山云": ["ks-cdn.com", "ksyuncdn.com"],
        "白山云": ["qingcdn.com", "bsgslb.com", "trpcdn.net", "bsgslb.cn", "bsclink.cn"],
        "迅雷星域": ["p2cdn.com", "00cdn.com", "xycdn.com"],
        "又拍云": ["b0.upaiyun.com", "b0.aicdn.com"],
        "小米": ["mgslb.com"],
        "乐视云": ["gslb.lecloud.com", "lsyun.net", "cdnle.com"],
    }
    all={}
    for t in types.iteritems():
        for hz in t[1]:
            all[hz]=t[0]
        for type in all.iteritems():
            if len(cname.split(type[0]))==2:
                return type[1]
    return False
#DEBUG
if __name__ == "__main__":
    DomainList=ReadFile('jiangsu.txt')
    check=CheckDomain(DomainList.ReturnData())
    WriteDate=check.ReturnDate()
    WriteFile(WriteDate)