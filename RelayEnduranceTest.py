from netprotocol.rbkNetProtoEnums import *
import json
import socket
import os
from time import sleep

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
<<<<<<< HEAD
so.settimeout(3)
so.connect(('192.168.4.235', API_PORT_OTHER))
# so.connect(('192.168.137.1', API_PORT_OTHER))
=======
so.settimeout(2)
so.connect(('192.168.4.235', API_PORT_STATE))
>>>>>>> c9c0f79bd63194350c093f6b46d143df9e82cb37
# so.connect(('192.168.192.5', API_PORT_OTHER))

ELECTRODE_DO_POS = 15
ELECTRODE_DO_NEG = 14


def setDO(id, polar):
    so.send(packMsg(1, robot_other_setdo_req, {"id": id, "status": polar}))
    data = so.recv(16)
    jsonDataLen = 0
    if(len(data) < 16):
        print('pack head error')
        os.system('pause')
        so.close()
        quit()
    else:
        jsonDataLen = unpackHead(data)[0]


cnt = 0

micro_dt = 0.01

continue_dt = 1

while True:
    setDO(ELECTRODE_DO_POS, True)
    sleep(micro_dt)
    setDO(ELECTRODE_DO_NEG, True)
    sleep(continue_dt)

    setDO(ELECTRODE_DO_POS, False)
    sleep(micro_dt)
    setDO(ELECTRODE_DO_NEG, False)
    sleep(continue_dt)

    cnt += 1
    print('Loop count = %d' % cnt)

os.system('pause')
so.close()
