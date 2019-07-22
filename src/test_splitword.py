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
cp.read("nlp.conf")
baseURL=cp.get("db","baseURL")
myurl = baseURL + 'splitWord'
myheaders = {'content-type': 'application/json'}

def readcontent(filename):
    resourcePath = os.path.join(parent, "data", "splitword", "input",filename)
    f = open(resourcePath, mode='r', encoding='utf-8')
    content = f.readlines()
    f.flush()
    f.close()
    content2="".join(content)
    return content2


def writeresult(filename,content,summary):
    resultPath = os.path.join(parent, "data", "splitword", "output", filename)
    f = open(resultPath, mode='a', encoding='utf-8')
    f.writelines('*' * 100 + "原文本是" + '*' * 100 + '\n')
    f.writelines(content)
    f.writelines('\n')
    f.flush()
    f.writelines('*' * 100 + "分词如下" + '*' * 100 + '\n')
    for line in summary:
        f.writelines(line)
        f.writelines('\n')
        f.flush()
    f.close()




# ("加强党建工作 习近平希望培养这样的人","test1.txt"),
# ("坐高铁=照X光?专家:中国高铁辐射严重属无稽之谈","test3.txt")
@pytest.mark.regression
@pytest.mark.parametrize("title,file", [
 ("我是标题","test2.txt")
    ])
def test_splitword_title_not_null(title,file):
    content = readcontent(file)
    datalist = [{"title":title,"content": content}]
    message=send_splitword(datalist)
    print(message[0])
    writeresult(file,content,message[0])
    return message[0]


@pytest.mark.regression
@pytest.mark.parametrize("file", [
 ("test1.txt")
    ])
def test_splitword_title_is_null(file):
    content = readcontent(file)
    datalist = [{"title":"","content": content}]
    message=send_splitword(datalist)
    print(message[0])
    writeresult(file,content,message[0])
    return message[0]


@pytest.mark.regression
def test_splitword_multi_article():
    datalist = []
    resourcePath = os.path.join(parent, "data", "splitword", "input")
    for file in os.listdir(resourcePath):
        content=readcontent(file)
        datalist.append({"title":"","content":content})

    message=send_splitword(datalist)
    i = 0
    for m in message:
        writeresult("multi_article.txt", datalist[i].get("content"), m)
        i = i + 1

def send_splitword(datalist):
    mydata = json.dumps(datalist)

    response = requests.post(url=myurl, headers=myheaders, data=mydata.encode('utf-8'))

    message = json.loads(response.text)
    return message

@pytest.mark.regression
@pytest.mark.parametrize("datalist", [
 ([{},{}]),
 ([{"title":"","content":"这初心正与高山榕那坚韧顽强、奋发向上的精神相呼应。"},{"content":"这初心正与高山榕那坚韧顽强、奋发向上的精神相呼应。"}]),
 ([{"title":"","content":"这初心正与高山榕那坚韧顽强、奋发向上的精神相呼应。"},{"title":"这初心正"}]),
    ([{"content":"这初心"},{"title":"","content":""}])
])
def test_splitword_multi_article_miss_some_field(datalist):
    message=send_splitword(datalist)
    #print(message+"000")
    assert message.startswith("article")

