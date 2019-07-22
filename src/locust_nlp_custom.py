from locust import HttpLocust,TaskSet,task
import json
import os




parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
missionList=["splitSentence","splitWord","posTag","ner","wordWeight","wordWeightMap","keyWord","vectorKeyWord","keyPhrase","keyExpression","summary","mlableClassifier","sentiment"]

def readcontent():
    data=[]
    folder="book"
    folderPath = os.path.join(parent, "data", "locust", folder)
    for file in os.listdir(folderPath):
        resourcePath = os.path.join(parent, "data", "locust", folder, file)
        f = open(resourcePath, mode='r', encoding='utf-8')
        content = f.readlines()
        f.flush()
        f.close()
        content = "".join(content)
        data.append({"title": "", "content": content})
    return data

def writeresult(content):
    resultPath = os.path.join(parent, "data", "locust", "request_body")
    f = open(resultPath, mode='a', encoding='utf-8')
    f.writelines('*' * 100  + '\n')
    f.writelines(content)
    f.writelines('\n')
    f.flush()
    f.close()


class UserBehavior(TaskSet):

    def setup(self):
        # self.data = json.dumps(readcontent()).encode('utf-8')
        print('task setup')

# and json.loads(response.text) != "向MASTER_TO_SLAVE_QUEUE放入数据失败"
    @task(1)
    def getcustom(self):
        data=self.locust.data
        with  self.client.post("custom",data, catch_response=True) as response:
            if response.status_code == 200:  # 对http响应码是否200进行判断
                response.success()
            else:
                response.failure("custom[Failed!]")

class WebSite(HttpLocust):

    articles = readcontent()
    parametersList=[]
    for item in missionList:
        if item=="summary":
            parametersList.append( {"percentage":0.5,"charLimit": 1500})
        elif item=="sentiment":
            parametersList.append({"domain": "content"})
        else:
            parametersList.append({})

    dataList = {'missionList': missionList, 'parametersList': parametersList, 'data': articles}

    data = json.dumps(dataList).encode('utf-8')

    task_set = UserBehavior
    min_wait = 15000

    max_wait = 18000
