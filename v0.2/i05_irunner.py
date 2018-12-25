from i02_initReader_general import getParams
from i02_initToJson import getParams as getParamsj
from i03_requestSenderWithJson import eventExecuter,multiExcuter,singleExecuter
from i04_htmlGenerator import reportGenerator

items=getParams("i01_interfaceDef.ini",mode="all")
resultList=eventExecuter(items)
reportGenerator(resultList)
