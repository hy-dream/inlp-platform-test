from locust import HttpLocust,TaskSet,task
import json
import os




parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


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

class UserBehavior(TaskSet):

    def setup(self):
        # self.data = json.dumps(readcontent()).encode('utf-8')
        print('task setup')


    @task(1)
    def getKeyword(self):
        # mydata = json.dumps(datalist)
        # data = mydata.encode('utf-8')
        data=self.locust.data
        with  self.client.post("keyWord",data, catch_response=True) as response:
            if response.status_code == 200:  # 对http响应码是否200进行判断
                response.success()
            else:
                response.failure("keyword[Failed!]")
    @task(1)
    def getNER(self):
        # mydata = json.dumps(datalist)
        # data = mydata.encode('utf-8')
        data = self.locust.data
        with  self.client.post("ner", data, catch_response=True) as response:
            if response.status_code == 200:  # 对http响应码是否200进行判断
                response.success()
            else:
                response.failure("ner[Failed!]")

    @task(1)
    def getSummary(self):
        data = self.locust.data
        with  self.client.post("summary", data, catch_response=True) as response:
            if response.status_code == 200:  # 对http响应码是否200进行判断
                response.success()
            else:
                response.failure("summary[Failed!]")

    @task(1000)
    def getSplitword(self):
        data = self.locust.data
        with  self.client.post("splitWord", data, catch_response=True) as response:
            if response.status_code == 200:  # 对http响应码是否200进行判断
                response.success()
            else:
                response.failure("splitword[Failed!]")

    @task(1)
    def getSplitsentence(self):
        data = self.locust.data
        with  self.client.post("splitSentence", data, catch_response=True) as response:
            if response.status_code == 200:  # 对http响应码是否200进行判断
                response.success()
            else:
                response.failure("splitsentence[Failed!]")


    @task(1)
    def getsentiment(self):
        data = self.locust.data
        with  self.client.post("sentiment", data, catch_response=True) as response:
            if response.status_code == 200:  # 对http响应码是否200进行判断
                response.success()
            else:
                response.failure("sentiment情感分析[Failed!]")


    @task(1)
    def getPostag(self):
        data = self.locust.data
        with  self.client.post("posTag", data, catch_response=True) as response:
            if response.status_code == 200:  # 对http响应码是否200进行判断
                response.success()
            else:
                response.failure("postag词性[Failed!]")

    @task(1)
    def getmlableClassifier(self):
        data = self.locust.data
        with  self.client.post("mlableClassifier", data, catch_response=True) as response:
            if response.status_code == 200:  # 对http响应码是否200进行判断
                response.success()
            else:
                response.failure("mlableClassifier多分类[Failed!]")

class WebSite(HttpLocust):

    data = json.dumps(readcontent()).encode('utf-8')
    task_set = UserBehavior
    min_wait = 2000

    max_wait = 5000

