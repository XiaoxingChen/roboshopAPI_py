from rbkNetProtoEnums import *
import rbkNetProtoEnums
import json
import socket
import os

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so.settimeout(2)
#so.connect(('192.168.4.109', API_PORT_STATE))
so.connect(('192.168.192.5', API_PORT_ROBOD))


so.send(packMsg(1, robot_daemon_ls_req, {"path": '/log'}))
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
try:
    ret = json.loads(data)
except json.decoder.JSONDecodeError:
    print(data)

print(ret)

os.system('pause')
so.close()
