from rbkNetProtoEnums import *
import rbkNetProtoEnums
import json
import socket
import os
import time

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so.connect(('192.168.4.59', API_PORT_STATE))
so.settimeout(20)
# so.connect(('127.0.0.1', API_PORT_STATE))

cnt = 0

while True:
    try:
        time.sleep(0.1)
    except (Exception,e):
        print(e)
        break

    so.send(packMsg(1, robot_status_area_req, {}))
    try:
        data = so.recv(16)
    except socket.timeout:
        print('timeout')
        continue

    jsonDataLen = 0
    if(len(data) < 16):
        print('pack head error')
        os.system('pause')
        so.close()
        quit()
    else:
        jsonDataLen = unpackHead(data)

    data = so.recv(1024)
    ret = json.loads(data)  
    area_num = len(ret['area_ids'])
    print('area num = %d, cnt = %d' %(area_num, cnt)) 
    if(area_num > 1):
        cnt = cnt + 1
        print('=================================!!!')

so.close()
