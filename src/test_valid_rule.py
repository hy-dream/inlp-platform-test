import test_summary
import test_splitword
import test_splitsentence
import test_sentiment
import test_postag
import test_ner
import test_mlableclassifier
import pytest
import requests
import json
import test_custom

@pytest.mark.regression
def test_too_many_articles():
    #最多支持1000个文章
    expected='too many articles'
    datalist=[]
    for i in range(1002):
        datalist.append({"title":"","content":"文章详细内容"})

    #摘要接口
    myparms = {"percentage": 0.3, "charLimit": 1000}
    m1=test_summary.send_summary(myparms,datalist)
    assert m1==expected

    #情感接口
    myparms = {"domain": "content"}
    m1=test_sentiment.send_sentiment(myparms,datalist)
    assert m1==expected

    #实体接口
    m1=test_ner.send_ner(datalist)
    assert m1 ==expected

    #分词接口
    m1=test_splitword.send_splitword(datalist)
    assert m1 ==expected

    #分句接口
    m1 = test_splitsentence.send_sentence(datalist)
    assert m1 == expected

    #关键表述


    #词性接口
    m1=test_postag.send_postag(datalist)
    assert m1 ==expected

    #文本分类接口
    m1=test_mlableclassifier.send_mlableclassifier(datalist)
    assert m1 == expected

    #关键词接口

    #自定义接口

@pytest.mark.regression
def test_no_article_in_data():
    datalist=[]
    expected='no article in data'
    # 摘要接口
    myparms = {"percentage": 0.3, "charLimit": 1000}
    m1 = test_summary.send_summary(myparms, datalist)
    assert m1 == expected

    # 情感接口
    myparms = {"domain": "content"}
    m1 = test_sentiment.send_sentiment(myparms, datalist)
    assert m1 == expected

    # 实体接口
    m1 = test_ner.send_ner(datalist)
    assert m1 == expected

    # 分词接口
    m1 = test_splitword.send_splitword(datalist)
    assert m1 == expected

    # 分句接口
    m1 = test_splitsentence.send_sentence(datalist)
    assert m1 == expected

    # 关键表述

    # 词性接口
    m1 = test_postag.send_postag(datalist)
    assert m1 == expected

    # 文本分类接口
    m1 = test_mlableclassifier.send_mlableclassifier(datalist)
    assert m1 == expected

    # 关键词接口

    # 自定义接口


@pytest.mark.regression
def test_article_data_must_be_a_list():
    expected='article data must be a list'
    datalist={"title":"","content":"我是内容"}
    # 摘要接口
    myparms = {"percentage": 0.3, "charLimit": 1000}
    m1 = test_summary.send_summary(myparms, datalist)
    assert m1 == expected

    # 情感接口
    myparms = {"domain": "content"}
    m1 = test_sentiment.send_sentiment(myparms, datalist)
    assert m1 == expected

    # 实体接口
    m1 = test_ner.send_ner(datalist)
    assert m1 == expected

    # 分词接口
    m1 = test_splitword.send_splitword(datalist)
    assert m1 == expected

    # 分句接口
    m1 = test_splitsentence.send_sentence(datalist)
    assert m1 == expected

    # 关键表述

    # 词性接口
    m1 = test_postag.send_postag(datalist)
    assert m1 == expected

    # 文本分类接口
    m1 = test_mlableclassifier.send_mlableclassifier(datalist)
    assert m1 == expected

    # 关键词接口

    # 自定义接口


@pytest.mark.regression
def test_article_is_not_a_dict():
    expected = 'is not a dict'
    datalist = [{"title": "", "content": "我是内容"},("title")]
    # 摘要接口
    myparms = {"percentage": 0.3, "charLimit": 1000}
    m1 = test_summary.send_summary(myparms, datalist)
    assert m1.endswith(expected)

    # 情感接口
    myparms = {"domain": "content"}
    m1 = test_sentiment.send_sentiment(myparms, datalist)
    assert m1.endswith(expected)

    # 实体接口
    m1 = test_ner.send_ner(datalist)
    assert m1.endswith(expected)

    # 分词接口
    m1 = test_splitword.send_splitword(datalist)
    assert m1.endswith(expected)

    # 分句接口
    m1 = test_splitsentence.send_sentence(datalist)
    assert m1.endswith(expected)

    # 关键表述

    # 词性接口
    m1 = test_postag.send_postag(datalist)
    assert m1.endswith(expected)

    # 文本分类接口
    m1 = test_mlableclassifier.send_mlableclassifier(datalist)
    assert m1.endswith(expected)

    # 关键词接口

    # 自定义接口



