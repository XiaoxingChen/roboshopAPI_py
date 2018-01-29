from rbkNetProtoEnums import *
import rbkNetProtoEnums
import json
import socket
import os
import struct
import time
import sys

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# so.connect(('192.168.4.109', API_PORT_STATE))
so.connect(('192.168.192.5', API_PORT_STATE))

preliftpoint = 'LM7'
liftpoint = 'LM6'
releasepoint = 'LM8'
afterreleasepoint = 'LM12'

SUSPENDED = 3
COMPLETED = 4
FIXED_PATH = 3

preliftstate = {'task_status': COMPLETED, 'task_type': FIXED_PATH,
                'target_id': preliftpoint}
liftstate = {'task_status': COMPLETED, 'task_type': FIXED_PATH,
             'target_id': liftpoint}
releasestate = {'task_status': COMPLETED, 'task_type': FIXED_PATH,
                'target_id': releasepoint}
afterreleasestate = {'task_status': COMPLETED, 'task_type': FIXED_PATH,
                     'target_id': afterreleasepoint}


def statematch(rbkstate):
    if(rbkstate['task_status'] is not COMPLETED or rbkstate['task_type'] is not FIXED_PATH):
        return None

    if(rbkstate['target_id'] == preliftstate['target_id']):
        print('Current rbkstate: wait to prelift')
        return 'prelift'
    elif(rbkstate['target_id'] == liftstate['target_id']):
        print('Current rbkstate: wait to lift')
        return 'lift'
    elif(rbkstate['target_id'] == releasestate['target_id']):
        print('Current rbkstate: wait to release')
        return 'release'
    elif(rbkstate['target_id'] == afterreleasestate['target_id']):
        print('Current rbkstate: wait to lift')
        return 'lift'
    else:
        print('Current rbkstate: None')
        return None


F4kCommandPort = 15003
F4kAddr = ('192.168.192.4', F4kCommandPort)
# F4kAddr = ('127.0.0.1', F4kCommandPort)
PALLET_PACK_HEAD = 0x0000103A
PALLET_LIFT = 0x01
PALLET_RELEASE = 0x02


def palletctrl(act):
    sof4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sof4.settimeout(0.03)
    msg = struct.pack('<2I', PALLET_PACK_HEAD, act)
    sof4.sendto(msg, F4kAddr)
    sof4.close()


while True:
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
    currstate = statematch(ret)
    if currstate is 'prelift':
        palletctrl(PALLET_RELEASE)
        time.sleep(1)
    elif currstate is 'lift':
        palletctrl(PALLET_LIFT)
        time.sleep(1)
    elif currstate is 'release':
        palletctrl(PALLET_RELEASE)
        time.sleep(1)
    else:
        time.sleep(0.5)
        print('[' + time.ctime()[11:19] + '] ' + str(ret))

os.system('pause')
so.close()
