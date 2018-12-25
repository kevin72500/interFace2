# coding:utf-8
import configparser
import itertools
import queue
from AutoParamEngine import ParamGener

class myConfig(configparser.ConfigParser):
    def __init__(self,defaults=None):
        configparser.ConfigParser.__init__(self,defaults=defaults)
    def optionxform(self, optionstr):
        return optionstr

class iniReader():
    def __init__(self, filePath, encoding='utf-8'):
        self.cf = myConfig()
        self.cf.read(filePath, encoding=encoding)

    def getSections(self):
        # print(self.cf.sections())
        return self.cf.sections()

    def getOptions(self, sectId):
        # print(self.cf.options(sectId))
        return self.cf.options(sectId)

    def getItem(self, section, option):
        # print(self.cf.get(section, option))
        return self.cf.get(section, option)


def production(*args):
    # 对列表进行笛卡儿积，并按照一个列表返回
    all = []
    for i in itertools.product(*args):
        all.append(i)
    return all


class UrlObj():
    __slots__=['method','host','url','name','desc','expectCode','expectContent','retCode','retContent','result','params','headers']
    def __init__(self,method="",host="",url="",name="",desc="",expectCode="",expectCotent="",retCode="",retContent="",result="",params=None,headers=None):
        self.method=method
        self.host=host
        self.url=url
        self.name=name
        self.desc=desc
        self.expectCode=expectCode
        self.expectContent=expectCotent
        self.retCode=retCode
        self.retContent=retContent
        self.result=result
        self.params=params
        self.headers=headers


def tuple2dict(tempTuple):
    # t=('sourcePointId=100281997', 'sourcePointName=23ewqrewqr', 'sourcePointDesc=2', 'sourcePointState=0')
    retDict={}
    for one in tempTuple:
        temp=one.split('=')
        retDict[temp[0]]=temp[1]
    return retDict




def getParams(iniFilePath,mode="all"):
    cf = iniReader(iniFilePath)
    urldata=[]
    jsondata=[]
    alldata = queue.deque()
    host=""
    method=""
    url=""
    name=""
    desc=""
    expectCode=""
    expectContent=""
    headers=""
    params=""
    for section in cf.getSections():
        #区域数据
        sectionJsonData=[]
        sectionParamData = []
        paramData=[]
        for option in cf.getOptions(section):
            #获取主机信息
            if option.lower()=='host':
                host=cf.getItem(str(section),str(option))
            #获取方法头
            elif option.lower()=='method':
                method=cf.getItem(str(section),str(option))
            #获取名字
            elif option.lower()=='name':
                name=cf.getItem(str(section),str(option))
            #获取描述
            elif option.lower()=='desc':
                desc=cf.getItem(str(section),str(option))
            #获取URL
            elif option.lower()=='url':
                url=cf.getItem(str(section),str(option))
            #获取期望返回码
            elif option.lower()=='expectcode':
                expectCode=cf.getItem(str(section),str(option))
            #获取期望返回内容
            elif option.lower()=='expectcontent':
                expectContent=cf.getItem(str(section),str(option))
            elif option.lower()=='headers':
                headers=cf.getItem(str(section),str(option))
            #其他数据判断
            else:
                data = cf.getItem(str(section), str(option))
                #判断是否是参数
                if data.startswith('j('):# and len(data) > 2:
                    paraName = option
                    paraValue = data
                    paraList = []
                    if len(data)>2:
                        #拼接参数url参数部分
                        paraValue=paraValue.lstrip("j")
                        for one in eval(paraValue):
                            paraList.append(paraName + "=" + str(one))
                        # print(paraList)
                    else:
                        paraList.append(paraName+"=")
                    # 添加到列表
                    sectionJsonData.append(paraList)
                if data.startswith('p('):# and len(data) > 2:
                    paraName = option
                    paraValue = data
                    paraList = []
                    if len(data)>2:
                        #拼接参数url参数部分
                        paraValue = paraValue.lstrip("p")
                        for one in eval(paraValue):
                            paraList.append(paraName + "=" + str(one))
                        # print(paraList)
                    else:
                        paraList.append(paraName+"=")
                    # 添加到列表
                    sectionParamData.append(paraList)
        # print(sectionData)
            #初始化参数
            urlParam = ParamGener(*sectionParamData)
            jsonParam = ParamGener(*sectionJsonData)

            #选取参数配对方式
            urls=[]
            jsons=[]
            if mode=="all":
                urls=urlParam.allConbine()
                jsons=jsonParam.allConbine()
            elif mode=="pair":
                urls=urlParam.pairWiseMore()
                jsons=jsonParam.pairWiseMore()

            #获得独立URL
            if len(urls)>1:
                for one in urls:
                    urldata.append(host+url+"?"+"&".join(one))
            else:
                urldata.append(host + url )
        # print(urldata)
        # print('**'*10)
            #获得独立json参数
            for one in jsons:
                params=tuple2dict(one)
                jsondata.append(params)
        # print(jsondata)
        #url json数据全量匹配
        for url in urldata:
            for params in jsondata:
                tempUrl=UrlObj(method=method,host=host,url=url,name=name,desc=desc,expectCode=expectCode,
                           expectCotent=expectContent,headers=eval(headers),params=params)
                alldata.append(tempUrl)
    return alldata


from xlwt import *
def write2Excel():
    res = getParams("i01_interfaceDef.ini",mode="pair")
    file=Workbook(encoding='utf-8')
    sheet=file.add_sheet('data')
    for num,sec in enumerate(res):
        # sheet.write(,sec.name,sec.method,sec.host,sec.url,sec.headers,sec.params,sec.expectCode,sec.expectContent)
        sheet.write(num,0,sec.desc)
        sheet.write(num, 1, sec.name)
        sheet.write(num, 2, sec.method)
        sheet.write(num, 3, sec.host)
        sheet.write(num, 4, sec.url)
        sheet.write(num, 5, str(sec.headers).replace("'",'"'))
        sheet.write(num, 6, str(sec.params).replace("'",'"'))
        sheet.write(num, 7, sec.expectCode)
        sheet.write(num, 8, sec.expectContent)
    file.save('caes.xlsx')

if __name__ == '__main__':
    res=getParams("i01_interfaceDef.ini",mode='pair')
    for sec in res:
        print(sec.desc,sec.name,sec.method,sec.host,sec.url,sec.headers,sec.params,sec.expectCode,sec.expectContent)
    print('{} 条数据'.format(len(res)))
    # write2Excel()