@pytest.mark.regression
def test_has_no_title():
    expected = 'article 1 has no title'
    datalist =[{"title": "", "content": "我是内容"},{"content":"我是第二個内容"}]
    # 摘要接口
    myparms = {"percentage": 0.3, "charLimit": 1000}
    m1 = test_summary.send_summary(myparms, datalist)
    assert m1 == expected

    # 情感接口
    myparms = {"domain": "content"}
    m1 = test_sentiment.send_sentiment(myparms, datalist)
    assert m1 == expected

    # 实体接口
    m1 = test_ner.send_ner(datalist)
    assert m1 == expected

    # 分词接口
    m1 = test_splitword.send_splitword(datalist)
    assert m1 == expected

    # 分句接口
    m1 = test_splitsentence.send_sentence(datalist)
    assert m1 == expected

    # 关键表述

    # 词性接口
    m1 = test_postag.send_postag(datalist)
    assert m1 == expected

    # 文本分类接口
    m1 = test_mlableclassifier.send_mlableclassifier(datalist)
    assert m1 == expected

    # 关键词接口

    # 自定义接口


@pytest.mark.regression
def test_has_no_content():
    expected = 'article 2 has no content'
    datalist = [{"title": "", "content": "我是内容"}, {"title":"","content": "我是第二個内容"},{"title":""}]
    # 摘要接口
    myparms = {"percentage": 0.3, "charLimit": 1000}
    m1 = test_summary.send_summary(myparms, datalist)
    assert m1 == expected

    # 情感接口
    myparms = {"domain": "content"}
    m1 = test_sentiment.send_sentiment(myparms, datalist)
    assert m1 == expected

    # 实体接口
    m1 = test_ner.send_ner(datalist)
    assert m1 == expected

    # 分词接口
    m1 = test_splitword.send_splitword(datalist)
    assert m1 == expected

    # 分句接口
    m1 = test_splitsentence.send_sentence(datalist)
    assert m1 == expected

    # 关键表述

    # 词性接口
    m1 = test_postag.send_postag(datalist)
    assert m1 == expected

    # 文本分类接口
    m1 = test_mlableclassifier.send_mlableclassifier(datalist)
    assert m1 == expected

    # 关键词接口

    # 自定义接口

@pytest.mark.parametrize("datalist", [
 ([{"title":1,"content":"abc"},{"title":"","content":"abc"}]),
 ([{"title":[1,2],"content":"abc"},{"title":"","content":"abc"}]),
 ([{"title":"","content":"abc"},{"title":3.4,"content":"abc"}]),
])
@pytest.mark.regression
def test_title_is_not_a_string(datalist):
    expected = 'title is not a string'

    # 摘要接口
    myparms = {"percentage": 0.3, "charLimit": 1000}
    m1 = test_summary.send_summary(myparms, datalist)
    assert m1.endswith(expected)

    # 情感接口
    myparms = {"domain": "content"}
    m1 = test_sentiment.send_sentiment(myparms, datalist)
    assert m1.endswith(expected)

    # 实体接口
    m1 = test_ner.send_ner(datalist)
    assert m1.endswith(expected)

    # 分词接口
    m1 = test_splitword.send_splitword(datalist)
    assert m1.endswith(expected)

    # 分句接口
    m1 = test_splitsentence.send_sentence(datalist)
    assert m1.endswith(expected)

    # 关键表述

    # 词性接口
    m1 = test_postag.send_postag(datalist)
    assert m1.endswith(expected)

    # 文本分类接口
    m1 = test_mlableclassifier.send_mlableclassifier(datalist)
    assert m1.endswith(expected)

    # 关键词接口

    # 自定义接口

