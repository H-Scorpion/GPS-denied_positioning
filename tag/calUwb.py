# -*- coding: UTF-8 -*-
import serial
import glob
import copy
import json
import threading
import collections
import datetime
import time
import os
import numpy as np
import pymap3d as pm
import collections
from auxiliary import anc_gps_q_2_anchor_gps
from datetime import datetime
from distance2Position import costfun_method

distanceQ = collections.deque(maxlen=1)

# class UWBBase():
#     def __init__(self):
#         self.


class UWBHardware():
    def __init__(self, offsetQ, comport, anchor_gps_q, baudrate=115200, timeout=0.01,):
        self.ser = serial.Serial(comport, baudrate=baudrate, timeout=timeout)
        self.is_run = threading.Event()
        self.distanceData = [0, 0, 0, 0]
        self.anchor_gps_q = anchor_gps_q
        self.anchor_gps = copy.deepcopy(
            anc_gps_q_2_anchor_gps(anchor_gps_q))  # gps list
        self.anchorPosition_enu = []
        self.offsetQ = offsetQ
        self.uwbDataList = []
        self.start_time = time.time()
        # self.recordDistanceData = []

    def gps2enu_list(self, anchorPosition_gps):
        print(anchorPosition_gps)
        anchorPosition_enu = [(0, 0, 0)]
        refPointGps = anchorPosition_gps[0]
        for i in range(1, len(anchorPosition_gps)):
            # print(anchorPosition_gps[i][0])
            enu = pm.geodetic2enu(anchorPosition_gps[i][0], anchorPosition_gps[i][1],
                                  anchorPosition_gps[i][2], refPointGps[0], refPointGps[1], refPointGps[2])
            anchorPosition_enu.append(enu)
        # print(anchorPosition_enu)
        self.anchorPosition_enu = anchorPosition_enu

    def onUwb(self, rx_1):
        self.anchor_gps = copy.deepcopy(
            anc_gps_q_2_anchor_gps(self.anchor_gps_q))
        # update anchorPosition_enu
        self.gps2enu_list(self.anchor_gps)
        duration = time.time()-self.start_time

        dec_rx1 = rx_1.decode('utf-8')
        if(dec_rx1 != ' ' and dec_rx1.find('mc') >= 0):
            dis_ = dec_rx1.split(' ')
            dis = np.array([(int(dis_[2],16)),(int(dis_[3],16)), (int(dis_[4],16)), (int(dis_[5],16))])/1000.0
            print(dis) # meter



        # data = str(rx_1).split(' ')
        # data = rx_1.split(' ')
        # print('Data:', data)
        print()
        # print('---Time---: ', duration)
        # print('data: ', data)
        # d0, d1, d2, d3 = data[2].split(',')[0], data[3].split(
        #     ',')[0], data[4].split(',')[0], data[5].split(',')[1]
        # dis = [int(d0)/1000, int(d1)/1000, int(d2)/1000, int(d3)/1000]
        # print('dis:',dis)

        # d0, d1, d2, d3 = int(data[2], 16), int(
        #     data[3], 16), int(data[4], 16), int(data[5], 16)
        # dis = [d0, d1, d2, d3]
        distanceQ.append(dis)
        # print('dis:', dis)
        recv_data_dic = {'time': duration, 'dis': dis,'timestamp': datetime.now().strftime("%Y%m%d-%H%M%S%f")}
        self.uwbDataList.append(
            recv_data_dic)
        self.distanceData = dis
        # print('anchor_gps:', self.anchor_gps)
        print('distanceData:', self.distanceData)
        # print('anchorPosition_enu:', self.anchorPosition_enu)
        offset = costfun_method(self.distanceData, self.anchorPosition_enu)
        # print('offset:',offset)
        self.offsetQ.append(offset)
        # self.recordDistanceData.append()

    def run(self):
        fi_num = datetime.now().strftime("%H_%M_%S")
        self.start_time = time.time()
        while self.is_run.is_set():
            rx_1 = self.ser.readline()

            if(len(rx_1) >= 20 and 'mc' in str(rx_1)):
                self.onUwb(rx_1)
            time.sleep(0.2)

    def start(self):
        self.is_run.set()
        threading.Thread(target=self.run, daemon=True).start()

    def stop(self):
        self.is_run.clear()
        self.ser.close()
        filename = os.path.dirname(__file__)+'/uwbData/UWB_dis_' + datetime.now().strftime("%Y%m%d-%H%M%S") + '.json'
        with open(filename, 'a') as fout:
            json.dump(self.uwbDataList, fout)
        print('finish dumping ubx json data.')


