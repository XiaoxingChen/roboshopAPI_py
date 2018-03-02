from netprotocol.rbkNetProtoEnums import *
import json
import socket
import os
from time import sleep

so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so.settimeout(2)
so.connect(('192.168.4.235', API_PORT_STATE))
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
while True:
    setDO(ELECTRODE_DO_POS, True)
    sleep(0.01)
    setDO(ELECTRODE_DO_NEG, True)
    sleep(0.5)

    setDO(ELECTRODE_DO_POS, False)
    sleep(0.01)
    setDO(ELECTRODE_DO_NEG, False)
    sleep(0.5)

    cnt += 1
    print('Loop count = %d' % cnt)

os.system('pause')
so.close()
