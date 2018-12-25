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




def getParams(iniFilePath):
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
        targetdata={}
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
                        # print(data)
                        #拼接参数url参数部分
                        paraValue = paraValue.lstrip("p")
                        # print(paraValue)
                        for one in eval(paraValue):
                            paraList.append(paraName + "=" + str(one))
                        # print(paraList)
                    else:
                        paraList.append(paraName+"=")
                    # 添加到列表
                    sectionParamData.append(paraList)
        # print(sectionData)
        # print(sectionJsonData)
        up=""
        if len(sectionParamData)>0:
            for pp in sectionParamData:
                for p in pp:
                    up=up+p+"&"
        up=up.rstrip("&")
        jdata=""
        temp=""
        if len(sectionJsonData)>0:
            for jj in sectionJsonData:
                for j in jj:
                    temp=temp+j+','
            temp=temp.rstrip(",")
            jdata=tuple2dict(temp.split(","))

        if len(up)>0:
            # print("{}  {}{}?{}  {}  {}  {}".format(desc,host,url,up,headers,method,jdata))
            targetdata['name']=desc
            targetdata['host']='{}{}?{}'.format(host,url,up)
            targetdata['url'] = '{}?{}'.format( url, up)
            targetdata['jdata']=jdata
            targetdata['expectCode'] = expectCode
            targetdata['expectContent'] = expectContent
        else:
            # print("{}  {}{}{}  {}  {}  {}".format(desc,host, url, up, headers,method, jdata))
            targetdata['name']=desc
            targetdata['host']='{}{}{}'.format(host,url,up)
            targetdata['url'] = '{}{}'.format( url, up)
            targetdata['jdata']=jdata
            targetdata['expectCode'] = expectCode
            targetdata['expectContent'] = expectContent
        alldata.append(targetdata)

    return alldata


from xlwt import *
import xlrd
from xlutils import copy
def write2Excel():
    res = getParams("i01_interfaceDef.ini")
    file=xlrd.open_workbook('caes.xlsx')
    table1=file.sheet_by_name('InterfaceCase')
    rows=table1.nrows
    cols=table1.ncols

    new_file=copy.copy(file)
    table=new_file.get_sheet(0)

    for row in range(0,rows):
        # for col in range(0,table.ncols):
        for item in res:
            if item['name']==table1.cell(row,0).value and item['expectCode']=='200':
                table.write(row,8,item['url'])
                table.write(row,9,str(item['jdata']))
                table.write(row, 11, str(item['expectCode']))
                table.write(row, 12, str(item['expectContent']))

    new_file.save('caes1.xlsx')

if __name__ == '__main__':
    # res=getParams("i01_interfaceDef.ini")
    # print(res)
    write2Excel()
    # for sec in res:
    #     print(sec.desc,sec.name,sec.method,sec.host,sec.url,sec.headers,sec.params,sec.expectCode,sec.expectContent)
    # print('{} 条数据'.format(len(res)))
    # write2Excel()
