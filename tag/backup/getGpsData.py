# Read GPS obj data and save as pkl file
# Can replay GPS obj Data in replay_pkl.py 
# to emulate GPS signal for mission planner

import joblib
import datetime
import time
import json
import serial
from ubx import UBXManager

filename = f'./gpsData/ubxPacket_{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}'
obj_id_to_attrs = {}

def obj_to_dict(obj):
    try:
        attrs = obj_id_to_attrs[obj._id]
    except KeyError:
        attrs = obj_id_to_attrs[obj._id] = [k for k in obj.Fields.__dict__.keys() if not k.startswith('__')]
    return {attr: getattr(obj, attr, 'No Data') for attr in attrs}


def my_onUBX(obj):
    duration = time.time() - timestamp_start

    print(duration, obj)

    all_recv.append(
        {'time': duration, 'obj': obj, 'timestamp': datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}
    )
    all_recv_obj.append(obj)


def my_onUBXError(msgClass, msgId, errMsg):
    print(msgClass, msgId, errMsg)


if __name__ == '__main__':
    with open("connection_data.json", 'r') as f:  # os.path.dirname(__file__)+'/uwbData/UWB_dis_18_49_17.json'
        connection_data = json.load(f)[0]
        comPort = connection_data["get_gps_com"]
    ser = serial.Serial(comPort, 115200, timeout=None)
    manager = UBXManager(ser, debug=False, eofTimeout=3.)

    manager.onUBX = my_onUBX
    manager.onUBXError = my_onUBXError

    timestamp_start = time.time()
    all_recv = []
    all_recv_obj = []
    manager.start()

    try:
        while True:
            time.sleep(1.)
    except KeyboardInterrupt:
        print('KeyboardInterrupt detected. Shutdown...')
    finally:
        manager.shutdown()
        joblib.dump(all_recv, filename + '.pkl')
        joblib.dump(all_recv_obj, filename + '_pure_obj.pkl')