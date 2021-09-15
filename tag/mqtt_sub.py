import joblib
import datetime
import time
import json
import serial
import io
import paho.mqtt.client as mqtt
from ubx import UBXManager






# 當地端程式連線伺服器得到回應時，要做的動作
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # 將訂閱主題寫在on_connet中
    # 如果我們失去連線或重新連線時
    # 地端程式將會重新訂閱
    client.subscribe("gps")

# 當接收到從伺服器發送的訊息時要進行的動作



    
    

def readGps(gpsQue):
    def on_message(client, userdata, msg):
        print(msg.payload)
        bio = io.BytesIO(msg.payload)
        obj = joblib.load(bio)
        print(obj)
        gpsQue.append(gpsQue)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("192.168.0.107", 1883, 60)

    client.loop_forever()

