import joblib
import datetime
import time
import json
import serial
import io
import paho.mqtt.client as mqtt
from ubx import UBXManager


def readGps(mqtt_client):

    def my_onUBX(obj):
        print(obj)
        bio = io.BytesIO()
        joblib.dump(obj, bio)
        data = bio.getvalue()
        mqtt_client.publish('gps',data)

    def my_onUBXError(msgClass, msgId, errMsg):
        print(msgClass, msgId, errMsg)

    comPort = 'COM11'
    ser = serial.Serial(comPort, 115200, timeout=None)

    manager = UBXManager(ser, debug=True, eofTimeout=3.)

    manager.onUBX = my_onUBX
    manager.onUBXError = my_onUBXError    
    
    manager.start()
    print('hi')

    try:
        while True:
            time.sleep(1.)
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    finally:
        print('manager.shutdown()')
        manager.shutdown()

# readGps('COM16')

if __name__=='__main__':
    client = mqtt.Client()
    client.connect("192.168.0.107", 1883, 60)
    readGps(client)
