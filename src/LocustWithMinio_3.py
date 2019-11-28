'''

任务三：两任务，同时执行上传和请求查询云盘文件

'''

# coding=utf-8
import time
from minio import Minio
from minio.error import ResponseError
import os,requests
from locust import HttpLocust, TaskSet, task, between, events
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings()

countUpload = 0
TotalTimeUpload = 0

countGetLists = 0
TotalTimeGetLists = 0

path = "1.jpg"

class MinioTest(TaskSet):
    def on_start(self):     #初始化，on_start只会执行一次
        global minioClient
        minioClient = Minio('play.min.io',
                            access_key='Q3AM3UQ867SPQQA43P2F',
                            secret_key='zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG',
                            secure=True)
    @task(2)
    def updateFile(self):
        try:
            # 请求成功时，标记该请求执行成功
            start_time = time.time()
            '''第一个参数储存桶名字，第二个参数你云端名字，第三个参数你本地文件'''
            minioClient.fput_object('rico', path , path)
            end_time = time.time()
            total_time = int((end_time - start_time) * 1000)
            events.request_success.fire(request_type="RpcClient",
                                        name="UploadFile",
                                        response_time=total_time,
                                        response_length=0)
            global countUpload , TotalTimeUpload
            countUpload = countUpload + 1
            TotalTimeUpload = TotalTimeUpload + total_time
            print(path + " update success! With time ： "+ str(total_time)+'  平均时间为 %.3f ms  ' % (TotalTimeUpload/countUpload)+ "  count:"+ str(countUpload))
        except ResponseError as err:
            print(err)

    @task(1)
    def getObjLists(self):
        starttime = time.time()
        objectLists = minioClient.list_objects('rico', recursive=True)
        for objectList in objectLists:
            print('fileName: '+objectList.object_name)
        endtime = time.time()
        totaltime = int((endtime - starttime) * 1000)
        events.request_success.fire(request_type="getObjLists",
                                    name="getwenwenList",
                                    response_time=totaltime,
                                    response_length=0)
        global countGetLists, TotalTimeGetLists
        countGetLists = countGetLists + 1
        TotalTimeGetLists = TotalTimeGetLists + totaltime
        print(" Request time: " + str(totaltime) + '  平均时间为 %.3f ms  ' % (
                    TotalTimeGetLists / countGetLists) + "  count:" + str(countGetLists))

class websitUser(HttpLocust):
    host = 'https://play.min.io/minio'
    task_set = MinioTest
    wait_time = between(2, 5)

if __name__ == "__main__":
    os.system("locust -f LocustWithMinio_4.py")