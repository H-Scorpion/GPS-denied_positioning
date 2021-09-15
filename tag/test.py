import collections
import time
# print('hi')
q = 5
def test(que):
    print(type(que))
    que.append(2)
    print('in test')
    for i in range(1000):
        que.append(i)
        time.sleep(1)
def qAppend():
    pass