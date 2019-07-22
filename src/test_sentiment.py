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
myurl = baseURL + 'sentiment'
myheaders = {'content-type': 'application/json'}

def readcontent(filename):
    resourcePath = os.path.join(parent, "data", "sentiment", "content",filename)
    f = open(resourcePath, mode='r', encoding='utf-8')
    content = f.readlines()
    f.flush()
    f.close()
    content2="".join(content)
    return content2


def readcomment(filename):
    resourcePath = os.path.join(parent, "data", "sentiment", "comment",filename)
    f = open(resourcePath, mode='r', encoding='utf-8')
    content = f.readlines()
    f.flush()
    f.close()
    content2="".join(content)
    return content2

def send_sentiment(myparms,datalist):
    mydata = json.dumps(datalist)

    response = requests.post(url=myurl, headers=myheaders, params=myparms, data=mydata.encode('utf-8'))
    summary = json.loads(response.text)

    return summary


@pytest.mark.regression
def test_sentiment_domain_content():
    myparms = {"domain": "content"}
    content = readcontent("鬼吹灯.txt")
    datalist = [{"title": "", "content": content}]

    summary = send_sentiment(myparms,datalist)
    assert summary[0] > 0 and summary[0] < 1
    print(summary)


@pytest.mark.regression
@pytest.mark.parametrize("file", [
 ("微博1"),
 ("微博2"),
 ("微博3"),
 ("微博4"),
  ("豆瓣1"),
("豆瓣2")
])
def test_sentiment_domain_comment(file):
    myparms = {"domain": "content"}
    content = readcomment(file)
    datalist = [{"title": file, "content": content}]
    summary = send_sentiment(myparms, datalist)
    assert summary[0]>0 and summary[0] <1
    print(summary)


@pytest.mark.regression
def test_sentiment_multi_article_comment():
    log.debug('-----调试信息[debug]---test_summary_multi_article--')
    myparms = {"domain": "comment"}
    datalist = []
    resourcePath = os.path.join(parent, "data", "sentiment", "comment")
    for file in os.listdir(resourcePath):
        content=readcomment(file)
        datalist.append({"title":"","content":content})

    message = send_sentiment(myparms,datalist)
    for m in message:
        assert m > 0 and m < 1
    #    print(m)


@pytest.mark.regression
def test_sentiment_multi_article_content():
    log.debug('-----调试信息[debug]---test_summary_multi_article--')
    myparms = {"domain": "content"}
    datalist = []
    resourcePath = os.path.join(parent, "data", "sentiment", "content")
    for file in os.listdir(resourcePath):
        content=readcontent(file)
        datalist.append({"title":"","content":content})

    message = send_sentiment(myparms,datalist)
    for m in message:
        assert m > 0 and m < 1
        print(m)


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
    myparms = {"domain": "content"}
    mydata = json.dumps(datalist)

    response = requests.post(url=myurl, headers=myheaders, params=myparms, data=mydata.encode('utf-8'))
    message = json.loads(response.text)
    #print(message+"000")
    assert message.startswith("article")

#test_sentiment_domain_comment("微博3")