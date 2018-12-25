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
        urldata = []
        jsondata = []
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
        elif mode=="anti":
            urls=urlParam.antiRandom(5)
            jsons=jsonParam.antiRandom(5)

        # print(len(urls))

        #获得独立URL
        if len(urls)>=1:
            for one in urls:
                urldata.append(host+url+"?"+"&".join(one))
        else:
            urldata.append(host + url)


        # print(urldata)
        # print(urldata)
        # print('**'*10)
        #获得独立json参数
        for one in jsons:
            params=tuple2dict(one)
            jsondata.append(params)
        # print(jsondata)
        #url json数据全量匹配
        for url in urldata:
            if len(jsondata)>=1:
                for params in jsondata:
                    tempUrl=UrlObj(method=method,host=host,url=url,name=name,desc=desc,expectCode=expectCode,
                               expectCotent=expectContent,headers=eval(headers),params=params)
                    alldata.append(tempUrl)
            else:
                tempUrl = UrlObj(method=method, host=host, url=url, name=name, desc=desc, expectCode=expectCode,
                                 expectCotent=expectContent, headers=eval(headers))
                alldata.append(tempUrl)
        # print(alldata)
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


def generateJmeterScript():
    res = getParams("i01_interfaceDef.ini", mode='pair')
    jmeterHeader='''<?xml version="1.0" encoding="UTF-8"?>
    <jmeterTestPlan version="1.2" properties="5.0" jmeter="5.0 r1840935">'''
    jmeterTailer='''</jmeterTestPlan>'''

    jmeterTestPlan='''<hashTree>    <TestPlan guiclass="TestPlanGui" testclass="TestPlan" testname="测试计划" enabled="true">
      <stringProp name="TestPlan.comments"></stringProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.tearDown_on_shutdown">true</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments" guiclass="ArgumentsPanel" testclass="Arguments" testname="User Defined Variables" enabled="true">
        <collectionProp name="Arguments.arguments"/>
      </elementProp>
      <stringProp name="TestPlan.user_define_classpath"></stringProp>
    </TestPlan>'''
    jmeterThreadGroup='''<hashTree><ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup" testname="线程组" enabled="true">
        <stringProp name="ThreadGroup.on_sample_error">continue</stringProp>
        <elementProp name="ThreadGroup.main_controller" elementType="LoopController" guiclass="LoopControlPanel" testclass="LoopController" testname="Loop Controller" enabled="true">
          <boolProp name="LoopController.continue_forever">false</boolProp>
          <stringProp name="LoopController.loops">1</stringProp>
        </elementProp>
        <stringProp name="ThreadGroup.num_threads">1</stringProp>
        <stringProp name="ThreadGroup.ramp_time">1</stringProp>
        <boolProp name="ThreadGroup.scheduler">false</boolProp>
        <stringProp name="ThreadGroup.duration"></stringProp>
        <stringProp name="ThreadGroup.delay"></stringProp>
      </ThreadGroup><hashTree>'''
    def getJmeterSampler(name,jsonPara,host,port,protocol,encoding,path,method):
        sampler='''<HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy" testname="{name}" enabled="true">
          <boolProp name="HTTPSampler.postBodyRaw">true</boolProp>
          <elementProp name="HTTPsampler.Arguments" elementType="Arguments">
            <collectionProp name="Arguments.arguments">
              <elementProp name="" elementType="HTTPArgument">
                <boolProp name="HTTPArgument.always_encode">false</boolProp>
                <stringProp name="Argument.value">{args}</stringProp>
                <stringProp name="Argument.metadata">=</stringProp>
              </elementProp>
            </collectionProp>
          </elementProp>
          <stringProp name="HTTPSampler.domain">{host}</stringProp>
          <stringProp name="HTTPSampler.port">{port}</stringProp>
          <stringProp name="HTTPSampler.protocol">{proto}</stringProp>
          <stringProp name="HTTPSampler.contentEncoding">{encoding}</stringProp>
          <stringProp name="HTTPSampler.path">{path}</stringProp>
          <stringProp name="HTTPSampler.method">{method}</stringProp>
          <boolProp name="HTTPSampler.follow_redirects">true</boolProp>
          <boolProp name="HTTPSampler.auto_redirects">false</boolProp>
          <boolProp name="HTTPSampler.use_keepalive">true</boolProp>
          <boolProp name="HTTPSampler.DO_MULTIPART_POST">false</boolProp>
          <stringProp name="HTTPSampler.embedded_url_re"></stringProp>
          <stringProp name="HTTPSampler.connect_timeout"></stringProp>
          <stringProp name="HTTPSampler.response_timeout"></stringProp>
        </HTTPSamplerProxy>'''.format(name=name,args=jsonPara,host=host,port=port,proto=protocol,encoding=encoding,path=path,method=method)
        return sampler

    def xmlEntityTrans(mystr):
        mystr=str(mystr)
        mystr=mystr.replace('<','&lt;')
        mystr=mystr.replace('>','&gt;')
        mystr=mystr.replace('&','&amp;')
        mystr=mystr.replace("'",'&apos;')
        mystr=mystr.replace('"','&quot;')
        return mystr

    def getJmeterHeader(headerString):
        headerPref= '''<hashTree><HeaderManager guiclass="HeaderPanel" testclass="HeaderManager" testname="请求头" enabled="true">
            <collectionProp name="HeaderManager.headers">'''

        headerSufx='''</collectionProp>
          </HeaderManager>'''

        allHeaders=""
        for k, v in headerString.items():
            temphader='''<elementProp name="" elementType="Header">
                <stringProp name="Header.name">{key}</stringProp>
                <stringProp name="Header.value">{value}</stringProp>
              </elementProp>'''.format(key=xmlEntityTrans(k),value=xmlEntityTrans(v))
            allHeaders=allHeaders+temphader
        return headerPref+allHeaders+headerSufx

    def getJmeterCodeAssert(code):
        jmeterAssert='''<hashTree/><ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="断言" enabled="true">
                <collectionProp name="Asserion.test_strings">
                  <stringProp name="26129577">{code}</stringProp>
                </collectionProp>
                <stringProp name="Assertion.custom_message"></stringProp>
                <stringProp name="Assertion.test_field">Assertion.response_code</stringProp>
                <boolProp name="Assertion.assume_success">false</boolProp>
                <intProp name="Assertion.test_type">16</intProp>
                <stringProp name="Assertion.scope">all</stringProp>
              </ResponseAssertion>'''.format(code=code)
        return jmeterAssert
    def getJmeterContentAssert(content):
        jmeterContentAssert='''<hashTree/><ResponseAssertion guiclass="AssertionGui" testclass="ResponseAssertion" testname="断言2" enabled="true">
            <collectionProp name="Asserion.test_strings">
              <stringProp name="36093938">{content}</stringProp>
            </collectionProp>
            <stringProp name="Assertion.custom_message"></stringProp>
            <stringProp name="Assertion.test_field">Assertion.response_message</stringProp>
            <boolProp name="Assertion.assume_success">false</boolProp>
            <intProp name="Assertion.test_type">16</intProp>
            <stringProp name="Assertion.scope">all</stringProp>
          </ResponseAssertion>
          <hashTree/></hashTree>'''.format(content=content)
        return jmeterContentAssert



    temp=""
    for sec in res:
        t=sec.host.split('//')[1]
        h=t.split(':')[0]
        p=t.split(':')[1]
        path=sec.url.split(str(p))[1]
        # print(sec.params)
        # print(xmlEntityTrans(sec.params))
        temp=temp+getJmeterSampler(xmlEntityTrans(sec.name),xmlEntityTrans(str(sec.params).replace("'",'"')),h,p,'http','utf-8',xmlEntityTrans(path),sec.method)
        temp=temp+getJmeterHeader(sec.headers)
        temp=temp+getJmeterCodeAssert(sec.expectCode)
        temp=temp+getJmeterContentAssert(xmlEntityTrans(sec.expectContent))

    allfile = jmeterHeader + jmeterTestPlan + jmeterThreadGroup+temp

    times=allfile.count('''<hashTree>''')
    # print(times)
    for one in range(0,times):
        allfile=allfile+"</hashTree>"
    allfile=allfile+jmeterTailer


    with open('out.jmx','w',encoding='utf-8') as f:
        f.write(allfile)



if __name__ == '__main__':
    res=getParams("i01_interfaceDef.ini",mode='pair')
    for sec in res:
        print(sec.desc,sec.name,sec.method,sec.host,sec.url,sec.headers,sec.params,sec.expectCode,sec.expectContent)
    print('{} 条数据'.format(len(res)))
    # write2Excel()
    generateJmeterScript()
