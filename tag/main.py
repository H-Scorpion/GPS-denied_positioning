import threading
# import concurrent.futures
import serial
import collections
import copy
import time
import joblib
import json
import datetime
import os
import pymap3d as pm
# from calGps import calGps
# from ubx import UBXManager
from auxiliary import objGetGps
from auxiliary import anchor_gps_2_anc_gps_q
from auxiliary import anc_gps_q_2_anchor_gps

# from readGps import readFixGps
# from readGps import mqtt_readGps
from calUwb import UWBSimulate
from calUwb import UWBHardware
from calUwb import UWBSimulate_enuGPS


relPos = collections.deque(maxlen=1)  # [(e,n,u)]
anc_gps_q = collections.deque(maxlen=1)

relPos.append((0, 0, 0))

# (lat, lon, heith)
# anchor_gps = [(25.02097, 121.54332, 0), (25.02208, 121.5346, 0), (
#     25.01646, 121.53351, 0), (25.01531, 121.54184, 0)]

# BL experiment ===========================
# anchor_gps = [(25.019742599999997, 121.5423204, 0.0084209), (25.0195689, 121.54227569999999, 0.0063062),
#               (25.019144299999997, 121.54208469999999, 0.0131656), (25.019026099999998, 121.5423699, 0.0106915)]
# anchor_gps = [(25.01941, 121.54243, 1.3), (25.01941, 121.54236, 1.3),
#               (25.01915, 121.54237, 1.3), (25.01915, 121.54244, 1.3)]
# anchor_enu = [(0, 0, 0), (-6, 0, 0), (-6, -29, 0), (0, -29, 0)]

# EE2 UWB exp ==========
anchor_gps =[(25.01871570076376, 121.5414674130481, 3.000000000735832), 
            (25.018740399874826, 121.5414674130481, 3.000000590359914), 
            (25.018740399873735, 121.54148548411611, 3.000000849311539), 
            (25.018715700762662, 121.5414854841125, 3.000000259884392)]
# anchor_gps = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]

anc_gps_q = anchor_gps_2_anc_gps_q(
    copy.deepcopy(anchor_gps))  # q stores ubx obj


def calRealPos(offset, pvt_obj):
    real_pos_obj = pvt_obj  # default

    real_pos_obj.lat, real_pos_obj.lon, real_pos_obj.height = pm.enu2geodetic(
        offset[0], offset[1], offset[2], pvt_obj.lat*10**-7, pvt_obj.lon*10**-7, pvt_obj.height*10**-7)

    real_pos_obj.lat = int(real_pos_obj.lat*10**7)
    real_pos_obj.lon = int(real_pos_obj.lon*10**7)
    real_pos_obj.height = int(real_pos_obj.height*10**7)
    real_pos_obj.pDOP = 1
    real_pos_obj.numSV = 15
    
    return real_pos_obj


def sendObj2FC(obj, ser):
    serialized = real_pos_obj.serialize()
    ser.write(serialized)


if __name__ == '__main__':
    # If you want to run with fix GPS, just initialize 'anchor_gps'
    # No need to run readFixGps
    with open("connection_data.json",'r') as f:
        connection_data = json.load(f)[0]
        serCom2FC = connection_data['fc_ttl_com']
        tag_com = connection_data['tag_com']

    isSending2FC = True
    tagPosData = []
    if isSending2FC:
        ser = serial.Serial(serCom2FC, 230400, timeout=None) #imprtant! 230400

    print('initial data:')
    print('anchor_gps:', anchor_gps)
    print('-------------------------------')
    # print('anc_gps_q:', anc_gps_q)
    # th_gps = threading.Thread(
    #     target=mqtt_readGps, args=[anc_gps_q], daemon=True)
    # th_gps.start()
    # uwbManager = UWBSimulate_enuGPS(relPos, os.path.join(os.path.dirname(
    #     __file__), './uwbData/GPSDe_UWB_dis_robot.json'), anchor_gps,anchor_enu)
    uwbManager = UWBHardware(relPos, tag_com, anc_gps_q)
    uwbManager.start()
    time.sleep(1)

    start_time = time.time()
    last_time = time.time()

    try:
        while True:
            t = time.time()
            if t - last_time > 0.15:
                print(t - last_time)
                last_time = t
                duration = t - start_time

                ref_pvt_obj = copy.deepcopy(anc_gps_q[0][0])
                # print('a0 position:', objGetGps(ref_pvt_obj))
                # print('anchor_gps:', anchor_gps)
                offset = relPos[0]
                # print(duration, ref_pvt_obj, offset)
                print('offset:', offset)
                real_pos_obj = calRealPos(offset, ref_pvt_obj)
                # print('Tag position:', 'lat:', real_pos_obj.lat*10**-7, 'lon:',
                #       real_pos_obj.lon*10**-7, 'height:', real_pos_obj.height*10**-7)
                print('Tag position:', objGetGps(real_pos_obj))
                tagPosData.append([time.time(), real_pos_obj, offset])
                # print(anc_gps_q)
                # calc_position(lon, lat, d0, d1, d2, d3)
                if isSending2FC:
                    sendObj2FC(real_pos_obj, ser)

            else:
                time.sleep(0.01)
    except KeyboardInterrupt:
        uwbManager.stop()
    # filename = f'tagPosData_{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}.pkl'
    # joblib.dump(tagPosData, filename)
