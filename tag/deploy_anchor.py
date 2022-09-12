import numpy as np
from auxiliary import enu_to_gps
import json
def rotate_frame(yaw , deploy_pos):
    """
    Parameters
    ----------
    yaw : float
        Yaw when drone at anchor 0, pointing to anchor 1
    deploy_pos : list
        2D array, the anchor position when deploy
        [[a0_x, a0_y], [a1_x, a2_y], [a2_x, a2_y], [a3_x, a3_y]]
    
    Returns
    -------
    enu_pos : np array
        2d numpy array, calibrate to north
    """
    yaw_rad = yaw/180 * np.pi
    deploy_pos = np.array(deploy_pos)
    deploy_pos = np.transpose(deploy_pos)
    rot_matrix = np.array([[np.cos(yaw_rad), -np.sin(yaw_rad)],
                           [np.sin(yaw_rad),  np.cos(yaw_rad)]])
    enu_pos = np.matmul(rot_matrix,deploy_pos)
    enu_pos = np.transpose(enu_pos)
    return enu_pos


def include_height(enu_pos,height):
    # print(enu_pos)
    anchor_enu = []
    for i in range(4):
        enu_pos[i].append(height)
        anchor_enu.append( enu_pos[i])
    return anchor_enu
# def measured_pos_to_enu():
    

def get_deploy_anchor_gps(deploy_pos,yaw, height, ref_gps):
    """
    Parameters
    ----------
    deploy_pos: 2D list
        Anchor position we deployed in its Cartesian coordinate
        e.g. deploy_pos = [[0, 0], [0, 10], [20, 10], [20, 0]]
    
    yaw: float
        Yaw(degree) when drone at anchor 0, pointing to anchor 1
    
    height: float
        height of the anchor (in meter)
        
    ref_gps: tuple
        Anchor 0 position at height = 0
        in (lat, lon, height)
        e.g. (25.01871570076376, 121.5414674130481, 0)
    
    Returns
    -------
    anchor_gps : list
        2D list
        GPS position of the 4 anchors
        e.g. [[25.018715700763757, 121.5414674130481, 1.5000000008883514], 
              [25.018740399880667, 121.5414674130481, 1.5000005896477655], 
              [25.018740399879572, 121.54148548412036, 1.5000008494433268], 
              [25.018715700762662, 121.54148548411675, 1.5000002589960404]]
    """
    enu_pos = rotate_frame(-1*yaw,deploy_pos).tolist()
    anchor_enu = include_height(enu_pos, height)
    anchor_gps = enu_to_gps(anchor_enu,ref_gps)
    return anchor_gps


if __name__ == '__main__':
    with open('./deploy.json', 'r') as f:
        deploy_data = json.load(f)[0]
        W = float(deploy_data['W']) # in meters
        L = float(deploy_data['L']) # in meters
        yaw = float(deploy_data['yaw']) # in degrees
        height = float(deploy_data['height']) # in meters
        ref_gps = [ float(i) for i in deploy_data['ref_gps']]
    print(ref_gps)
    
    
    deploy_pos = [[0, 0], [0, W], [L, W], [L, 0]] 

    # ref_gps = (25.01871570076376, 121.5414674130481, 0)
    # ref_gps = (25.0177, 121.54419, 0)
    anchor_gps = get_deploy_anchor_gps(deploy_pos, yaw, height, ref_gps)
    print(anchor_gps)
    
    with open("./connection_data.json",'r') as f:
        connection_data = json.load(f)[0]

    data = []
    data.append(anchor_gps)
    connection_data["anchor_gps"] = data

    
    with open('./connection_data.json', 'w') as f:
        f.write(json.dumps([connection_data]))
    
    # enu_pos = rotate_frame(90,deploy_pos).tolist()
    # # print(enu_pos)
    # anchor_enu = include_height(enu_pos, 1.3)
    # anchor_gps = enu_to_gps(anchor_enu,ref_gps)
    # print(anchor_gps)
    # # anchor_gps = enu_to_gps(enu_pos,(25.01871570076376, 121.5414674130481, 3.000000000735832))
    
