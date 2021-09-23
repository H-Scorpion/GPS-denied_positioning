import joblib
import datetime
import copy
import time
import json
import serial
import io
import os
import collections
import paho.mqtt.client as mqtt
from ubx import UBXManager
from auxiliary import objGetGps
from auxiliary import anchor_gps_2_anc_gps_q
from auxiliary import anc_gps_q_2_anchor_gps

def readFixGps(gpsQue):
    """Write 4 anchor gps to queue

    Args:
        gpsQue (deque): maxlen = 1, contains a 4*3 list, 4 anchor each has (lat, lon, height) 
    """
    print('gpsQue in readFix:', gpsQue)
    templatePath = os.path.dirname(__file__)+'/template/'
    anchor_list = gpsQue[0]

    for i in range(4):
        pvt_obj = joblib.load(templatePath + 'NAV-PVT_template.pkl')
        pvt_obj.lat = int(gpsQue[0][i][0]*10**7)
        pvt_obj.lon = int(gpsQue[0][i][1]*10**7)
        pvt_obj.height = int(gpsQue[0][i][2]*10**7)
        anchor_list[i] = pvt_obj
    gpsQue.append(anchor_list)



def mqtt_readGps(gpsQue):
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("gps/a0")
        client.subscribe("gps/a1")
        client.subscribe("gps/a2")
        client.subscribe("gps/a3")

    def on_message(client, userdata, msg):
        print('msg:', msg.topic)
        bio = io.BytesIO(msg.payload)
        obj = joblib.load(bio)
        anchor_list = gpsQue[0]
        if msg.topic == "gps/a0":
            anchor_list[0] = obj
        elif msg.topic == "gps/a1":
            anchor_list[1] = obj
        elif msg.topic == "gps/a2":
            anchor_list[2] = obj
        elif msg.topic == "gps/a3":
            anchor_list[3] = obj
        print('readGps a0 gps:', objGetGps(anchor_list[0]), '\nreadGps a1 gps:', objGetGps(
            anchor_list[1]), '\nreadGps a2 gps:', objGetGps(anchor_list[2]), '\nreadGps a3 gps:', objGetGps(anchor_list[3]))
        gpsQue.append(anchor_list)
        # print(obj)

    with open(os.path.dirname(__file__)+'/brokerIP.txt') as f:
        brokerIP = f.read()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(brokerIP, 1883, 60)
    print('connected to broker')
    client.loop_forever()


if __name__ == '__main__':
    anchor_gps = [(25.02097, 121.54332, 0), (25.02208, 121.5346, 0), (
        25.01646, 121.53351, 0), (25.01531, 121.54184, 0)]
    anc_gps_q = anchor_gps_2_anc_gps_q(anchor_gps)
    # print(anc_gps_q)
    new_anchor_gps = anc_gps_q_2_anchor_gps(anc_gps_q)
    print(new_anchor_gps)
