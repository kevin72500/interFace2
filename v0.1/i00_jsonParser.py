import json
import requests
import hashlib
from  datetime import datetime
from i06_util_write2Excel import tuple2dict,getParams

targetServerHost="192.168.110.25"
targetServerPort="9111"
def jsonParser(projectId="186",yapiHost="192.168.110.8",yapiPort='3000',iniFileName='i00_interfaceOut.ini'):
    head='''{'Accept': 'application/json, text/plain, */*','Accept-Encoding': 'gzip, deflate','Connection': 'keep-alive', 'Content-Type': 'application/json;charset=UTF-8', 'Cookie': 'sidebar_collapsed=false', 'Origin': 'http://192.168.105.236:3000','Referer': 'http://192.168.105.236:3000/login'} '''

    data='''
    {"email":"kevin@mycompany.com","password":"myPassword"}
    '''
    hostAndPort="http://{}:{}".format(yapiHost,yapiPort)

    s=requests.session()
    ret=s.post(url="http://"+yapiHost+":"+yapiPort+"/api/user/login",
               headers=eval(head),
               data=data)
    retCook=ret.cookies
    ret=s.get(url="http://"+yapiHost+":"+yapiPort+"/api/interface/list_menu?project_id={}".format(projectId),cookies=retCook)
    # print(ret.content.decode('utf-8'))
    # print(ret.status_code)
    p=json.loads(ret.content.decode('utf-8'))
    now=datetime.now().strftime('%y-%m-%d %H:%M:%S')
    comments="#"+now+"\n"+''';#如果包含%字符在值里面，需要用%%进行转义
    ;#数字不需要引号，字符串用引号
    ;#参数用括号嵌套，如果只有一个参数，需要用元祖表示方式（'para1',），记得加上逗号
    ;#如果是URL的后端加参数用param=p(value,)
    ;#如果是json加参数用param=j(value,)'''
    i=1
    allData = []
    with open(iniFileName,'w',encoding='utf-8') as f:
        f.writelines(comments+"\n")
        for one in p['data']:
            for item in one['list']:
                infoDict={}
                Uparam=[]
                Jparam=[]
                f.writelines("[{}]\n".format(i))
                f.writelines("name={}\n".format(item['title']))
                f.writelines("method={}\n".format(item['method']))
                f.writelines("desc={}\n".format(item['title']))
                f.writelines("url={}\n".format(item['path']))
                f.writelines("host=http://{}:{}\n".format(targetServerHost,targetServerPort))

                # f.writelines("url={}\n".format("http://192.168.105.236:3000/api/interface/get?id="+str(item['_id'])))
                # print("http://192.168.105.236:3000/api/interface/get?id={}    --{}:{}:{}".format(item['_id'],item['title'],item['method'],item['path']))
                sub_resp=s.get(url="http://"+yapiHost+":"+yapiPort+"/api/interface/get?id="+str(item['_id']))
                resp=json.loads(sub_resp.content)
                # print(resp)
                headers={}
                #写入header
                # print(resp['data'])
                for one in resp['data']['req_headers']:
                    headers[one['name']]=one['value']
                f.writelines("headers={}\n".format(headers))
                f.writelines("expectCode=200\n")
                f.writelines("expectContent=\n")

                infoDict['name']=item['title']
                infoDict['method']=item['method']
                infoDict['desc']=item['title']
                infoDict['url']=item['path']
                infoDict['host']=hostAndPort
                infoDict['headers']=headers
                infoDict['expectCode']='200'
                infoDict['expectContent']=""
                try:
                    # 写入url参数,提交参数
                    for one in resp['data']['req_query']:
                        f.writelines("{}=p('{}=>',)\n".format(one['name'], one['desc']))
                        Uparam.append("{}={}".format(one['name'], one['desc']))
                    # 写入url参数，URL中的参数
                    for one in resp['data']['req_params']:
                        if one['name'] not in item['path']:
                            f.writelines("{}=p('{}=>',)\n".format(one['name'],one['desc']))
                            Uparam.append("{}={}".format(one['name'], one['desc']))
                    # f.writelines("params=p({})\n".format(resp['data']['req_params']))

                    infoDict['uparam']=Uparam
                    #写入json参数

                    # print(resp['data']['req_body_other'])
                    properDict=eval(resp['data']['req_body_other'])['properties']
                    # print(properDict)
                    for key in properDict:
                        if 'maxLength' in properDict[key] and 'type' in properDict[key]:
                            f.writelines("{}=j('{}=>{}',)\n".format(key,properDict[key]['type'],properDict[key]['maxLength']))
                            Jparam.append("{}='{}=>{}'".format(key,properDict[key]['type'],properDict[key]['maxLength']))
                        elif  'type' in properDict[key]:
                            f.writelines("{}=j('{}',)\n".format(key, properDict[key]['type']))
                            Jparam.append("{}='{}'".format(key, properDict[key]['type']))
                        else:
                            f.writelines("{}=j(,)\n".format(key))
                            Jparam.append("{}=".format(key))
                    infoDict['jparam']=Jparam
                except Exception as e:
                    # print("Not key: "+str(e))
                    pass
                f.writelines("ExResponse={}\n".format(resp['data']['res_body']))
                try:
                    infoDict['ExpectResponse']=eval(resp['data']['res_body'])['properties']
                except Exception as e:
                    infoDict['ExpectResponse'] = {}
                i=i+1
                allData.append(infoDict)
    return allData


