from netprotocol.rbkNetProtoEnums import *
import json
import socket
import os

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so.settimeout(2)
so.connect(('192.168.4.235', API_PORT_OTHER))
# so.connect(('192.168.192.5', API_PORT_OTHER))


so.send(packMsg(1, robot_other_setdo_req, {"id": 15, "status": False}))

data = so.recv(16)
jsonDataLen = 0
if(len(data) < 16):
    print('pack head error')
    os.system('pause')
    so.close()
    quit()
else:
    jsonDataLen = unpackHead(data)[0]
    print([hex(v) for v in data])

if(jsonDataLen > 0):
    data = so.recv(1024)
    try:
        ret = json.loads(data)
    except json.decoder.JSONDecodeError:
        print(data)

    print(ret)

os.system('pause')
so.close()
