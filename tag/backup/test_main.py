import collections
import time
import threading
from backup.check_packet_attribute import test
# def count():
#     c = 0
#     def add():
#         nonlocal c
#         c += 1
#     add()
#     return c
q = collections.deque(maxlen=5)
q.append(1)
q.append(3)
print(type(q),'in main')
t = threading.Thread(target=test,args=[q],daemon=True)
t.start()
time.sleep(1)
while True:
    print(q)
    time.sleep(1)
t.join()
# print(count())