@pytest.mark.regression
@pytest.mark.parametrize("datalist", [
 ([{"title":"","content":1},{"title":"","content":"abc"}]),
 ([{"title":"","content":["abc"]},{"title":"","content":"abc"}]),
 ([{"title":"","content":"abc"},{"title":"","content":3.4}]),
])
def test_content_is_not_a_string(datalist):
    expected = 'content is not a string'

    # 摘要接口
    myparms = {"percentage": 0.3, "charLimit": 1000}
    m1 = test_summary.send_summary(myparms, datalist)
    assert m1.endswith(expected)

    # 情感接口
    myparms = {"domain": "content"}
    m1 = test_sentiment.send_sentiment(myparms, datalist)
    assert m1.endswith(expected)

    # 实体接口
    m1 = test_ner.send_ner(datalist)
    assert m1.endswith(expected)

    # 分词接口
    m1 = test_splitword.send_splitword(datalist)
    assert m1.endswith(expected)

    # 分句接口
    m1 = test_splitsentence.send_sentence(datalist)
    assert m1.endswith(expected)

    # 关键表述

    # 词性接口
    m1 = test_postag.send_postag(datalist)
    assert m1.endswith(expected)

    # 文本分类接口
    m1 = test_mlableclassifier.send_mlableclassifier(datalist)
    assert m1.endswith(expected)

    # 关键词接口

    # 自定义接口


@pytest.mark.regression
@pytest.mark.parametrize("datalist", [
 ([{"title":"","content":""},{"title":"","content":"abc"}]),
 ([{"title":"","content":""},{"title":"","content":"abc"}]),
 ([{"title":"","content":"abc"},{"title":"","content":""}]),
])
def test_content_is_null(datalist):
    expected = 'content is null'

    # 摘要接口
    myparms = {"percentage": 0.3, "charLimit": 1000}
    m1 = test_summary.send_summary(myparms, datalist)
    assert m1.endswith(expected)

    # 情感接口
    myparms = {"domain": "content"}
    m1 = test_sentiment.send_sentiment(myparms, datalist)
    assert m1.endswith(expected)

    # 实体接口
    m1 = test_ner.send_ner(datalist)
    assert m1.endswith(expected)

    # 分词接口
    m1 = test_splitword.send_splitword(datalist)
    assert m1.endswith(expected)

    # 分句接口
    m1 = test_splitsentence.send_sentence(datalist)
    assert m1.endswith(expected)

    # 关键表述

    # 词性接口
    m1 = test_postag.send_postag(datalist)
    assert m1.endswith(expected)

    # 文本分类接口
    m1 = test_mlableclassifier.send_mlableclassifier(datalist)
    assert m1.endswith(expected)

    # 关键词接口

    # 自定义接口


@pytest.mark.regression
def test_title_is_longer_than_100():
    title="布洛芬是我们生活中的常用药，对于布洛芬这个药物，它的功效相对来说是比较多的，可以有效退热、缓解由于感冒流感等引起的轻度头疼、咽痛以及牙痛等症状，但是布洛芬这个药物，并不是适合所有人服用的，哪些人不是個。"
    datalist=[{"title":"","content":"我是内容"},{"title":title,"content":"我是内容"}]
    expected = 'article 1 title is longer than 100'

    # 摘要接口
    myparms = {"percentage": 0.3, "charLimit": 1000}
    m1 = test_summary.send_summary(myparms, datalist)
    assert m1 == expected

    # 情感接口
    myparms = {"domain": "content"}
    m1 = test_sentiment.send_sentiment(myparms, datalist)
    assert m1 == expected

    # 实体接口
    m1 = test_ner.send_ner(datalist)
    assert m1 == expected

    # 分词接口
    m1 = test_splitword.send_splitword(datalist)
    assert m1 == expected

    # 分句接口
    m1 = test_splitsentence.send_sentence(datalist)
    assert m1 == expected

    # 关键表述

    # 词性接口
    m1 = test_postag.send_postag(datalist)
    assert m1 == expected

    # 文本分类接口
    m1 = test_mlableclassifier.send_mlableclassifier(datalist)
    assert m1 == expected

    # 关键词接口

    # 自定义接口

@pytest.mark.regression
def test_content_is_not_Chinese():
    expected='article 1 content is not Chinese'
    content="Do you want a friend whom you could tell everything to, like your deepest feelings and thoughts? 我的英文Or are you afraid that your friend would laugh at you, or would not understand what you are going through? Anne Frank wanted the first kind, so she made her diary her best friend.Annie lived in Amsterdam in the Netherlands during World War II. Her family was Jewish so they had to hide or they would be caught by the German Nazis. She and her family hid away for nearly twenty-five months before they were discovered. During that time the only true friend was her diary. She said, I don't want to set down a series of facts in a diary as most people do, but I want this diary itself to be my best friend, and I shall call my friend Kitty. Now read how she felt after being in the hiding place since July 1942."
    datalist = [{"title": "", "content": content}]

    # 摘要接口
    myparms = {"percentage": 0.3, "charLimit": 1000}
    m1 = test_summary.send_summary(myparms, datalist)
    assert m1 == expected

    # 情感接口
    myparms = {"domain": "content"}
    m1 = test_sentiment.send_sentiment(myparms, datalist)
    assert m1 == expected

    # 实体接口
    m1 = test_ner.send_ner(datalist)
    assert m1 == expected

    # 分词接口
    m1 = test_splitword.send_splitword(datalist)
    assert m1 == expected

    # 分句接口
    m1 = test_splitsentence.send_sentence(datalist)
    assert m1 == expected

    # 关键表述

    # 词性接口
    m1 = test_postag.send_postag(datalist)
    assert m1 == expected

    # 文本分类接口
    m1 = test_mlableclassifier.send_mlableclassifier(datalist)
    assert m1 == expected

    # 关键词接口

    # 自定义接口

