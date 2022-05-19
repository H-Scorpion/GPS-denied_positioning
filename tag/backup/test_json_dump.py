import json

pos_dic = dict()
pos_dic['anchor_gps'] = True


with open('pos.json','w') as f:
    json.dump(pos_dic,f)