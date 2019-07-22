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
myurl = baseURL + 'splitSentence'
myheaders = {'content-type': 'application/json'}

def readcontent(filename):
    resourcePath = os.path.join(parent, "data", "splitsentence", "input",filename)
    f = open(resourcePath, mode='r', encoding='utf-8')
    content = f.readlines()
    f.flush()
    f.close()
    content2="".join(content)
    return content2


def writeresult(filename,content,summary):
    resultPath = os.path.join(parent, "data", "splitsentence", "output", filename)
    f = open(resultPath, mode='a', encoding='utf-8')
    f.writelines('*' * 100 + "原文本是" + '*' * 100 + '\n')
    f.writelines(content)
    f.writelines('\n')
    f.flush()
    f.writelines('*' * 100 + "分句如下" + '*' * 100 + '\n')
    for line in summary:
        f.writelines(line)
        f.writelines('\n')
        f.flush()
    f.close()

def send_sentence(datalist):
    mydata = json.dumps(datalist)

    response = requests.post(url=myurl, headers=myheaders, data=mydata.encode('utf-8'))

    message = json.loads(response.text)
    return  message


@pytest.mark.regression
@pytest.mark.parametrize("title,file", [
 ("衡水中学:有学校冒用衡中名义","test1.txt"),
("上半年GDP增长6.3%如何解读？统计局给出五句概括", "test2.txt"),
    ("动真格！北京将试点生活垃圾“不分类、不收运”", "test3.txt")
    ])
def test_splitsentence_title_not_null(title,file):
    content = readcontent(file)
    datalist = [{"title":title,"content": content}]

    message = send_sentence(datalist)
    print(message[0])
    writeresult(file,content,message[0])


@pytest.mark.regression
@pytest.mark.parametrize("file", [
 ("微博1"),
 ("微博2"),
 ("微博3"),
 ("微博4"),
  ("豆瓣1"),
("豆瓣2")
    ])
def test_splitsentence_title_is_null(file):
    content = readcontent(file)
    datalist = [{"title":"","content": content}]
    message = send_sentence(datalist)
    writeresult(file,content,message[0])


@pytest.mark.regression
def test_splitsentence_multi_article():
    datalist = []
    resourcePath = os.path.join(parent, "data", "splitsentence", "input")
    for file in os.listdir(resourcePath):
        content=readcontent(file)
        datalist.append({"title":"","content":content})

    message = send_sentence(datalist)
    i = 0
    for m in message:
        writeresult("multi_article.txt", datalist[i].get("content"), m)
        i = i + 1

@pytest.mark.regression
@pytest.mark.parametrize("datalist", [
 ([{},{}]),
 ([{"title":"","content":"这初心正与高山榕那坚韧顽强、奋发向上的精神相呼应。习近平亲手种下了一棵胸径约15厘米、高2米多的直干高山榕。"},{"content":"这初心正与高山榕那坚韧顽强、奋发向上的精神相呼应。"}]),
 ([{"title":"","content":"这初心正与高山榕那坚韧顽强、奋发向上的精神相呼应。"},{"title":"习近平亲手种下了一棵胸径约15厘米、高2米多的直干高山榕。"}]),
    ([{"content":"这初心"},{"title":"","content":""}])
])
def test_splitsentence_multi_article_miss_some_field(datalist):
    message = send_sentence(datalist)
    #print(message+"000")
    assert message.startswith("article")

#test_splitsentence_title_is_null("黄帝内经")