from rbkNetProtoEnums import *
import rbkNetProtoEnums
import json
import socket
import os
import time
import sys

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if(len(sys.argv) < 4):
    print('No enough input param')
    print('Usage: [ip] [speed(m/s)] [delay(seconds)]')
    print('example: BYD_No4_Test.exe 192.168.192.5 0.08 0.5')
# ip address of RBK!

targetip = sys.argv[1]
speed = float(sys.argv[2])
if(speed > 0.1):
    print('Overspeed: %fm/s!' % speed)
    speed = 0.1
delay = float(sys.argv[3])

so.connect((targetip, API_PORT_CTRL))
so.settimeout(5)

jCmd = {"vx": speed, "vy": 0.0, "w": 0.0}

while(True):
    time.sleep(delay)
    jCmd['vx'] = jCmd['vx'] * -1.0
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
        print('json datalen: %d, backReqNum: %d' % (jsonDataLen, backReqNum))

    if(jsonDataLen > 0):
        data = so.recv(1024)
        ret = json.loads(data)

        print(ret)

so.close()
