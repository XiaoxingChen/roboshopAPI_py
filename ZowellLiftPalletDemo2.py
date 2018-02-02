from rbkNetProtoEnums import packMsg
from rbkNetProtoEnums import unpackHead
from rbkNetProtoEnums import *
import rbkNetProtoEnums
import json
import socket
import os
import struct
import time
import sys


prepoint = ['LM3', 'LM4']
workpoint = ['LM1', 'LM2']


class ZowellApi(object):
    PALLET_LIFT = 0x01
    PALLET_RELEASE = 0x02

    def __init__(self):
        self._rbkip = '192.168.192.5'
        self._f4addr = ('192.168.192.4', 15003)

        self._so_state = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._so_state.settimeout(3)
        self._so_state.connect((self._rbkip, API_PORT_STATE))

        self._so_task = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._so_task.settimeout(0.5)
        self._so_task.connect((self._rbkip, API_PORT_TASK))

        self._so_f4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._so_f4.settimeout(0.5)
        try:
            self._so.sendto(b'', self._f4addr)
        except:
            pass

    def gotarget(self, landmark):
        self._so_task.send(
            packMsg(1, robot_task_gotarget_req, {"id": landmark}))

    def reachtarget(self):
        COMPLETED = 4
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
        ret = json.loads(data)
        if(ret['task_status'] is COMPLETED):
            return True
        else:
            print('[' + time.ctime()[11:19] + '] ' + str(ret))
            return False

    def gotargetblock(self, point):
        demo.gotarget(point)
        time.sleep(0.5)
        while demo.reachtarget() is not True:
            time.sleep(0.5)

    def ctrlpallet(self, act):
        PALLET_PACK_HEAD = 0x0000103A
        msg = struct.pack('<2I', PALLET_PACK_HEAD, act)
        self._so_f4.sendto(msg, self._f4addr)

    def gopointcontrolpallet(self, point, action):
        demo.gotarget(point)
        time.sleep(0.5)
        while demo.reachtarget() is not True:
            time.sleep(0.5)
        demo.ctrlpallet(action)
        time.sleep(5)
        print('reach point:' + point)


demo = ZowellApi()
demo.ctrlpallet(ZowellApi.PALLET_LIFT)

direction = True


def home():
    if direction:
        return 1
    else:
        return 0


def dest():
    if direction:
        return 0
    else:
        return 1


while True:

    demo.gopointcontrolpallet(prepoint[dest()], ZowellApi.PALLET_RELEASE)
    print('Reach prepoint, release pallet')

    demo.gopointcontrolpallet(workpoint[dest()], ZowellApi.PALLET_LIFT)
    print('Reach workpoint, lift pallet')

    demo.gopointcontrolpallet(workpoint[home()], ZowellApi.PALLET_RELEASE)
    print('Reach home, release pallet')

    demo.gopointcontrolpallet(prepoint[home()], ZowellApi.PALLET_LIFT)
    print('Leave home, lift pallet')

    demo.gotargetblock(prepoint[dest()])
    print('ddddd')

    direction = not direction
