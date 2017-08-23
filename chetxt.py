# -*- coding: utf8 -*-
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import DNS, re
import csv
import xlrd
import IPy


def ReadFile(Filename):
    suffix= Filename.split(".")
    if suffix[-1]== "xlsx":
        data = xlrd.open_workbook(Filename)
        table = data.sheet_by_index(0)
        nrows = table.nrows
        domainList={}
        for i in range(nrows):
            domainList[table.row_values(i)[1]]= table.row_values(i)[3]
    elif suffix[-1]=="txt":
        data= open(Filename,'r')
        domainList = {}
        for i in data.readlines():
            domainList[i.strip()]="网信分析"
    elif suffix[-1] == "xls":
        data = xlrd.open_workbook(Filename)
        table = data.sheet_by_index(0)
        nrows = table.nrows
        domainList = {}
        for i in range(nrows):
            domainList[table.row_values(i)[0]] = "网信分析"
    return domainList



f = open('dnslog.txt', 'w')
def WrlteFile(domain,company,CP_NAME="无CNAME"):
    WDATA=domain+" "+company+" "+str(CP_NAME)+'\n'
    f.writelines(WDATA)
        #f.writelines(WDATA)


def FindCNAME(domain):
    DNS.DiscoverNameServers()
    reqobj = DNS.Request()
    try:
        print domain
        answerobj = reqobj.req(domain)  #这句
        x = answerobj.answers
    except Exception,e:
        print e
        return  "none"
    for donequeries in x:
        if donequeries['typename']=="CNAME": #判断是否含有CNAME
            answers = []
            i=[]
            re_ip = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$') #判断IP
            for i in x:
                if not re_ip.match(i['data']):#直到IP停止
                    answers=i['data']
            if len(answers) != 0:
                try:
                    if i['data'] in IPy.IP("113.214.0.0/15"):
                        answers=answers+" "+"网内已经覆盖"
                    elif i['data'] in IPy.IP("43.247.232.0/22"):
                        answers=answers+" "+"网内已经覆盖"
                    else:
                        answers=answers+" "+"域名出网"
                except Exception,e:
                    print e
            return answers #返回最后一个CNAME
        else:
            if donequeries['data'] in IPy.IP("113.214.0.0/15"):
                return  "none" + " " + "网内已经覆盖"
            else:
                return   "none" + " " + "域名出网"

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
    return "CNAME不在服务列表中"





if __name__=="__main__":
    #读取文件返回字典{域名：公司名}
    domainList=ReadFile("jiangsu.txt")
    data=[]
    i=1
    f = open('jiangsucheckover.txt', 'w')
    re_ip = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    for domain in domainList.iteritems():
        if not re_ip.match(domain[0]):
            answers = FindCNAME(domain[0])
            f.writelines(domain[0]+","+str(answers)+'\n')
    '''  
        if not answers=="none"and answers:
            CP_NAME=ProcessData(answers)
        else:
            CP_NAME="无CNAME"
        WrlteFile(domain[0], domain[1], CP_NAME)
    '''

        #print domain#每行最后新加覆盖CP标识