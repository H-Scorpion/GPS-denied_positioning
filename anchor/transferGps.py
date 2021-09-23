import argparse
import joblib
import datetime
import time
import json
import serial
import io
import paho.mqtt.client as mqtt
from ubx import UBXManager

def parseArg():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', default='a0')
    parser.add_argument('-i', default='192.168.0.116')
    args = parser.parse_args()
    return args


def readGps(mqtt_client,anchor):

    def my_onUBX(obj):
        print(obj)
        if obj._id == 0x07:
            bio = io.BytesIO()
            joblib.dump(obj, bio)
            data = bio.getvalue()
            mqtt_client.publish('gps/'+anchor,data)

    def my_onUBXError(msgClass, msgId, errMsg):
        print(msgClass, msgId, errMsg)

    # comPort = '/dev/ttyUSB0'
    comPort = 'COM12'
    ser = serial.Serial(comPort, 115200, timeout=None)

    manager = UBXManager(ser, debug=True, eofTimeout=3.)

    manager.onUBX = my_onUBX
    manager.onUBXError = my_onUBXError    
    
    manager.start()
    print('manager started...')

    try:
        while True:
            time.sleep(1.)
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    finally:
        manager.shutdown()
        print('manager.shutdown()')
        

# readGps('COM16')

if __name__=='__main__':
    args = parseArg()
    brokerIP = args.i
    anchor = args.a
    # print(brokerIP)
    client = mqtt.Client()
    client.connect(brokerIP, 1883, 60)
    readGps(client,anchor)
