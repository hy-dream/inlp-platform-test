import pytest
import requests
import json
import  os,shutil
import logging as log


log.basicConfig(level=log.DEBUG,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                handlers={log.FileHandler(filename='test.log', mode='a', encoding='utf-8')})

parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

baseURL = 'http://172.18.82.251:1240/'
myurl = baseURL + 'ner'
myheaders = {'content-type': 'application/json'}

def readcontent(filename):
    resourcePath = os.path.join(parent, "data", "ner", "input",filename)
    f = open(resourcePath, mode='r', encoding='utf-8')
    content = f.readlines()
    f.flush()
    f.close()
    content2="".join(content)
    return content2

def send_ner(datalist):
    mydata = json.dumps(datalist)

    response = requests.post(url=myurl, headers=myheaders, data=mydata.encode('utf-8'))

    message = json.loads(response.text)
    return  message


def writeresult(filename,content,message):
    resultPath = os.path.join(parent, "data", "ner", "output", filename)
    f = open(resultPath, mode='a', encoding='utf-8')
    f.writelines('*' * 100 + "原文本是" + '*' * 100 + '\n')
    f.writelines(content)
    f.writelines('\n')
    f.flush()
    f.writelines('*' * 100 + "实体内容如下" + '*' * 100 + '\n')
    for m in message:
        ner=str(m)
        f.writelines(ner)
        f.writelines('\n')
        f.flush()
    f.close()


@pytest.mark.regression
@pytest.mark.parametrize("title,file", [
 ("斯里兰卡政治危机再度升级 总统宣布解散议会","bad_ner_2"),
    ])
def test_ner_title_not_null(title,file):
    content = readcontent(file)
    datalist = [{"title":title,"content": content}]

    message=send_ner(datalist)
    writeresult(file,content,message[0])


@pytest.mark.regression
@pytest.mark.parametrize("file", [
 ("right_ner")
    ])
def test_ner_title_is_null(file):
    content = readcontent(file)
    datalist = [{"title":"","content": content}]
    message = send_ner(datalist)
    writeresult(file,content,message[0])


@pytest.mark.regression
def test_ner_multi_article():
    datalist = []
    resourcePath = os.path.join(parent, "data", "ner", "input")
    for file in os.listdir(resourcePath):
        content=readcontent(file)
        datalist.append({"title":"","content":content})

    message = send_ner(datalist)
    i = 0
    for m in message:
        writeresult("multi_article.txt", datalist[i].get("content"), m)
        i = i + 1

