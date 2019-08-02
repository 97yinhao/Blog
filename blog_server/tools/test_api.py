"""
    模仿三十个请求
"""
import random
import threading
import requests


# 线程事件函数
def getRequest():
    url1 = 'http://127.0.0.1:8000/test_api/'
    url2 = 'http://127.0.0.1:8001/test_api/'
    get_url = random.choice([url1, url2])
    # 打开浏览器输入地址
    requests.get(get_url)


t_list = []
for i in range(30):
    t = threading.Thread(target=getRequest)
    t_list.append(t)
    t.start()

for m in t_list:
    m.join()