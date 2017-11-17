from rbkNetProtoEnums import *
import rbkNetProtoEnums
import json
import socket
import os
import time

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

so.connect(('192.168.4.53', API_PORT_CTRL))
#so.connect(('192.168.4.54', API_PORT_CTRL))

so.settimeout(5)

radius = 0.3
vx0 = 0.5
vy0 = 0.5
speedgain = 1.05
jCmd = {"vx":vx0, "vy": vy0, "w": (vx0*vx0 + vy0*vy0)** 0.5 /radius}

while(True):
    time.sleep(0.1)
    so.send(packMsg(1, robot_control_motion_req, jCmd))
    try:
        data = so.recv(16)
    except socket.timeout:
        print('timeout')
        quit()

    jsonDataLen = 0
    backReqNum = 0
    if(len(data) < 16):
        print('pack head error')
        print(data)
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
 

    jCmd['vx'] = jCmd['vx'] * speedgain
    jCmd['vy'] = jCmd['vy'] * speedgain
    jCmd['w'] = jCmd['w'] * speedgain
    if jCmd['vx'] > 2.8:
        speedgain = 1

so.close()
