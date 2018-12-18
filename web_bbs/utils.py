import os.path
import time
import json

def log(*args,**kwargs):
    #定义当前时间
    dt=time.strftime('%H:%M:%S',time.localtime(int(time.time())))
    #打印东西追加到gua.log.txt文件
    with open('gua.log.txt','a',encoding='utf-8') as f:
        print(dt,*args,file=f,**kwargs)
