import os
import collections
import joblib
import copy

def objGetGps(pvt_obj):
    return (pvt_obj.lat*10**-7, pvt_obj.lon*10**-7, pvt_obj.height*10**-7)

def anchor_gps_2_anc_gps_q(anchor_gps):
    templatePath = os.path.dirname(__file__)+'/template/'
    anchor_list = copy.deepcopy(anchor_gps)

    for i in range(4):
        pvt_obj = joblib.load(templatePath + 'NAV-PVT_template.pkl')
        pvt_obj.lat = int(anchor_gps[i][0]*10**7)
        pvt_obj.lon = int(anchor_gps[i][1]*10**7)
        pvt_obj.height = int(anchor_gps[i][2]*10**7)
        anchor_list[i] = pvt_obj
    return collections.deque([anchor_list], maxlen=1)

def anc_gps_q_2_anchor_gps(anc_gps_q):
    anchor_gps = []
    for i in range(4):
        anchor_gps.append([])
        anchor_gps[i].append(anc_gps_q[0][i].lat*10**-7)
        anchor_gps[i].append(anc_gps_q[0][i].lon*10**-7)
        anchor_gps[i].append(anc_gps_q[0][i].height*10**-7)
    return(anchor_gps)