import threading
# import concurrent.futures
import serial
import collections
import time
import joblib
import os
import pymap3d as pm
# from calGps import calGps
# from ubx import UBXManager
from mqtt_sub import readGps
from calUwb import UWBSimulate


relPos = collections.deque(maxlen=1)
refGps = collections.deque(maxlen=1)

anchor_gps = [(25.02097, 121.54332, 0), (25.02208, 121.5346, 0), (
    25.01646, 121.53351, 0), (25.01531, 121.54184, 0)]

relPos.append(
    (0, 0, 0)  # (e, n, u)
)

refGps.append(
    anchor_gps[0]
    # (lat, lon, heith)
)

# a0:25.017808099461927, 121.54450303082434
# a1:25.01798327478762, 121.54427409377229
# a2:25.017893345724577, 121.54415342667595
# a3:25.0177143806361, 121.54435981418773


def readUwb():
    pass


def calRealPos(offset, pvt_obj):
    real_pos_obj = pvt_obj  # default

    real_pos_obj.lat, real_pos_obj.lon, real_pos_obj.height = pm.enu2geodetic(
        offset[0], offset[1], offset[2], pvt_obj.lat*10**-7, pvt_obj.lon*10**-7, pvt_obj.height*10**-7)

    real_pos_obj.lat =int(real_pos_obj.lat*10**7)
    real_pos_obj.lon =int(real_pos_obj.lon*10**7)
    real_pos_obj.height =int(real_pos_obj.height*10**7)
    return real_pos_obj


def readFixGps(gpsQue):
    templatePath = os.path.dirname(__file__)+'/template/'
    pvt_obj = joblib.load(templatePath + 'NAV-PVT_template.pkl')
    pvt_obj.lat = int(gpsQue[0][0]*10**7)
    pvt_obj.lon = int(gpsQue[0][1]*10**7)
    pvt_obj.height = int(gpsQue[0][2]*10**7)
    # print(pvt_obj)
    gpsQue.append(pvt_obj)


if __name__ == '__main__':
    # th_gps = threading.Thread(
    #     target=readGps, args=[refGps], daemon=True)
    th_gps = threading.Thread(
        target=readFixGps, args=[refGps], daemon=True)
    th_gps.start()
    uwbManager = UWBSimulate(relPos, os.path.dirname(
        __file__)+'/uwbData/UWB_dis_18_49_17.json', anchor_gps)
    uwbManager.start()
    time.sleep(1)

    start_time = time.time()
    last_time = time.time()
    while True:
        t = time.time()
        if t - last_time > 0.2:
            last_time = t
            duration = t - start_time

            pvt_obj = refGps[0]
            offset = relPos[0]
            print(duration, pvt_obj, offset)

            real_pos_obj = calRealPos(offset, pvt_obj)
            print(real_pos_obj.lat,real_pos_obj.lon,real_pos_obj.height)
            # do something
            # calc_position(lon, lat, d0, d1, d2, d3)
        else:
            time.sleep(0.01)
