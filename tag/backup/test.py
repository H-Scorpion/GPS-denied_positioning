import collections
import time
import os
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

# filePath = __file__
# print("This script file path is ", filePath)

# wd = os.getcwd()
# print("working directory is ", wd)




# absFilePath = os.path.abspath(__file__)
# print("This script absolute path is ", absFilePath)

# path, filename = os.path.split(absFilePath)
# print("Script file path is {}, filename is {}".format(path, filename))
# print(os.path.split(absFilePath))

import os

print(os.path.dirname(__file__))