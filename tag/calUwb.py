# -*- coding: UTF-8 -*-
import serial
import glob
import json
import threading
import collections
import datetime
import time
import os
import numpy as np
import pymap3d as pm
import collections
from datetime import datetime
from distance2Position import costfun_method

distanceQ = collections.deque(maxlen=1)

# class UWBBase():
#     def __init__(self):
#         self.

class UWBHardware():
    def __init__(self, comport, baudrate=9600, timeout=0.01):
        self.ser = serial.Serial(comport, baudrate=baudrate, timeout=timeout)
        self.is_run = threading.Event()
        self.distanceData = [0,0,0,0]

    def run(self):
        fi_num = datetime.now().strftime("%H_%M_%S")
        uwbDataList = []
        start_time = time.time()

        while self.is_run.is_set():
            rx_1 = self.ser.readline()
            try:                
                if(len(rx_1) >= 20 and 'mc' in str(rx_1)):
                    timestamp = time.time()-start_time
                    data = str(rx_1).split(' ')
                    print()
                    print('---Time---: ', timestamp)
                    # print('data: ', data)
                    d0, d1, d2, d3 = int(data[2], 16), int(
                        data[3], 16), int(data[4], 16), int(data[5], 16)
                    rn = int(data[6], 16)
                    dis = [d0, d1, d2, d3]
                    distanceQ.append(dis)
                    print('dis:', dis)
                    uwbDataList.append({'time': timestamp, 'dis': dis, 'rn':rn})
                    self.distanceData = dis
                time.sleep(0.2)

            except ValueError:
                print('ValueError')
            finally:
                pass
        
        with open(os.path.dirname(__file__)+'/uwbData/UWB_dis_' + fi_num + '.json', 'a') as fout:
            json.dump(uwbDataList, fout)

        print('finish dumping ubx json data.')

    def start(self):
        self.is_run.set()
        threading.Thread(target=self.run, daemon=True).start()

    def stop(self):
        self.is_run.clear()
        self.ser.close()


class UWBSimulate():
    def __init__(self,offsetQ, filename, anchor_gps):
        self.is_run = threading.Event()
        self.distanceData = [0,0,0,0]
        self.anchor_gps = anchor_gps
        self.anchorPosition_enu = []
        self.offsetQ = offsetQ
        with open(filename,'r') as f:  #os.path.dirname(__file__)+'/uwbData/UWB_dis_18_49_17.json'
            self.allUwb = json.load(f)
        # print(self.allUwb)

    def metadata_initialize(self,anchorPosition_gps):
        print(anchorPosition_gps)
        anchorPosition_enu = [(0, 0, 0)]
        refPointGps = anchorPosition_gps[0]
        for i in range(1, len(anchorPosition_gps)):
            # print(anchorPosition_gps[i][0])
            enu = pm.geodetic2enu(anchorPosition_gps[i][0], anchorPosition_gps[i][1],
                                anchorPosition_gps[i][2], refPointGps[0], refPointGps[1], refPointGps[2])
            anchorPosition_enu.append(enu)
        print(anchorPosition_enu)
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
    def _onUwb(self,uwb):
        print(uwb)

    def onUwb(self,uwb):
        # print(uwb)
        self.distanceData = [i/1000 for i in uwb['dis'][:4]]
        offset = costfun_method(self.distanceData, self.anchorPosition_enu)
        # print('offset:',offset)
        self.offsetQ.append(offset)

    def start(self):
        self.is_run.set()
        threading.Thread(target=self.uwbReplay, daemon=True).start()

    def stop(self):
        self.is_run.clear()



def readUwb():
    # _ser1 = serial.Serial('/dev//ttyACM0', baudrate=9600, timeout=0.01)
    _ser1 = serial.Serial('COM20', baudrate=9600, timeout=0.01)


    fi_num = datetime.now().strftime("%H_%M_%S")
    uwbDataList = []
    start_time = time.time()
    try:
        while True:
            rx_1 = _ser1.readline()
            try:                
                if(len(rx_1) >= 20 and 'mc' in str(rx_1)):
                    timestamp = time.time()-start_time
                    data = str(rx_1).split(' ')
                    print()
                    print('---Time---: ', timestamp)
                    # print('data: ', data)
                    d0, d1, d2, d3 = int(data[2], 16), int(
                        data[3], 16), int(data[4], 16), int(data[5], 16)
                    rn = int(data[6], 16)
                    dis = [d0, d1, d2, d3]
                    distanceQ.append(dis)
                    print('dis:', dis)
                    uwbDataList.append({'time': timestamp, 'dis': dis, 'rn':rn})
                time.sleep(0.2)

            except ValueError:
                print('ValueError')
            finally:
                pass
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        
        with open(os.path.dirname(__file__)+'/uwbData/UWB_dis_' + fi_num + '.json', 'a') as fout:
            json.dump(uwbDataList, fout)

        print('finish dumping ubx json data.')



# def calOffset(offsetQ,anchorPosition_enu):
#     def myonUwb(uwb):
#         dis = [i/1000 for i in uwb['dis']]  #and i != 0 and i !=4
#         # print(dis)
#         offset = costfun_method(dis[:4],anchorPosition_enu)
#         print(offset)
#         offsetQ.append(offset)
#     uwbSimulate(myonUwb)


    
if __name__=='__main__':
    uwbmanager = UWBSimulate(os.path.dirname(__file__)+'/uwbData/UWB_dis_18_49_17.json')
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
