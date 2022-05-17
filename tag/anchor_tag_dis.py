import json
import serial
import time
import numpy as np

with open("connection_data.json",'r') as f:
    connection_data = json.load(f)[0]
    tag_com = connection_data['tag_com']

calibrate_dis = np.array([-.6, -.6, -.6 ,-.6])

ser = serial.Serial(tag_com, baudrate=115200, timeout=0.01)
while True:
    rx_1 = ser.readline().decode('utf-8')
    # print(rx_1)
    if(rx_1 != ' ' and rx_1.find('mc') >= 0):
        dis = rx_1.split(' ')
        dis_array = np.array([(int(dis[2],16)),(int(dis[3],16)), (int(dis[4],16)), (int(dis[5],16))])/1000.0
        dis_array = dis_array + calibrate_dis
        print(dis_array) # meter
    # if(len(rx_1) >= 20 and 'mc' in str(rx_1)):
    #     try:
    #         data = str(rx_1).split(' ')
    #         # print(data)
    #         d0, d1, d2, d3 = data[2].split(',')[0], data[3].split(
    #             ',')[0], data[4].split(',')[0], data[5].split(',')[1]
    #         dis = [int(d0)/1000, int(d1)/1000, int(d2)/1000, int(d3)/1000]
    #         print(dis)
        # except Exception:
        #     print(Exception)
    time.sleep(0.01)