import threading
# import concurrent.futures
import serial
import collections
import time
import joblib
import os
# from calGps import calGps
# from ubx import UBXManager
from mqtt_sub import readGps

relPos = collections.deque(maxlen=1)
refGps = collections.deque(maxlen=1)


relPos.append(
    (0, 0, 0)  # (e, n, u)
)

refGps.append(
    (25.018130, 121.545107, 0)  # (lat, lon, heith)
)


def readUwb():
    pass


def calRealPos(offset, pvt_obj):
    real_pos_obj = pvt_obj  # default
    return real_pos_obj


def readFixGps(gpsQue):
    templatePath = os.path.dirname(__file__)+'/template/'
    pvt_obj = joblib.load(templatePath + 'NAV-PVT_template.pkl')
    pvt_obj.lat = int(gpsQue[0][0]*10**7)
    pvt_obj.lon = int(gpsQue[0][1]*10**7)
    pvt_obj.height = int(gpsQue[0][2]*10**7)
    # print(pvt_obj)
    gpsQue.append(gpsQue)


if __name__ == '__main__':
    # th_gps = threading.Thread(
    #     target=readGps, args=[refGps], daemon=True)
    th_gps = threading.Thread(
        target=readFixGps, args=[refGps], daemon=True)
    th_uwb = threading.Thread(target=readUwb, daemon=True)
    th_gps.start()
    th_uwb.start()
    time.sleep(1)

    start_time = time.time()
    last_time = time.time()
    while True:
        t = time.time()
        if t - last_time > 0.2:
            last_time = t
            duration = t - start_time

            pvt_obj = refGps[0]
            print(duration,pvt_obj)
            offset = relPos[0]
            real_pos_obj = calRealPos(offset, pvt_obj)

            # do something
            # calc_position(lon, lat, d0, d1, d2, d3)
        else:
            time.sleep(0.01)
