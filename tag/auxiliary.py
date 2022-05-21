import os
import collections
import joblib
import copy
import pymap3d as pm

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



def gps_to_enu(anchor_gps):
    # input:     
    #     anchor_gps = [(25.01941, 121.54243, 1.3), (25.01941, 121.54236, 1.3),
    #             (25.01915, 121.54237, 1.3), (25.01915, 121.54244, 1.3)]
    # output:
    #     anchor_enu = [(0, 0, 0), (-6, 0, 0), (-6, -29, 0), (0, -29, 0)]
    # example:
    #   anchor_gps = [(25.01941, 121.54243, 1.3), (25.01941, 121.54236, 1.3),
    #                (25.01915, 121.54237, 1.3), (25.01915, 121.54244, 1.3)]
    #   anchor_enu = gps_to_enu(anchor_gps)
    #   print(anchor_enu)
    #   # anchor_enu = [(0, 0, 0), (-6, 0, 0), (-6, -29, 0), (0, -29, 0)]
    anchor_enu = []
    lat0,lon0,h0 = anchor_gps[0]
    for i in range(len(anchor_gps)):
        lat,lon,h = anchor_gps[i]
        e,n,u = pm.geodetic2enu(lat, lon, h, lat0, lon0, h0, ell=None, deg=True)
        anchor_enu.append((e,n,u))
    return anchor_enu


def enu_to_gps(anchor_enu:list, ref_a0_gps:tuple):
    """
    Parameters
    ----------
    anchor_enu:list

    ref_a0_gps:tuple
    ref_a0_gps = (lat, lon, height)
    
    Returns
    -------
    anchor_gps : list
    """
    anchor_gps = []
    lat0, lon0,h0 = ref_a0_gps
    for i in range(len(anchor_enu)):
        e,n,u = anchor_enu[i]
        lat,lon,h = pm.enu2geodetic(e, n, u, lat0, lon0, h0)
        anchor_gps.append([lat,lon,h])
    return anchor_gps


if(__name__ == '__main__'):
    # anchor hight is given by enu data
    anchor_enu = [(0,0,1.5), (0,2.736,1.5),
                 (1.824,2.736,1.5), (1.824, 0, 1.5)]
    # projected onto the ground
    ref_a0_gps = (25.018715700763757, 121.5414674130481,0) 
    anchor_gps = enu_to_gps(anchor_enu,ref_a0_gps)
    print(anchor_gps)
  