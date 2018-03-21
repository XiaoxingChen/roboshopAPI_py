from netprotocol.rbkNetProtoEnums import *
import json
import socket
import os
import time
import sys

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if(len(sys.argv) < 4):
    print('No enough input param')
    print('example: BYD_No4_Test.exe 192.168.192.5')
# ip address of RBK!

targetip = sys.argv[1]
landmark1 = 'LM' + sys.argv[2]
landmark2 = 'LM' + sys.argv[3]

class BYDApi(object):

    def __init__(self):
        self._rbkip = targetip

        self._so_state = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._so_state.settimeout(3)
        self._so_state.connect((self._rbkip, API_PORT_STATE))

        self._so_task = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._so_task.settimeout(0.5)
        self._so_task.connect((self._rbkip, API_PORT_TASK))


    def gotarget(self, landmark):
        self._so_task.send(
            packMsg(1, robot_task_gotarget_req, {"id": landmark}))

    def reachtarget(self, landmark):
        COMPLETED = 4
        FAILED = 5
        self._so_state.send(packMsg(1, robot_status_task_req, {}))
        try:
            data = self._so_state.recv(16)
        except socket.timeout:
            return False
        jsonDataLen = 0
        if(len(data) < 16):
            print('pack head error')
            os.system('pause')
            self._so_state.close()
            quit()
        else:
            jsonDataLen = unpackHead(data)

        data = self._so_state.recv(1024)
        try:
            ret = json.loads(data)
        except:
            print('load back date to json error' + str(data))
            return False

        if(ret['task_status'] is COMPLETED and ret['target_id'] == landmark):
            return True
        if(ret['task_status'] is FAILED):
            print('Reach target failed, give up')
            return True
        else:
            print('[' + time.ctime()[11:19] + '] ' + str(ret) + '; target:' + landmark)
            return False

    def gotargetblock(self, point):
        demo.gotarget(point)
        time.sleep(0.5)
        while demo.reachtarget(point) is not True:
            time.sleep(0.5)
        print('Reach target: ' + point)


demo = BYDApi()



while True:

    demo.gotargetblock(landmark1)
    time.sleep(3)

    demo.gotargetblock(landmark2)

