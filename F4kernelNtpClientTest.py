from rbkNetProtoEnums import *
import rbkNetProtoEnums
import json
import socket
import os
import time


def checkNtpLossWarning():
    so.send(packMsg(1, robot_status_alarm_res, {}))
    try:
        data = so.recv(16)
    except socket.timeout:
        print('timeout')

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
    # print(ret)
    warningdict = ret['warnings']
    findNtpLossWarning = False
    # print(warningdict)
    for d in warningdict:
        if('54005' in d):
            findNtpLossWarning = True

    return findNtpLossWarning


so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#so.connect(('192.168.4.59', API_PORT_STATE))
so.connect(('127.0.0.1', API_PORT_STATE))
so.settimeout(20)

print('Cut NTP server')
os.system('net stop w32Time')
cnt = 30
while cnt > 0:
    cnt = cnt - 1
    print('wait %d seconds to check warning' % cnt)
    time.sleep(1)
    if checkNtpLossWarning():
        break

if checkNtpLossWarning():
    print('NTP cut test passed...')
else:
    print('NTP cut test failed!!!')

os.system('net start w32Time')

if not checkNtpLossWarning():
    print('NTP recover test passed...')
else:
    print('NTP recover test failed...')

so.close()
