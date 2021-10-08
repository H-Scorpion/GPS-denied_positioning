import joblib
import os
import json
import auxiliary
file_dir = os.path.dirname(__file__)
ubx_recv = joblib.load(file_dir+'/'+'ubxPacket_20211001-164623.pkl')

output_json = []
for ubx in ubx_recv:
    output_json.append({'timestamp': ubx['tiemstamp'],
    'gps_position': auxiliary.objGetGps(ubx['obj']),
    'time':ubx['time']}
    )

with open(file_dir+'/'+'ubxPacket_20211001-164623.json','w') as f :
    json.dump(output_json,f)
# print(ubx_recv[0])
