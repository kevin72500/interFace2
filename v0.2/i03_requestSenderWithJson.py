#coding:utf-8
import requests
from requests import adapters
from concurrent import futures
from i02_initReader_general import getParams,UrlObj
from threading import Thread
from queue import deque
import json
import jinja2
import time,datetime
import asyncio
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import re
from re import match,compile,search


def resultContain(realValue,expectValue):
    mode=re.compile(expectValue.encode('utf-8'))
    res=mode.search(realValue)
    if res:
        # print(res.groups())
        return True,"成功：返回内容包含--"+expectValue
    else:
        return False,"失败：返回内容不包含--"+expectValue

def resultCodeCompare(realValue,expectValue):
    if realValue==expectValue:
        return True,"成功：返回码--"+expectValue
    else:
        return False,"失败：返回码--"+expectValue




def singleSender(method,url,**kwargs):
    res=None
    requests.adapters.DEFAULT_RETRIES = 10
    try:
        if method.lower()=="get":
            res=requests.get(url,**kwargs)
        elif method.lower()=='post':
            res=requests.post(url,**kwargs)
        elif method.lower()=='put':
            res=requests.put(url,**kwargs)
        elif method.lower()=='delete':
            res=requests.delete(url,**kwargs)
        elif method.lower()=='patch':
            res=requests.patch(url,**kwargs)
        return res.status_code,res.content

    except Exception as e:
        print(e)


async def gevnetSender(urlObj):
    retObj=UrlObj()
    retObj.desc = urlObj.desc
    retObj.name = urlObj.name
    retObj.method = urlObj.method
    retObj.url = urlObj.url
    retObj.expectCode=urlObj.expectCode
    retObj.expectContent=urlObj.expectContent

    # print(type(urlObj.headers))
    # print(urlObj.headers)
    try:
        if urlObj.params.__len__()==0 and urlObj.headers.__len__()==0:
            retObj.retCode, retObj.retContent = singleSender(urlObj.method, urlObj.url)
        elif urlObj.params.__len__()==0:
            retObj.retCode, retObj.retContent= singleSender(urlObj.method,
                                                             urlObj.url,
                                                             headers=urlObj.headers)
            retObj.headers=urlObj.headers
        else:
            retObj.retCode, retObj.retContent = singleSender(urlObj.method, urlObj.url,
                                                         headers=urlObj.headers,
                                                         data=json.dumps(urlObj.params))
            retObj.headers = urlObj.headers
            retObj.params = urlObj.params
    except Exception as e:
        print(e)
    return retObj


#继承多线程类
class multiThreadSender(Thread):
    #初始化
    def __init__(self,urlOjb):
        super(multiThreadSender,self).__init__()
        self.UrlObj=urlOjb
        self.ret=None
    #执行单线程，并获取返回
    def run(self):
        # for one in self.UrlObj:
        retObj=UrlObj()
        retObj.desc=self.UrlObj.desc
        retObj.name=self.UrlObj.name
        retObj.method=self.UrlObj.method
        retObj.url=self.UrlObj.url
        retObj.expectCode = self.UrlObj.expectCode
        retObj.expectContent = self.UrlObj.expectContent
        retObj.headers = self.UrlObj.headers
        retObj.params = self.UrlObj.params
        # retObj.retCode,retObj.retContent=singleSender(self.UrlObj.method,self.UrlObj.url,
        #                                               headers=UrlObj.headers,data=json.dumps(UrlObj.params))
        try:
            if self.UrlObj.params.__len__() == 0 and self.UrlObj.headers.__len__() == 0:
                retObj.retCode, retObj.retContent = singleSender(self.UrlObj.method, self.UrlObj.url)
            elif UrlObj.params.__len__() == 0:
                retObj.retCode, retObj.retContent = singleSender(self.UrlObj.method,
                                                                 self.UrlObj.url,
                                                                 headers=self.UrlObj.headers)
            else:
                retObj.retCode, retObj.retContent = singleSender(self.UrlObj.method, self.UrlObj.url,
                                                                 headers=self.UrlObj.headers,
                                                                 data=json.dumps(self.UrlObj.params))

        except Exception as e:
            print(e)


        self.ret=retObj
    #获取返回
    def getReturn(self):
        return self.ret



def multiSender(thread_num,requestList):
    workers=min(thread_num,len(requestList))
    with futures.ThreadPoolExecutor(workers) as runner:
        res=runner.map(singleSender,requestList)


#单进程，顺序执行
def singleExecuter(items):
    # starttime=datetime.datetime.now()
    # items=getParams("i01_interfaceDef.ini")
    retList=[]
    for one in items:
        # print(one.url)
        one.retCode,one.retContent=singleSender(one.method,one.url,
                                                headers=one.headers,data=json.dumps(one.params))
        tempOjb=UrlObj(one.method,one.host,one.url,one.name,one.desc,one.expectCode,one.expectContent,one.retCode,one.retContent)
        retList.append(tempOjb)
    # endtime=datetime.datetime.now()
    newRes=[]
    for one in retList:
        tempList=[]
        flag,res=resultContain(one.retContent, one.expectContent)
        if flag:
            one.result=res
            # print(one.result,one.desc,one.retCode,one.name,one.url,one.retContent,one.retCode,one.retContent,one.expectCode,one.expectContent)
            print(one.desc,one.result, one.retCode, one.name, one.url,one.retContent.decode('utf-8'))
            tempList.append(one.desc)
            tempList.append(one.result)
            tempList.append(str(one.retCode))
            tempList.append(one.name)
            tempList.append(one.url)
            tempList.append(one.retContent.decode('utf-8'))
        else:
            one.result=res
            print(one.desc,one.result, one.retCode, one.name, one.url,one.retContent.decode('utf-8'))
            tempList.append(one.desc)
            tempList.append(one.result)
            tempList.append(str(one.retCode))
            tempList.append(one.name)
            tempList.append(one.url)
            tempList.append(one.retContent.decode('utf-8'))
        newRes.append(tempList)
    return newRes
    # print((endtime-starttime).seconds)

