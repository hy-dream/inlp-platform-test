import pytest
import requests
import json
import  os,shutil
import logging as log
import test_splitword
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
myurl = baseURL + 'posTag'
myheaders = {'content-type': 'application/json'}

def readcontent(filename):
    resourcePath = os.path.join(parent, "data", "postag", "input",filename)
    f = open(resourcePath, mode='r', encoding='utf-8')
    content = f.readlines()
    f.flush()
    f.close()
    content2="".join(content)
    return content2


def writeresult(filename,content,words,postags):
    resultPath = os.path.join(parent, "data", "postag", "output", filename)
    f = open(resultPath, mode='a', encoding='utf-8')
    f.writelines('*' * 100 + "原文本是" + '*' * 100 + '\n')
    f.writelines(content)
    f.writelines('\n')
    f.flush()
    f.writelines('*' * 100 + "分词，词性如下" + '*' * 100 + '\n')
    i=0
    for line in words:
        f.writelines(line)
        f.writelines("   ")
        f.writelines(postags[i])
        f.writelines('\n')
        f.flush()
        i=i+1
    f.close()


def send_postag(datalist):
    mydata = json.dumps(datalist)

    response = requests.post(url=myurl, headers=myheaders, data=mydata.encode('utf-8'))

    message = json.loads(response.text)
    return  message


@pytest.mark.regression
@pytest.mark.parametrize("title,file", [
 ("上半年GDP增长6.3%如何解读？统计局给出五句概括","test2.txt")
    ])
def test_postag_title_not_null(title,file):
    content = readcontent(file)
    datalist = [{"title":title,"content": content}]

    message=send_postag(datalist)
    # print(message[0])

    message1=test_splitword.send_splitword(datalist)
    writeresult(file,content,message1[0],message[0])


@pytest.mark.regression
@pytest.mark.parametrize("file", [
 ("劳动法")
    ])
def test_postag_title_is_null(file):
    content = readcontent(file)
    datalist = [{"title":"","content": content}]
    message = send_postag(datalist)
    # print(message[0])

    message1 = test_splitword.send_splitword( datalist)
    # print(message1)

    writeresult(file, content, message1[0], message[0])


@pytest.mark.regression
def test_postag_multi_article():
    datalist = []
    resourcePath = os.path.join(parent, "data", "postag", "input")
    for file in os.listdir(resourcePath):
        content=readcontent(file)
        datalist.append({"title":"","content":content})

    # 词性分析结果
    message=send_postag(datalist)
    #分词结果
    message1 = test_splitword.send_splitword(datalist)

    i = 0
    for m in message:
        writeresult("multi_article.txt", datalist[i].get("content"), message1[i],m)
        i = i + 1

#test_postag_multi_article()
#test_postag_title_not_null("我是标题","test1.txt")
# test_postag_title_is_null("test1.txt")
@pytest.mark.regression
@pytest.mark.parametrize("datalist", [
 ([{},{}]),
 ([{"title":"","content":"这初心正与高山榕那坚韧顽强、奋发向上的精神相呼应。"},{"content":"这初心正与高山榕那坚韧顽强、奋发向上的精神相呼应。"}]),
 ([{"title":"","content":"这初心正与高山榕那坚韧顽强、奋发向上的精神相呼应。"},{"title":"这初心正"}]),
    ([{"content":"这初心"},{"title":"","content":""}])
])
def test_postag_multi_article_miss_some_field(datalist):
    message=send_postag(datalist)
    #print(message+"000")
    assert message.startswith("article")