# -*- coding: UTF-8 -*-
import serial
import glob
import json
import collections
import datetime
import time
import os
import numpy as np
from datetime import datetime

# _ser1 = serial.Serial('/dev//ttyACM0', baudrate=9600, timeout=0.01)
_ser1 = serial.Serial('COM20', baudrate=9600, timeout=0.01)


fi_num = datetime.now().strftime("%H_%M_%S")
while True:
    rx_1 = _ser1.readline()

    try:
        ti = datetime.now().strftime("%H:%M:%S")
        if(len(rx_1) >= 20):
            data = str(rx_1).split(' ')
            print()
            print('---Time---: ', ti)
            # print('data: ', data)
            d0, d1, d2, d3 = int(data[2], 16), int(
                data[3], 16), int(data[4], 16), int(data[5], 16)
            rn = int(data[6], 16)
            dis = [d0, d1, d2, d3, rn]
            print('dis:', dis)
            with open(os.path.dirname(__file__)+'/uwbData/UWB_dis_' + fi_num + '.txt', 'w') as fout:
                json.dump({'time': ti, 'dis': dis}, fout)
        time.sleep(0.2)

    except ValueError:
        print('ValueError')
    finally:
        pass
