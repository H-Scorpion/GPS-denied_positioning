import json
import serial
import time

with open("connection_data.json",'r') as f:
    connection_data = json.load(f)[0]
    tag_com = connection_data['tag_com']
    
ser = serial.Serial(tag_com, baudrate=115200, timeout=0.01)
while True:
    rx_1 = ser.readline()
    # print(rx_1)
    if(len(rx_1) >= 20 and 'mc' in str(rx_1)):
        try:
            data = str(rx_1).split(' ')
            # print(data)
            d0, d1, d2, d3 = data[2].split(',')[0], data[3].split(
                ',')[0], data[4].split(',')[0], data[5].split(',')[1]
            dis = [int(d0)/1000, int(d1)/1000, int(d2)/1000, int(d3)/1000]
            print(dis)
        except Exception:
            print(Exception)
    time.sleep(0.01)