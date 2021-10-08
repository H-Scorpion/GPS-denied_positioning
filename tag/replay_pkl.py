import time
import serial
import joblib
import os
import json
from auxiliary import objGetGps

# filename ='./gpsData/demoGps.pkl'
# filename ='./gpsData/ubxPacket_20210901-165743.pkl'
# filename ='fakeGps.pkl'
filename ='./gpsData/ubxPacket_20211001-164456.pkl'

all_objs = joblib.load(filename)

with open("connection_data.json", 'r') as f:  # os.path.dirname(__file__)+'/uwbData/UWB_dis_18_49_17.json'
    connection_data = json.load(f)[0]
    comPort = connection_data["fc_ttl_com"]

ser = serial.Serial(comPort, 115200, timeout=None)

timestamp_start = time.time()


for data in all_objs:
    duration = data['time']
    obj = data['obj']
    timestamp = data['timestamp']

    while (time.time() - timestamp_start) < duration:
        time.sleep(0.001)
        
        



    try: 
        if obj._id ==7:
            serialized = obj.serialize()
            ser.write(serialized)
            print('exact_time:',timestamp)
            print(duration, 'sent:', len(serialized))
            print(objGetGps(obj))
            # print(obj)
    except TabError:
        continue
