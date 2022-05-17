import joblib
import datetime

# the gps data wanted to be template
target_gps_path = './gpsData/ubxPacket_20211001-164623.pkl'

load_data = joblib.load(target_gps_path)

ubx_obj = load_data[-31]['obj']
print(ubx_obj._class)
print(ubx_obj._id)
print(ubx_obj)
# print(dir(ubx_obj))

# save template file
save_filename = input('save as template? (input file name)')
if(save_filename):
    joblib.dump(ubx_obj,f'./{save_filename}.pkl')