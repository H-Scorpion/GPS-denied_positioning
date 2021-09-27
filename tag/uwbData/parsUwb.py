import json
import os

originalFileName = "/new_20m.json"
dirPath = os.path.dirname(__file__)

with open(dirPath+originalFileName, "r") as f1:
    dis_data1 = json.load(f1)

new_data = []
start_time = float(dis_data1[0]['time'])
for i in dis_data1:
    if float(i['time']) < 60:
        i['time'] = float(i['time'])-start_time
        new_data.append(i)
        # with open('UWB_dis_exp_robot' + '.txt', 'a') as fout:
        #     json.dump(data_dic, fout)
    else:
        break


opFileName = '/pars_time'+originalFileName[4:]
with open(dirPath+opFileName, 'a') as fout:
    json.dump(new_data, fout)
