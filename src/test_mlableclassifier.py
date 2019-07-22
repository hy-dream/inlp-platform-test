import pytest
import requests
import json
import  os,shutil
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
myurl = baseURL + 'mlableClassifier'
myheaders = {'content-type': 'application/json'}

def readcontent(filename):
    resourcePath = os.path.join(parent, "data", "mlableclassifier", "input",filename)
    f = open(resourcePath, mode='r', encoding='utf-8')
    content = f.readlines()
    f.flush()
    f.close()
    content2="".join(content)
    return content2

def send_mlableclassifier(datalist):
    mydata = json.dumps(datalist)

    response = requests.post(url=myurl, headers=myheaders, data=mydata.encode('utf-8'))

    message = json.loads(response.text)
    return  message




    #("林志玲倾情公益 太阳雨阳光浴室与白鹭义工团落户桂林","公益1","公益1")
    #  ("生活之道","万象","万象") 万象的定义不清楚 其他的定义
@pytest.mark.regression
@pytest.mark.parametrize("title,file,expected", [
 ("斯里兰卡政治危机再度升级 总统宣布解散议会","政治","政治"),
    ("美联储主席鲍威尔：将采取恰当措施维持经济持续扩张", "经济", "经济"),
    ("北京通州发生一起交通事故 4死1伤 两车损坏","事故","事故"),
    ("官方回应互联网“寒冬”:经济增长1%拉动200万人就业","就业","就业"),
    ("奇普菲尔德的新作：柏林博物馆岛的“文化卫城”","文化","文化"),
    ("夏季常吃六种豆 平安过“苦夏”","生活","生活"),
    ("女超综述-王霜回归首秀破门 武汉主场2-1逆袭广东","体育","体育"),
    ("新歌《如约》而至 刘宇宁在音乐中探索真我","娱乐","娱乐"),
    ("伊朗无人机贴脸拍美国航母，美国航母是纸老虎吗?","军事","军事"),
    ("王昌荣在全省加强诉源治理工作部署会上强调:深入推进诉源治理 源头减少诉讼增量 持续增强群众获得感幸福感安全感","法制","法制"),
    ("学位证编号出错 毕业生离校半月后被短信召回","教育","教育"),
    ("中国科研团队发布两款柔性芯片：厚度小于25微米","科技","科技"),
("持续关注江西灾情 中国红十字会共向灾区调拨近190万元救灾物资","公益","公益")
    ])
def test_mlableclassifier_title_not_null(title,file,expected):
    content = readcontent(file)
    datalist = [{"title":title,"content": content}]

    message=send_mlableclassifier(datalist)
    print(message[0])
    assert expected in message[0]


@pytest.mark.regression
@pytest.mark.parametrize("file,expected", [
 ("体育","体育")
    ])
def test_mlableclassifier_title_is_null(file,expected):
    content = readcontent(file)
    datalist = [{"title":"","content": content}]
    message = send_mlableclassifier(datalist)
    print(message[0])
    assert expected in message[0]


@pytest.mark.regression
def test_mlableclassifier_multi_article():
    datalist = []
    resourcePath = os.path.join(parent, "data", "mlableclassifier", "input")
    for file in os.listdir(resourcePath):
        content=readcontent(file)
        datalist.append({"title":"","content":content})

    # 词性分析结果
    message=send_mlableclassifier(datalist)
    allType=['政治', '经济', '事故', '公益', '就业', '万象', '文化', '生活',   '体育', '娱乐', '军事', '法制', '教育', '科技','其他']

    for item in message:
        for text in item:
            assert text in allType


@pytest.mark.regression
@pytest.mark.parametrize("datalist", [
 ([{},{}]),
 ([{"title":"","content":"会议期间，浙江省柔性电子与智能技术全球研究中心研发团队发布了两款经减薄后厚度小于25微米的柔性芯片，其厚度不到人体头发丝直径的1/4。。"},{"content":"这初心正与高山榕那坚韧顽强、奋发向上的精神相呼应。"}]),
 ([{"title":"","content":"这初心正与高山榕那坚韧顽强、奋发向上的精神相呼应。"},{"title":"第二届柔性电子国际学术大会（ICFE 2019）在杭州举行。"}]),
    ([{"content":"第二届柔性电子国际学术大会（ICFE 2019）在杭州举行。"},{"title":"","content":""}])
])
def test_mlableclassifier_multi_article_miss_some_field(datalist):
    message=send_mlableclassifier(datalist)
    #print(message+"000")
    assert message.startswith("article")