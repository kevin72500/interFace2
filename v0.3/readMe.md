V0.1介绍
1.文件模块介绍：
AutoParamEngine.py：主要用于把列出的参数进行配对，主要有4中配对方式，全配对，组合配对，随机配对，反随机配对四种。
i00_interfaceOut.ini：此文件是由i00_jsonParser.py生成，用ini文件的形式描述了对应yapi上项目的接口信息，方便测试人员对相应的接口进行复制修改，进行测试。
i00_jsonParser.py：主要用于根据项目ID号码，解析yapi上项目的接口信息，并生成I00_interfaceOut.ini和case.xlsx两个接口定义文件。
i01_interfaceDef.ini：此文件主要用于存放根据i00_interfaceOut.ini修改后的接口定义信息，用于实际的接口功能测试。
i02_initReader_general.py：此模块用于生成根据参数配对后，产生的请求对象队列。
i03_requestSenderWithJson.py：此模块用多协程的方式，发送请求队列中的请求，并存储请求发送后的结果。
i04_htmlGenerator.py：此模块用于把，请求返回回来的结果，利用html方式生成报告。
i05_irunner.py：此模块用于运行接口测试，生成报告，可以利用参数形式，定义请求参数生成方式。
i06_util_write2Excel.py：此模块用于把已经发送过的请求及其参数，写入excel用例当中，为后续自动化测试提供参考。


添加i02_initReader_general.py，可以生成jmx jmeter文件 2018/12/18

2.使用方式：
安装python对应的模块。
查找需要测试的yapi项目编号，运行i00_jsonParser.py，生成i00_interfaceOut.ini接口定义文件。
接口功能测试时，将i00_interfaceOut.ini接口定义文件中的接口，按照测试顺序，复制粘贴到i01_interfaceDef.ini文件中，并修改需要配对的参数，运行i05_irunner.py模块。（如果参数数量过对，可以传入配对过滤方式，参数少时，不建议使用此模式，配对比较耗时）
如果需要将测试用例提供给自动化小组，可以运行i06_util_write2Excel.py，会生成一个case1.xlsx的文件，包含了接口的定义和一个参数示例。

