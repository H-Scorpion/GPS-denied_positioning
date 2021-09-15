import joblib
import datetime
import time
import json
import serial
from ubx import UBXManager


def readGps(gpsQue):

    def my_onUBX(obj):
        gpsQue.append(obj)

    def my_onUBXError(msgClass, msgId, errMsg):
        print(msgClass, msgId, errMsg)

    comPort = 'COM11'
    ser = serial.Serial(comPort, 115200, timeout=None)

    manager = UBXManager(ser, debug=True, eofTimeout=3.)

    manager.onUBX = my_onUBX
    manager.onUBXError = my_onUBXError    
    
    manager.start()

    try:
        while True:
            time.sleep(1.)
    finally:
        print('manager.shutdown()')
        manager.shutdown()

# readGps('COM16')