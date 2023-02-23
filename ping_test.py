# -*- coding: utf-8 -*-

import os
import subprocess
import threading
import time
import re,sys
import ipaddress

interval = 1
count = 3

if sys.platform == 'win32':
    ping_cmd = ["ping", "-n", "1", "-w", "1000"]
else:
    ping_cmd = ["ping", "-c", "1", "-W", "1"]

# split_str = "time=|time<|时间=|时间<"
# ss = re.search(split_str, result)
# print(ss)

def getip(file):
    file_path = os.path.abspath(sys.argv[0])
    if sys.platform == 'win32':  # 判断是否为windows系统
        p = file_path.rfind('\\')
        filename = file_path[:p+1] + file

    else:
        p = file_path.rfind('/')
        filename = file_path[:p+1] + file

    with open(filename, 'r', encoding='utf-8') as f:
        iptxt = f.readlines()
    
    iplist = []

    for each in iptxt:
        each = each.strip()
        if each.rfind('/') != -1:
            for ip in ipaddress.IPv4Network(each):
                iplist.append(str(ip))
        else:
            iplist.append(each)

        # iptxt = map(lambda s: s.strip(), iptxt) #删除换行符

    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print('-'*30, current_time, '-'*30,)

    return iplist


def ping(ip):
    for i in range(1, count + 1):

        result = subprocess.run(ping_cmd +[ip], stdout=subprocess.PIPE)
        try:
            result = result.stdout.decode()
        except:
            result = result.stdout.decode('gbk')

        splitstr = ["time=","time<","时间=","时间<"]

        for s in splitstr:
            if s in result:
                if sys.platform == 'win32':
                    delay = result.split(s)[1].split(" TTL")[0]
                else:
                    delay = result.split(s)[1].split(" ")[0]

                if "time" in s:
                    loss = result.split("received, ")[1].split("% ")[0]
                else:
                    loss = result.split("丢失 = ")[1].split(" ")[0]

                break

        else:
            delay = -1
            loss = 100

        print("Ping {}\t result #{}:\t delay={}, loss={}".format(ip, i, delay, loss))  
        time.sleep(interval)


ip_list = getip('ipip.txt') # 在此输入ip文件的名字，文件需与py放到同一目录
# ip_list = ["10.0.3.251", "10.0.2.76", "10.0.5.251"] #临时测试可单独定义列表

threads = []
for ip in ip_list:
    thread = threading.Thread(target=ping, args=(ip,))
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
