import json
import struct

API_PORT_ROBOD = 19200
API_PORT_STATE = 19204
API_PORT_CTRL = 19205
API_PORT_TASK = 19206
API_PORT_CONFIG = 19207
API_PORT_KERNEL = 19208
API_PORT_OTHER = 19210

robot_status_info_req = 1000
robot_status_run_req = 1002
robot_status_mode_req = 1003
robot_status_loc_req = 1004
robot_status_speed_req = 1005
robot_status_area_req = 1011
robot_status_io_res = 1013
robot_status_task_req = 1020
robot_status_all1_req = 1100
robot_status_alarm_res = 1050

robot_control_reloc_req = 2002
robot_control_motion_req = 2010

robot_task_gotarget_req = 3051

robot_daemon_ls_req = 5100
robot_daemon_scp_req = 5101
robot_daemon_rm_req = 5102

robot_other_setdo_req = 6001


# 0x5A + Version + serierNum + jsonLen + reqNum + rsv
PACK_HEAD_FMT_STR = '!BBHLH6s'
PACK_RSV_DATA = b'\x00\x00\x00\x00\x00\x00'


def packMsg(reqId, msgTyp, msg={}):
    msgLen = 0
    jsonStr = json.dumps(msg)
    if(msg != {}):
        msgLen = len(jsonStr)
    rawMsg = struct.pack(PACK_HEAD_FMT_STR, 0x5A, 1, reqId,
                         msgLen, msgTyp, PACK_RSV_DATA)
    if(msg != {}):
        rawMsg += bytearray(json.dumps(msg), 'ascii')
    return rawMsg


def unpackHead(data):
    result = struct.unpack(PACK_HEAD_FMT_STR, data)
    jsonLen = result[3]
    reqNum = result[4]

    return (jsonLen, reqNum)