def send_request(url,datalist):
    baseURL = 'http://172.18.82.251:1240/'
    myurl = baseURL + url
    myheaders = {'content-type': 'application/json'}
    mydata = json.dumps(datalist)

    response = requests.post(url=myurl, headers=myheaders, data=mydata.encode('utf-8'))

    message = json.loads(response.text)
    return message


@pytest.mark.regression
def test_we_do_not_support_this_mission():
    expected="we do not support this mission"
    wrongrequest=["splitsentence","postag","NER","keyphrase"]
    datalist=[{"title":"","content":"我是内容"}]
    for url in wrongrequest:
        message=send_request(url,datalist)
        assert message== expected


@pytest.mark.regression
def test_custom_mission_is_conflict_with_data():
    datalist=[]
    expected='mission is conflict with data'
    message=test_custom.send_custom(datalist)
    assert message==expected


@pytest.mark.regression
def test_custom_data_must_has_missionList():
    expected="data must has missionList"
    dataList = { 'parametersList': [], 'data': []}
    message = test_custom.send_custom(dataList)
    assert message == expected


@pytest.mark.regression
def test_custom_missionList_must_be_a_list():
    expected="missionList must be a list"
    dataList = {"missionList":12,'parametersList': [], 'data': []}
    message = test_custom.send_custom(dataList)
    assert message == expected


@pytest.mark.regression
def test_custom_missionList_must_be_larger_than_1():
    expected="missionList must be larger than 1"
    dataList = {"missionList": [], 'parametersList': [], 'data': []}
    message = test_custom.send_custom(dataList)
    assert message == expected



@pytest.mark.regression
def test_custom_mission_is_not_in_avaliable():
    mission="newNer"
    expected='mission: ' + str(mission) + ' is not in avaliable'
    dataList = {"missionList": ["ner",mission], 'parametersList': [], 'data': []}
    message = test_custom.send_custom(dataList)
    assert message == expected



@pytest.mark.regression
def test_custom_data_must_has_parametersList():
    expected="data must has parametersList"
    dataList = {"missionList": ["ner"], 'data': []}
    message = test_custom.send_custom(dataList)
    assert message == expected



@pytest.mark.regression
def test_custom_parametersList_must_be_a_list():
    expected="parametersList must be a list"
    dataList = {"missionList": ["ner"], 'parametersList':23, 'data': []}
    message = test_custom.send_custom(dataList)
    assert message == expected


@pytest.mark.regression
def test_custom_parametersList_must_have_the_same_length_as_missionList():
    expected="parametersList must have the same length as missionList"
    dataList = {"missionList": ["ner"], 'parametersList': [], 'data': []}
    message = test_custom.send_custom(dataList)
    assert message == expected


@pytest.mark.regression
def test_custom_data_must_contain_article_data():
    expected="data must contain article data"
    dataList = {"missionList": ["ner"], 'parametersList': [{}]}
    message = test_custom.send_custom(dataList)
    assert message == expected


@pytest.mark.regression
def test_custom_valid_data_miss_title():
    articlelist = [{"title": "", "content": "我是内容"}, {"content": "我是第二個内容"}]
    expected = 'article 1 has no title'
    dataList = {"missionList": ["ner"], 'parametersList': [{}],'data':articlelist}
    message = test_custom.send_custom(dataList)
    assert message == expected


@pytest.mark.regression
def test_custom_valid_data_content_is_null():
    articlelist = [{"title": "", "content": "我是内容"}, {"title":"","content": ""}]
    expected = 'article 1 content is null'
    dataList = {"missionList": ["ner"], 'parametersList': [{}],'data':articlelist}
    message = test_custom.send_custom(dataList)
    assert message == expected

