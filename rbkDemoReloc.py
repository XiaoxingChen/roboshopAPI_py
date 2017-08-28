from rbkNetProtoEnums import *
import rbkNetProtoEnums
import json
import socket
import os

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# so.connect(('192.168.4.109', API_PORT_STATE))
so.connect(('127.0.0.1', API_PORT_STATE))
so.settimeout(5)



so.send(packMsg(1, robot_control_reloc_req, {"x":10.0,"y":3.0,"angle":0}))
try:
    data = so.recv(16)
except socket.timeout:
    print('timeout')
    quit()

jsonDataLen = 0
backReqNum = 0
if(len(data) < 16):
    print('pack head error')
    os.system('pause')
    so.close()
    quit()
else:
    jsonDataLen, backReqNum = unpackHead(data)
    print('json datalen: %d, backReqNum: %d' %(jsonDataLen, backReqNum))

if(jsonDataLen > 0):
    data = so.recv(1024)
    ret = json.loads(data)

    print(ret)

os.system('pause')
so.close()
