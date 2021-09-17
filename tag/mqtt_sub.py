import joblib
import datetime
import time
import json
import serial
import io
import paho.mqtt.client as mqtt
from ubx import UBXManager






# # 當地端程式連線伺服器得到回應時，要做的動作
# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code "+str(rc))

#     # 將訂閱主題寫在on_connet中
#     # 如果我們失去連線或重新連線時
#     # 地端程式將會重新訂閱
#     client.subscribe("gps")


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # 將訂閱主題寫在on_connet中
    # 如果我們失去連線或重新連線時
    # 地端程式將會重新訂閱
    # client.subscribe("gps")

    client.subscribe("gps/a0")
    client.subscribe("gps/a1")
    client.subscribe("gps/a2")
    client.subscribe("gps/a3")


def readGps(gpsQue):
    def on_message(client, userdata, msg):
        # print('msg:',msg.topic)
        bio = io.BytesIO(msg.payload)
        obj = joblib.load(bio)
        anchor_list = gpsQue[0]
        if msg.topic == "gps/a0":
            anchor_list[0] = obj
            gpsQue.append(anchor_list)
        # print(obj)
        

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("192.168.0.106", 1883, 60)

    client.loop_forever()

