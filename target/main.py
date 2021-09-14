import threading
# import concurrent.futures
import serial
import collections
import time
from calGps import calGps
# from ubx import UBXManager
from readGps import readGps

relPos = collections.deque(maxlen=1)
refGps = collections.deque(maxlen=1)


relPos.append(
    (0, 0, 0)  # (e, n, u)
)
refGps.append(
    (0, 0, 0)  # (lat, lon, heith)
)


def readUwb():
    pass


if __name__ == '__main__':
    th_gps = threading.Thread(
        target=readGps, args=[refGps], daemon=True)
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
            # do something
            # calc_position(lon, lat, d0, d1, d2, d3)
        else:
            time.sleep(0.01)
