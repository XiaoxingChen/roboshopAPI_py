# Robokit Netprotocol API
Python codes for Robokit Netprotocol Application Interface.

# Table of Contents

   * [Requirements](#requirements)
   * [Reference](#reference)
   * [Netprotocol Basic Definations](#netprotocol-basic-definations)
      * [API Type and Port](#api-type-and-port)
      * [Package and Unpackage of A Message](#package-and-unpackage-of-a-message)
    * [Examples](#examples)
       * [Let a Robot Turn Around](#let-a-robot-turn-around)

# Requirements

- Python 3.x

# Reference
[Robokit Netprotocol 1.4.2 by PDF](http://static.seer-robotics.com/robotkit-netprotocol-l-1.4.2.pdf)

[Robokit Netprotocol on github](https://github.com/seer-robotics/robokit_netprotocol_l)

# Netprotocol Basic Definations

[rbkNetProtoEnums.py](https://github.com/XiaoxingChen/roboshopAPI_py/blob/master/netprotocol/rbkNetProtoEnums.py) defines the rules of Robokit Netprotocol for packing method, unpacking method, request ID and TCP port of all connections.

It is a python achievement of:
## [API Type and Port](https://github.com/seer-robotics/robokit_netprotocol_l/blob/master/zh/chapter1/api_type.md)
```
API_PORT_ROBOD = 19200
API_PORT_STATE = 19204
API_PORT_CTRL = 19205
API_PORT_TASK = 19206
API_PORT_CONFIG = 19207
API_PORT_KERNEL = 19208
API_PORT_OTHER = 19210
```
## [Package and Unpackage of A Message](https://github.com/seer-robotics/robokit_netprotocol_l/blob/master/zh/chapter1/api_constitution.md)


Package:
```
packMsg(reqId, msgTyp, msg={})
```
Unpackage:
```
 unpackHead(data)
```

# Examples
## [Let a Robot Turn Around](https://github.com/XiaoxingChen/roboshopAPI_py/blob/master/rbkDemoTurn.py)
