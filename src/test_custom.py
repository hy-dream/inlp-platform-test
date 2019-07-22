import pytest
import requests
import json
import  os,shutil
import logging as log
import random
import configparser

log.basicConfig(level=log.DEBUG,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                handlers={log.FileHandler(filename='test.log', mode='a', encoding='utf-8')})

parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))





cp=configparser.RawConfigParser()
cp.read("nlp.conf")
baseURL=cp.get("db","baseURL")
myurl = baseURL + 'custom'
myheaders = {'content-type': 'application/json'}

missionList=["splitSentence","splitWord","posTag","ner","wordWeight","wordWeightMap","keyWord","vectorKeyWord","keyPhrase","keyExpression","summary","mlableClassifier","sentiment"]

def readcontent(filename):
    resourcePath = os.path.join(parent, "data", "custom", "input",filename)
    f = open(resourcePath, mode='r', encoding='utf-8')
    content = f.readlines()
    f.flush()
    f.close()
    content2="".join(content)
    return content2


def writecontent(filename,content,message):
    resultPath = os.path.join(parent, "data", "custom", "output", filename)
    f = open(resultPath, mode='a', encoding='utf-8')
    f.writelines('*' * 100 + "原文本是" + '*' * 100 + '\n')
    f.writelines(content)
    f.writelines('\n')
    f.flush()
    f.writelines('*' * 100 + "分析内容如下" + '*' * 100 + '\n')
    for k,v in message.items():
        f.writelines(k)
        f.writelines(str(v))
        f.writelines("\n")
        f.flush()

    f.close()

def send_custom(dataList):
    # articles=[{"title":"","content":"一个女性朋友跟我说过这样一段话：不介意孤单，已经做好一个人终老的准备，我生来 并没有义务一定要成为谁的妻子或者母亲，人生中结婚和生子不是必要选项，生而为人在这个社会已经很辛苦，只愿父母安康。"},{"title":"","content":"哇塞，好厉害，我只会简单的给狗狗做个小肚兜，缝沙发布，桌布什么的，简单窗帘这些，不过裁剪。你做得太棒了吧。"}]
    # missionList = ['keyWord', 'keyExpression', 'summary', 'mlableClassifier', 'ner', 'wordWeightMap',
    #                'sentiment', 'splitWord']
    # parametersList = [{}, {"s":1}, {"percentage":0.5}, {}, {}, {}, {'domain1': 'content'},{}]

    mydata = json.dumps(dataList)

    response = requests.post(url=myurl, headers=myheaders, data=mydata.encode('utf-8'))

    message = json.loads(response.text)
    return message

@pytest.mark.regression
def test_custom_muilt_articles():
    articles = []
    parametersList=[]
    resourcePath = os.path.join(parent, "data", "custom", "input")
    random.shuffle(missionList)
    for file in os.listdir(resourcePath):
        content = readcontent(file)
        articles.append({"title": "", "content": content})

    for item in missionList:
        if item=="summary":
            parametersList.append( {"percentage":0.5,"charLimit": 1500})
        elif item=="sentiment":
            parametersList.append({"domain": "comment"})
        else:
            parametersList.append({})

    dataList = {'missionList': missionList, 'parametersList': parametersList, 'data': articles}
    message=send_custom(dataList)
    i=0
    for item in message:
        assert len(item) ==len(missionList)
        writecontent("nuilt_result", articles[i].get("content"),item)
        i=i+1



# test_custom_muilt_articles()