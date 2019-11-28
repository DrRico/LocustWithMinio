'''

任务一：打印平均时间版

'''

# coding=utf-8
import time
from minio import Minio
from minio.error import ResponseError
import os,requests
from locust import HttpLocust, TaskSet, task, between, events
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings()
count = 0
TotalTime = 0
path = "1.jpg"
class MinioTest(TaskSet):

    def on_start(self):     #初始化，on_start只会执行一次
        self.minioClient = Minio('play.min.io',
                            access_key='Q3AM3UQ867SPQQA43P2F',
                            secret_key='zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG',
                            secure=True)

    @task
    def updateFile(self):
        try:
            '''第一个参数储存桶名字，第二个参数你云端名字，第三个参数你本地文件'''
            # 请求成功时，标记该请求执行成功
            start_time = time.time()
            self.minioClient.fput_object('wenwen', path , path)
            end_time = time.time()
            total_time = int((end_time - start_time) * 1000)
            events.request_success.fire(request_type="RpcClient",
                                        name="wenwenTest",
                                        response_time=total_time,
                                        response_length=0)
            global count , TotalTime
            count = count + 1
            TotalTime = TotalTime + total_time
            print(path + " update success! With time ： "+ str(total_time)+'  平均时间为 %.3f ms  ' % (TotalTime/count)+ "  count:"+ str(count))
        except ResponseError as err:
            print(err)


class websitUser(HttpLocust):
    host = 'https://play.min.io/minio'
    task_set = MinioTest
    wait_time = between(2, 5)

if __name__ == "__main__":
    os.system("locust -f LocustWithMinio_1.py")