from rbkNetProtoEnums import *
import rbkNetProtoEnums
import json
import socket
import os
import time

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ip address of RBK!
so.connect(('192.168.4.136', API_PORT_CTRL))
# so.connect(('127.0.0.1', API_PORT_STATE))
so.settimeout(5)

jCmd = {"vx": 0.5, "vy": 0.0, "w": 0.0}
originspeed = jCmd['vx']


def sendspeed(cmd):
    so.send(packMsg(1, robot_control_motion_req, jCmd))
    print('vx = %f' % cmd['vx'])
    # try:
    #     data = so.recv(16)
    # except socket.timeout:
    #     print('timeout')
    #     quit()

    # jsonDataLen = 0
    # backReqNum = 0
    # if(len(data) < 16):
    #     print('pack head error')
    #     print(data)
    #     os.system('pause')
    #     so.close()
    #     quit()
    # else:
    #     jsonDataLen, backReqNum = unpackHead(data)
    #     print('json datalen: %d, backReqNum: %d' % (jsonDataLen, backReqNum))

    # if(jsonDataLen > 0):
    #     data = so.recv(1024)
    #     ret = json.loads(data)

    #     print(ret)


sendspeed(jCmd)
time.sleep(2)
#jCmd['vx'] = 0
# sendspeed(jCmd)
# quit()
deltat = 0.02

# while(True):
#    time.sleep(deltat)
#    acc = (originspeed - jCmd['vx'] + 0.01) * (jCmd['vx']) * 0.3
#    jCmd['vx'] = jCmd['vx'] * - acc * deltat
#    sendspeed(jCmd)
t = 0
while t < 0.5:
    time.sleep(deltat)
    acc = (jCmd['vx'] * 4)**2
    jCmd['vx'] = jCmd['vx'] - acc * deltat
    sendspeed(jCmd)
    t += deltat

    sendspeed(jCmd)
so.close()