from xlwt import *
def write2Excel(projectId,excelName='case'):
    res = jsonParser(projectId=projectId)
    file=Workbook(encoding='utf-8')
    # now=datetime.now().strftime('%y%m%d%H%M%S')
    sheet=file.add_sheet('InterfaceCase')
    sheet.write(0, 0, '接口名称')
    sheet.write(0, 1, '用例编号')
    sheet.write(0, 2, '入参场景')
    sheet.write(0, 3, '场景')
    sheet.write(0, 4, '优先级')
    sheet.write(0, 5, '预置条件')
    sheet.write(0, 6, '接口方法')
    sheet.write(0, 7, '请求地址')
    sheet.write(0, 8, 'URL')
    sheet.write(0, 9, 'Json参数示例')
    sheet.write(0, 10, '请求头')
    sheet.write(0, 11, '期望http返回码')
    sheet.write(0, 12, '期望返回值')
    sheet.write(0, 13, '返回示例')
    sheet.write(0, 14, 'URL参数')
    sheet.write(0, 15, 'Json参数解释')


    index=1
    for item in res:
        # print(item)
        # print(index)
        # sheet.write(,sec.name,sec.method,sec.host,sec.url,sec.headers,sec.params,sec.expectCode,sec.expectContent)
        sheet.write(index, 0, item['name'])
        sheet.write(index, 6, item['method'])
        sheet.write(index, 7, item['host'])
        sheet.write(index, 8, item['url'])
        sheet.write(index, 9, 'jdata')
        sheet.write(index, 10, str(item['headers']))
        sheet.write(index, 11, item['expectCode'])
        if len(item['ExpectResponse'])>0:
            sheet.write(index, 12, list(item['ExpectResponse'].keys())[0])
        sheet.write(index, 13, str(item['ExpectResponse']))
        if 'uparam' in item.keys():
            upLen=len(item['uparam'])
            if upLen>=1:
                for i,v in enumerate(item['uparam']):
                    sheet.write(index+i, 14, v)
        if 'jparam' in item.keys():
            jpLen = len(item['jparam'])
            if jpLen >= 1:
                for i,v in enumerate(item['jparam']):
                    sheet.write(index+i, 15, v)

        if upLen>jpLen:
            index=index+upLen
        else:
            index=index+jpLen
        # print(index)
        # print('&'*100)
        # sheet.write(index, 9,item['ExpectResponse'].keys())
        # print(type(item['ExpectResponse']))

    file.save(excelName+".xlsx")


if __name__=='__main__':
    write2Excel(projectId=243,excelName='helpCenter')




