import threading
# import concurrent.futures
import serial
import collections
import copy
import time
import joblib
import os
import pymap3d as pm
# from calGps import calGps
# from ubx import UBXManager
from readGps import readFixGps
from readGps import mqtt_readGps
from readGps import anchor_gps_2_anc_gps_q
from readGps import anc_gps_q_2_anchor_gps
from calUwb import UWBSimulate
from calUwb import UWBHardware


relPos = collections.deque(maxlen=1)  # [(e,n,u)]
anc_gps_q = collections.deque(maxlen=1)

relPos.append((0, 0, 0))

# (lat, lon, heith)
anchor_gps = [(25.02097, 121.54332, 0), (25.02208, 121.5346, 0), (
    25.01646, 121.53351, 0), (25.01531, 121.54184, 0)]
# anchor_gps = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]

anc_gps_q = anchor_gps_2_anc_gps_q(copy.deepcopy(anchor_gps)) #q stores ubx obj

def objGetGps(pvt_obj):
    return (pvt_obj.lat*10**-7, pvt_obj.lon*10**-7, pvt_obj.height*10**-7)

def calRealPos(offset, pvt_obj):
    real_pos_obj = pvt_obj  # default

    real_pos_obj.lat, real_pos_obj.lon, real_pos_obj.height = pm.enu2geodetic(
        offset[0], offset[1], offset[2], pvt_obj.lat*10**-7, pvt_obj.lon*10**-7, pvt_obj.height*10**-7)

    real_pos_obj.lat = int(real_pos_obj.lat*10**7)
    real_pos_obj.lon = int(real_pos_obj.lon*10**7)
    real_pos_obj.height = int(real_pos_obj.height*10**7)
    return real_pos_obj


if __name__ == '__main__':
    # If you want to run with fix GPS, just initialize 'anchor_gps'
    # No need to run readFixGps
    print('anchor_gps:', anchor_gps)
    print('anc_gps_q:', anc_gps_q)
    # th_gps = threading.Thread(
    #     target=mqtt_readGps, args=[anc_gps_q], daemon=True)
    # th_gps.start()
    
    uwbManager = UWBSimulate(relPos, os.path.dirname(
        __file__)+'/uwbData/UWB_dis_18_49_17.json', anchor_gps)
    # uwbManager = UWBHardware(relPos,'COM20', anchor_gps)
    uwbManager.start()
    time.sleep(1)

    # while True:
    #     print(anc_gps_q)
    #     time.sleep(1.)

    start_time = time.time()
    last_time = time.time()
    while True:
        t = time.time()
        if t - last_time > 1:
            last_time = t
            duration = t - start_time

            ref_pvt_obj = copy.deepcopy(anc_gps_q[0][0])
            # print('a0 position:',objGetGps(ref_pvt_obj))
            # print('anchor_gps:', anchor_gps)
            offset = relPos[0]
            # print(duration, ref_pvt_obj, offset)

            real_pos_obj = calRealPos(offset, ref_pvt_obj)
            print('Tag position:', 'lat:', real_pos_obj.lat*10**-7, 'lon:',
                  real_pos_obj.lon*10**-7, 'height:', real_pos_obj.height*10**-7)
            # print(anc_gps_q)
            # do something
            # calc_position(lon, lat, d0, d1, d2, d3)
        else:
            time.sleep(0.01)
