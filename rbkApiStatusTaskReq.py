from rbkNetProtoEnums import *
import rbkNetProtoEnums
import json
import socket
import os

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#so.connect(('192.168.4.109', API_PORT_STATE))
so.connect(('192.168.192.5', API_PORT_STATE))


so.send(packMsg(1, robot_status_task_req, {}))
data = so.recv(16)
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

print(ret)

os.system('pause')
so.close()
