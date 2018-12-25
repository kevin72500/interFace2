from random import randint
def largerOrSmall(practiceNum=10):
    for i in range(1,practiceNum):
        a=randint(1,100)
        b=randint(1,100)
        allowList=['<','>','=']
        oper=input("欧昊然：来挑战下，看看应该输入的是：大于>, 小于<, 还是等于= 符号\n {} ()  {}".format(a,b))
        if oper not in allowList:
            print('你输入的不是 大于>, 小于<, 等于= 符号')
        else:
            if a>b:
                if oper=='>':
                    print("回答正确，你太棒了 ^ _ ^")
                else:
                    print("回答错误，下次加油哦  - _ -")
            elif a<b:
                if oper=='<':
                    print("回答正确，你太棒了 ^ _ ^")
                else:
                    print("回答错误，下次加油哦  - _ -")
            elif a==b:
                if oper=='=':
                    print("回答正确，你太棒了 ^ _ ^")
                else:
                    print("回答错误，下次加油哦  - _ -")
        print('='*100)


def getSepNum():
    num=12345
    sepNum=[]
    while len(str(num))!=1:
        sepNum.append(num%10)
        num=num//10
    else:
        sepNum.append(num)
    print(sepNum)
getSepNum()