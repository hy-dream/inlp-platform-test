import pytest
import requests
import json
import os
import logging as log
import configparser

log.basicConfig(level=log.DEBUG,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                handlers={log.FileHandler(filename='test.log', mode='a', encoding='utf-8')})

parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

cp=configparser.RawConfigParser()
confPath = os.path.join(parent, "data","nlp.conf")
cp.read(confPath)
baseURL=cp.get("db","baseurl")
myurl=baseURL+'summary'
myheaders={'content-type': 'application/json'}

def send_summary(myparms,datalist):
    mydata = json.dumps(datalist)

    response = requests.post(url=myurl, headers=myheaders, params=myparms,data=mydata.encode('utf-8'))

    message = json.loads(response.text)
    return  message

def readcontent(filename):
    resourcePath = os.path.join(parent, "data", "summary", "input",filename)
    f = open(resourcePath, mode='r', encoding='utf-8')
    content = f.readlines()
    f.flush()
    f.close()
    content2="".join(content)
    return content2


def writeresult(filename,content,summary):
    resultPath = os.path.join(parent, "data", "summary", "output", filename)
    f = open(resultPath, mode='a', encoding='utf-8')
    f.writelines('*' * 100 + "原文本是" + '*' * 100 + '\n')
    f.writelines(content)
    f.writelines('\n')
    f.flush()
    f.writelines('*' * 100 + "摘要如下" + '*' * 100 + '\n')
    f.writelines(summary)
    f.writelines('\n')
    f.flush()
    f.close()

@pytest.mark.regression
def test_summary_percentage_default():

    #smaple  http://172.18.82.251:1240/summary?percentage=0.3&charLimit=1000

    charLimit=6000
    myparms={"charLimit":charLimit}
    content=readcontent( "test1.txt")
    datalist=[{"title":"","content":content}]
    summary=send_summary(myparms,datalist)
    writeresult("result.txt",content,summary[0])

@pytest.mark.regression
@pytest.mark.parametrize("percentage", [
 ("0"),
 ("0.1"),
 ("0.5"),
 ("0.9"),
  (1)
])
def test_summary_percentage_valid(percentage):
    title = ''
    # url ,port读配置
    charLimit = 1000
    myparms = {"percentage":percentage,"charLimit": charLimit}
    content = readcontent("percentage_valid.txt")
    datalist = [{"title": "高山榕树望初心", "content": content}]
    summary=send_summary(myparms,datalist)

    writeresult("percentage_valid.txt",content,summary[0])

@pytest.mark.parametrize("percentage", [
 ("-1"),
 ("1.1"),
 ("2"),
    ("abc"),
    ("")
])
@pytest.mark.skip(reason="skip haha")
def test_summary_percentage_not_valid(percentage):

    charLimit = 1000
    myparms = {"percentage": percentage, "charLimit": charLimit}
    content = readcontent("percentage_valid.txt")
    datalist = [{"title": "高山榕树望初心", "content": content}]

    summary = send_summary(myparms,datalist)

    writeresult("percentage_not_valid.txt", content, summary[0])


@pytest.mark.regression
def test_summary_charlimit__default():

    myparms = {"percentage": 0.5}
    content = readcontent("test1.txt")
    datalist = [{"title": "", "content": content}]
    summary = send_summary(myparms, datalist)
    writeresult("charlimit__default.txt", content, summary[0])


@pytest.mark.regression
@pytest.mark.parametrize("charLimit", [
 (50),
 (800),
 (3000)
])
def test_summary_charlimit__valid(charLimit):
    myparms = {"percentage": 0.5,"charLimit":charLimit}
    content = readcontent("charlimit_valid.txt")
    datalist = [{"title": "全球气候变暖", "content": content}]
    summary = send_summary(myparms, datalist)

    writeresult("charlimit__valid.txt", content, summary[0])

@pytest.mark.parametrize("charLimit", [
 (-1),
 (100.89),
 ("")
])
@pytest.mark.skip(reason="jajajja")
def test_summary_charlimit__not_valid(charLimit):
    myparms = {"percentage": 0.5, "charLimit": charLimit}
    content = readcontent("charlimit_valid.txt")
    datalist = [{"title": "全球气候变暖", "content": content}]
    summary = send_summary(myparms, datalist)

    writeresult("charlimit__not_valid.txt", content, summary[0])


@pytest.mark.regression
def test_summary_multi_article():
    log.debug('-----调试信息[debug]---test_summary_multi_article--')
    myparms = {"percentage": 0.3, "charLimit": 600}
    datalist = []
    resourcePath = os.path.join(parent, "data", "summary", "input")
    for file in os.listdir(resourcePath):
        content=readcontent(file)
        datalist.append({"title":"","content":content})

    message = send_summary(myparms, datalist)
    i=0
    for m in message:
        writeresult("multi_article.txt",datalist[i].get("content"),m)
        i=i+1

@pytest.mark.regression
@pytest.mark.parametrize("datalist", [
 ([{},{}]),
 ([{"title":"","content":"这初心正与高山榕那坚韧顽强、奋发向上的精神相呼应。"},{"content":"这初心正与高山榕那坚韧顽强、奋发向上的精神相呼应。"}]),
 ([{"title":"","content":"这初心正与高山榕那坚韧顽强、奋发向上的精神相呼应。"},{"title":"这初心正"}]),
    ([{"content":"这初心"},{"title":"","content":""}])
])
def test_summary_multi_article_miss_some_field(datalist):
    log.getLogger("test_summary_multi_article_miss_some_field")
    log.debug('-----调试信息[debug]---test_summary_multi_article_miss_some_field--')
    myparms = {"percentage": 0.3, "charLimit": 600}
    message = send_summary(myparms, datalist)
    assert message.startswith("article")
    log.debug('-----调试信息[debug]----'+message)