#多进程
def multiExcuter(items):
    # starttime = datetime.datetime.now()
    # items=getParams("i01_interfaceDef.ini")

    threadList=deque()
    for one in items:
        threadList.append(multiThreadSender(one))
    returnList=[]
    resultList=[]
    for t in threadList:
        t.start()
        t.join()
        resultList.append(t.getReturn())
    # endtime = datetime.datetime.now()
    for one in resultList:
        # print(one.desc,one.retCode,one.name,one.url,one.retContent,one.expectCode,one.expectContent)
        flag, res = resultContain(one.retContent, one.expectContent)
        tempList=[]
        if flag:
            one.result = res
            # print(one.result,one.desc,one.retCode,one.name,one.url,one.retContent,one.retCode,one.retContent,one.expectCode,one.expectContent)
            print(one.desc,one.result, one.retCode, one.name, one.url,one.retContent.decode('utf-8'))
            tempList.append(one.desc)
            tempList.append(one.result)
            tempList.append(str(one.retCode))
            tempList.append(one.name)
            tempList.append(one.url)
            tempList.append(one.retContent.decode('utf-8'))
        else:
            one.result = res
            print(one.desc,one.result, one.retCode, one.name, one.url,one.retContent.decode('utf-8'))
            tempList.append(one.desc)
            tempList.append(one.result)
            tempList.append(str(one.retCode))
            tempList.append(one.name)
            tempList.append(one.url)
            tempList.append(one.retContent.decode('utf-8'))
        returnList.append(tempList)
    return returnList
    # print((endtime - starttime).seconds)

def eventExecuter(items):
    # starttime = datetime.datetime.now()
    # items = getParams("i01_interfaceDef.ini")

    taskList=[]
    returnList=[]
    for one in items:
        taskList.append(asyncio.ensure_future(gevnetSender(one)))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(taskList))
    # endtime = datetime.datetime.now()

    for one in taskList:
        # print(one.result().desc,one.result().retCode,one.result().name,one.result().url,one.result().retContent,one.result().expectCode,one.result().expectContent)
        tempList=[]
        flag, res = resultContain(one.result().retContent, one.result().expectContent)
        if flag:
            one.result().result = res
            # print(one.result,one.desc,one.retCode,one.name,one.url,one.retContent,one.retCode,one.retContent,one.expectCode,one.expectContent)
            print(one.result().desc,one.result().result, one.result().retCode, one.result().name, one.result().params,one.result().url,one.result().retContent.decode('utf-8'))
            tempList.append(one.result().desc)
            tempList.append(one.result().result)
            tempList.append(str(one.result().retCode))
            tempList.append(one.result().name)
            tempList.append(one.result().params)
            tempList.append(one.result().url)
            tempList.append(one.result().retContent.decode('utf-8'))
        else:
            one.result().result = res
            print(one.result().desc,one.result().result, one.result().retCode, one.result().name, one.result().params,one.result().url,one.result().retContent.decode('utf-8'))
            tempList.append(one.result().desc)
            tempList.append(one.result().result)
            tempList.append(str(one.result().retCode))
            tempList.append(one.result().name)
            tempList.append(one.result().params)
            tempList.append(one.result().url)
            tempList.append(one.result().retContent.decode('utf-8'))
        returnList.append(tempList)
    # print((endtime - starttime).seconds)
    return returnList


def eventExecute2():
    items = getParams("i01_interfaceDef.ini")

    taskList=[]
    for one in items:
        taskList.append(asyncio.ensure_future(gevnetSender(one)))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(taskList))

async def start(executor):
    await asyncio.get_event_loop().run_in_executor(executor,eventExecute2)




#验证对比函数
# if __name__=='__main__':
#     r = '''</title></head>\r\n<body bgcolor="white">\r\n<center><h1>404 Not Found</h1></center>\r\n<hr><center>nginx/1.14.0</center>\r\n</body>\r\n</html>'''
#     e = '404'
#     print(resultContain(r,e))


# 单进程
# 3000个15秒
# singleExecuter()
# if __name__=='__main__':
#     singleExecuter()

#多进程
# #3000个16秒
# #51888个242秒
# # multiExcuteor()
# if __name__=='__main__':
#     multiExcuter()

#协程
#3000个14秒
#51888个233秒
# eventExecute()
if __name__=='__main__':
    eventExecuter()


# 此作为多进程+多协程的组合，但是没有返回值
# if __name__=='__main__':
#     starttime = datetime.datetime.now()
#     exec=ProcessPoolExecutor()
#     asyncio.get_event_loop().run_until_complete(start(exec))
#     endtime = datetime.datetime.now()
#     print((endtime - starttime).seconds)


# if __name__=='__main__':
#     a,b=singleSender('POST','http://172.30.200.3:8081/ds-web-jt/allPoint/getAspList?soucePointId=&sourcePointName=&sourcePointDesc=0&sourcePointState=2&omcId=1&currentPage=1&itemsPerPage=10&syncState=&searchState=0&mapperState=9&from_time=&to_time=')
#     print(b.decode('utf-8'))