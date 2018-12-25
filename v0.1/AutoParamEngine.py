import itertools
from random import randint
import numpy
from copy import deepcopy
import collections

class ParamGener:
    '''参数生成方式'''
    def __init__(self,*args):
        '''参数列表，2维数组'''
        self.inputParam=args
    def allConbine(self):
        '''对列表进行笛卡儿积，并按照一个列表返回'''
        all = []
        for i in itertools.product(*self.inputParam):
            all.append(i)
        return all

    # def eachChoice(self):
    #     all=self.allConbine()
    #
    #     for one in all:
    #         print(one)
    #     print('######################')
    #
    #     retList=[]
    #     retList.append(all[0])
    #     for one in all:
    #         for index,item in enumerate(one):
    #             if retList[index]==item:
    #                 break
    #             else:
    #                 retList.append(one)
    #     retList=set(retList)
    #     print(len(retList))
    #     return retList

    def pairWiseMore(self):
        #获取正交参数对
        all=self.allConbine()
        pairList=[]

        #根据正交参数对，获取配对算法全部的配对参数对
        for one in all:
            temp=[]
            for item in itertools.combinations(one,2):
                temp.append(item)
            pairList.append(temp)

        compareList=deepcopy(pairList)
        # for one in pairList:
        #     print(one)
        #配对参数对筛选
        remainsList=[]
        returnList=[]

        for line, pairGroups in enumerate(pairList):
            flag=[0]*len(pairGroups)
            for col in range(0, len(pairGroups)):
                for row in range(0,len(compareList)):
                    if pairList[line]!=compareList[row] and pairGroups[col]==compareList[row][col]:
                        flag[col]=1
                        break
                    else:
                        flag[col]=0

            # print(flag)
            if 0 not in flag:
                # deleteList.append(pairGroups)
            # count=collections.Counter(flag)[1]
            # flag=[]
            # if count>=5:
                compareList.remove(pairGroups)
            else:
                remainsList.append(pairGroups)

        #合并配对参数的列表
        temp=[]
        for items in remainsList:
            for one in items:
                for item in one:
                    if item not in temp:
                        temp.append(item)
            # returnList.append(sorted(list(set(temp.lstrip(",").split(",")))))
            returnList.append(temp)
            temp=[]
        return returnList

    def pairWiseLess(self):
        #获取正交参数对
        all=self.allConbine()
        pairList=[]

        #根据正交参数对，获取配对算法全部的配对参数对
        for one in all:
            temp=[]
            for item in itertools.combinations(one,2):
                temp.append(item)
            pairList.append(temp)
        compareList=deepcopy(pairList)
        # for one in compareList:
        #     print(one)
        #配对参数对筛选
        remainsList=[]
        returnList=[]

        for line, pairGroups in enumerate(pairList):
            flag=[0]*len(pairGroups)
            for col in range(0, len(pairGroups)):
                for row in range(0,len(compareList)):
                    if pairList[line]!=compareList[row] and pairGroups[col]==compareList[row][col]:
                        flag[col]=1
                        break
                    else:
                        flag[col]=0
            print(flag)
            if flag.count(1)>=len(pairGroups)-1:
                # deleteList.append(pairGroups)
                compareList.remove(pairGroups)
            else:
                remainsList.append(pairGroups)

        #合并配对参数的列表
        temp=[]
        for items in remainsList:
            for one in items:
                for item in one:
                    if item not in temp:
                        temp.append(item)
            # returnList.append(sorted(list(set(temp.lstrip(",").split(",")))))
            returnList.append(temp)
            temp=[]
        return returnList

    def antiRandom(self,n):
        '''反随机，找边界'''
        all = self.allConbine()
        start=0
        end=len(all)-1
        resList=[]
        resList.append(all[0])
        resList.append(all[end])

        middle = (start + end) // 2
        while len(resList)<n:
            m2=middle//2
            counter=2
            while m2<end and len(resList)<n:
                if all[m2] not in resList:
                    resList.append(all[m2])
                m2=counter*(middle//2)
                counter=counter+1
            middle=middle//2
        return resList

    def randomChoice(self,n):
        '''随机获取任意个数个参数列表'''
        all=self.allConbine()
        all_len=len(all)-1
        retList = []

        if n<all_len:
            for i in range(0,n):
                retList.append(all[randint(0,all_len)])
        else:
            print("all got params larger than length of all conbine")
        return retList

if __name__=="__main__":
    # testList=[['winxp','win7','win10','win2003'],['chrome','firefox','ie','opera'],['64bits',"32bits"]]
    # testList=[['M','O','P'],['W','L','I'],['C','E','K'],[1,2,3],['Yes','No'],['666','']]
    # testList = [['firefox', 'ie', 'opera'], ['websphere', 'apache', '.net'], ['mastercard', 'visa', 'unionpay'], ['db2', 'oracle', 'access']]
    # testList=[['M','O','P','i','2'],['W','L','I','O','U'],['M','E'],['L','P']]
    testList=[['M','O','P','i','2','M','O','P',4],['M','O','P','i','2','M','O','P',4],['M','O','P','i','2','M','O','P',4],['M','O','P','i','2','M','O','P',4],
              ['M', 'O', 'P', 'i', '2', 'M', 'O', 'P', 4],['M','O','P','i','2','M','O','P',4],['M','O','P','i','2','M','O','P',4],['M','O','P','i','2','M','O','P',4],['M','O','P','i','2','M','O','P',4]
              ,['M','O','P','i','2','M','O','P',4],['M','O','P','i','2','M','O','P',4],['M','O','P','i','2','M','O','P',4],['M','O','P','i','2','M','O','P',4],['M','O','P','i','2','M','O','P',4]
              ,['M','O','P','i','2','M','O','P',4]]
    p=ParamGener(*testList)
    # all=p.allConbine()
    # anti=p.antiRandom(6)
    # rand=p.randomChoice(4)
    # each=p.eachChoice()
    pair=p.allConbine()

    # p=itertools.count()

    print("#######################")
    # for a in pair:
    #     print(a)
    # print(len(pair))