class UWBSimulate():
    def __init__(self, offsetQ, filename, anchor_gps):
        self.is_run = threading.Event()
        self.distanceData = [0, 0, 0, 0]
        self.anchor_gps = copy.deepcopy(anchor_gps)
        self.anchorPosition_enu = []
        self.offsetQ = offsetQ
        with open(filename, 'r') as f:  # os.path.dirname(__file__)+'/uwbData/UWB_dis_18_49_17.json'
            self.allUwb = json.load(f)
        # print(self.allUwb)

    def metadata_initialize(self, anchorPosition_gps):
        print(anchorPosition_gps)
        anchorPosition_enu = [(0, 0, 0)]
        refPointGps = anchorPosition_gps[0]
        for i in range(1, len(anchorPosition_gps)):
            # print(anchorPosition_gps[i][0])
            enu = pm.geodetic2enu(anchorPosition_gps[i][0], anchorPosition_gps[i][1],
                                  anchorPosition_gps[i][2], refPointGps[0], refPointGps[1], refPointGps[2])
            anchorPosition_enu.append(enu)
        print('metadata_initialize:anchorPosition_enu:\n', anchorPosition_enu)
        self.anchorPosition_enu = anchorPosition_enu

    def uwbReplay(self):
        # print('uwbReplay, self',self.anchor_gps)
        # print(self.anchor_gps)
        self.metadata_initialize(self.anchor_gps)
        start_time = time.time()
        for uwb in self.allUwb:
            timestamp = float(uwb['time'])
            while time.time()-start_time < timestamp:
                time.sleep(0.01)
            try:
                self.onUwb(uwb)
            except Exception as e:
                print(e)
                self._onUwb(uwb)
        self.stop()

    def _onUwb(self, uwb):
        print(uwb)

    def onUwb(self, uwb):
        # print(uwb)
        self.distanceData = [float(i)/1000 for i in uwb['dis'][:4]]
        offset = costfun_method(self.distanceData, self.anchorPosition_enu)
        # print('offset:',offset)
        self.offsetQ.append(offset)

    def start(self):
        self.is_run.set()
        threading.Thread(target=self.uwbReplay, daemon=True).start()

    def stop(self):
        self.is_run.clear()


class UWBSimulate_enuGPS(UWBSimulate):
    def __init__(self, offsetQ, filename, anchor_gps,anchor_enu):
        super().__init__(offsetQ, filename, anchor_gps)
        self.anchorPosition_enu = anchor_enu

    def metadata_initialize(self, anchorPosition_gps):
        # self.anchorPosition_enu = self.anchorPosition_enu
        print('UWBSimulate_enuGPS:metadata_initialize')




if __name__ == '__main__':
    uwbmanager = UWBSimulate(os.path.dirname(
        __file__)+'/uwbData/UWB_dis_18_49_17.json')
    print(uwbmanager)
    uwbmanager.start()
    while True:
        time.sleep(1.)
        print(uwbmanager.distanceData)
        # except KeyboardInterrupt:
        #     # print(e)
        #     uwbmanager.stop()
        #     print('uwbmanager.stop()')

    # readUwb()
    # uwbSimulate()
    # calOffset(distanceQ)
    # start_time = time.time
    # myTime = datetime.strptime('18:05:36','%H:%M:%S').time()
    # newTime = datetime.strptime('18:20:36','%H:%M:%S').time()
    # c = newTime - myTime
    # print(newTime - myTime)
