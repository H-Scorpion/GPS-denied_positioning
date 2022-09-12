import numpy as np
from scipy import optimize
import sys
import collections
import time
from scipy.optimize import lsq_linear, root, minimize
import random
import matplotlib.pyplot as plt
from tqdm import tqdm, trange
import numpy.matlib
from itertools import product
from itertools import combinations
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import heapq
import random
from sympy import *


def my_lsq(distances_to_anchors, anchor_positions):
    distances_to_anchors, anchor_positions = np.array(
        distances_to_anchors), np.array(anchor_positions)
    ref_x, ref_y, ref_z = anchor_positions[0][0], anchor_positions[0][1], anchor_positions[0][2]
    l_01 = (anchor_positions[1][0]-ref_x)**2 + (anchor_positions[1]
                                                [1] - ref_y)**2 + (anchor_positions[1][2]-ref_z)**2
    l_01 = l_01**0.5
    l_02 = (anchor_positions[2][0]-ref_x)**2 + (anchor_positions[2][1] - ref_y)**2 + (anchor_positions[2][2]-ref_z)**2
    l_02 = l_02**0.5
    l_03 = (anchor_positions[3][0]-ref_x)**2 + (anchor_positions[3]
                                                [1] - ref_y)**2 + (anchor_positions[3][2]-ref_z)**2
    l_03 = l_03**0.5
    
    B = [0.5*(distances_to_anchors[0]**2 +l_01**2-distances_to_anchors[1]**2),
         0.5*(distances_to_anchors[0]**2 +l_02**2-distances_to_anchors[2]**2),
         0.5*(distances_to_anchors[0]**2 +l_03**2-distances_to_anchors[3]**2)]
    B = np.array(B)
    B = B.transpose()
    A = [[anchor_positions[1][0]-ref_x, anchor_positions[1][1] - ref_y, anchor_positions[1][2]-ref_z],
         [anchor_positions[2][0]-ref_x, anchor_positions[2]
             [1] - ref_y, anchor_positions[2][2]-ref_z],
         [anchor_positions[3][0]-ref_x, anchor_positions[3][1] - ref_y, anchor_positions[3][2]-ref_z]]
    A = np.array(A)
    u, s, Vh = numpy.linalg.svd(A)
    Smat = np.zeros((3, 3))
    Smat[:3, :3] = np.diag(s)
    print(u)
    print(Smat)
    print(Vh)
    Smat_inv = np.linalg.inv(Smat)
    X = np.matmul(Vh.transpose(), Smat_inv)
    X = np.matmul(X, u.transpose())
    X = np.matmul(X, B)
    print(X)


def lsq_method(distances_to_anchors, anchor_positions):
    distances_to_anchors, anchor_positions = np.array(
        distances_to_anchors), np.array(anchor_positions)
    if not np.all(distances_to_anchors):
        raise ValueError(
            'Bad uwb connection. distances_to_anchors must never be zero. ' + str(distances_to_anchors))
    anchor_offset = anchor_positions[0]
    anchor_positions = anchor_positions[1:] - anchor_offset
    K = np.sum(np.square(anchor_positions), axis=1)  # ax=1 列加
    squared_distances_to_anchors = np.square(distances_to_anchors)
    squared_distances_to_anchors = (
        squared_distances_to_anchors - squared_distances_to_anchors[0])[1:]
    b = (K - squared_distances_to_anchors) / 2.
    res = lsq_linear(anchor_positions, b, lsmr_tol='auto', verbose=0)
    # res = np.dot(np.dot(np.linalg.inv(np.dot(anchor_positions.T, anchor_positions)),(anchor_positions.T)), b)
    # res = np.linalg.lstsq(anchor_positions, b, rcond=None)[0]
    return res.x + anchor_offset


def two_stage(distances_to_anchors, anchor_positions):
    tag_pos = lsq_method(distances_to_anchors, anchor_positions)
    z = symbols('z', real=True)
    f = symbols('f', cls=Function)
    f = 0
    for i in range(anchor_positions.shape[0]):
        delta = distances_to_anchors[i]**2 - (
            (tag_pos[0] - anchor_positions[i][0])**2 + (tag_pos[1] - anchor_positions[i][1])**2)
        f += 4 * ((z - anchor_positions[i][2]) **
                  3 - delta*((z)-anchor_positions[i][2]))
    z_candidate = np.array(solve(f, z))
    #print(f, z_candidate)
    cost_function = list()
    for j in range(z_candidate.shape[0]):
        cost = 0
        for i in range(anchor_positions.shape[0]):
            d = (tag_pos[0] - anchor_positions[i][0])**2 + (tag_pos[1] -
                                                            anchor_positions[i][1])**2 + (z_candidate[j] - anchor_positions[i][2])**2
            cost += (d - distances_to_anchors[i] ** 2)**2
        cost_function.append(cost)
    #print('first stage,', tag_pos)
    # print('candidate:',z_candidate)#, 'cost:', cost_function)
    #tag_pos[2] = z_candidate[np.argmin(cost_function)]
    # return tag_pos
    result = list()
    for i in range(z_candidate.shape[0]):
        result.append(np.array([tag_pos[0], tag_pos[1], z_candidate[i]]))
    return np.array(result).astype(np.float32)

# some function and setting for test


def select_real_location():
    a, b = 0, 1
    x = 10 * random.uniform(a, b)
    y = 10 * random.uniform(a, b)
    z = 10 * random.uniform(a, b)
    return [x, y, z]


def calculate_distances(anchor_num, anchor_positions, real_position):
    distances = [0]*anchor_num
    for i in range(anchor_num):
        distance_square = 0
        for j in range(3):
            distance_square += (anchor_positions[i][j]-real_position[j])**2
        distances[i] = distance_square ** (1/2)
    return distances


def calculate_distances_differences(distances_to_anchors, anchor_num):
    dif = [[0 for _ in range(anchor_num)]for _ in range(anchor_num)]
    for i in range(anchor_num):
        for j in range(anchor_num):
            dif[i][j] = distances_to_anchors[i]-distances_to_anchors[j]
    return dif


def rotation_matrix_from_vectors(vec1, vec2):
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 /
                                                      np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    if any(v):  # if not all zeros then
        c = np.dot(a, b)
        s = np.linalg.norm(v)
        kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        return np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))

    else:
        # cross of all zeros only occurs on identical directions
        return np.eye(3)


'''
def test (anchor_num ,anchor_positions ,size ,method ,noise_scale,position_type, position=[0,0,0], rotate=False, rtx=None, mean=None):
    
    max_xyz = [10,10,10] ## max range of x , y ,z
  
    locations = [0]*size
    real_positions = [0]*size

    average_error = 0
    error_x = [0]*size
    error_y = [0]*size
    error_z = [0]*size
    error_distance = [0]*size

    noisy_distances = [0]*anchor_num
    
    
    for k in range(size):

        # position_tpye 設定要test的位置

        # 只測試function中給定的那一點
        if position_type == "only_one":
            [x,y,z] = position
            real_position = [x,y,z]

        # 只測試select_real_location這個function隨機抽中的那一點
        if position_type == "random":
            [x,y,z] = select_real_location()
            real_position = [x,y,z]
          
        # 測試all_task_positions_1m這個list裡的所有點
        if position_type == "1m":
            real_position = all_task_positions_1m[k]
         
        real_positions[k]=real_position
    
        distances_to_anchors = calculate_distances(anchor_num,anchor_positions,real_position)
        
        distances_differences = calculate_distances_differences(distances_to_anchors,anchor_num)

        
        if method == "ToA":
            # 給ToA有誤差的量測距離
            for i in range(anchor_num):
                noisy_distances[i] = distances_to_anchors[i] + random.gauss(0,noise_scale)

            locations[k] = ToA(noisy_distances, anchor_num, anchor_positions, max_xyz)
        
        if method == "TDoA":
            
            noisy_distances_differences = distances_differences
            
            # 給ToA有誤差的量測距離差
            for i in range(anchor_num):
                for j in range(i):
                    noisy_distances_differences[i][j] = distances_differences[i][j] + random.gauss(0,noise_scale)
                    noisy_distances_differences[j][i] = -noisy_distances_differences[i][j]

            locations[k] = TDoA(anchor_num, anchor_positions,noisy_distances_differences,max_xyz)
        if method == 'ToA_twostage':
            for i in range(anchor_num):
                noisy_distances[i] = distances_to_anchors[i] + random.gauss(0,noise_scale)
            locations[k] = two_stage(noisy_distances, anchor_positions)
        if rotate:
            locations[k] = (np.linalg.inv(rtx).dot(locations[k].T)) + mean
        error_x[k] = (locations[k][0]-real_position[0])
        error_y[k] = (locations[k][1]-real_position[1])
        error_z[k] = (locations[k][2]-real_position[2])
        error_distance[k] = ( error_x[k]**2 + error_y[k]**2 + error_z[k]**2 )**(1/2)
        
        average_error += error_distance[k]/size

    return {"average_error":average_error , "error_distance":error_distance , "error_x":error_x , "error_y":error_y , "error_z":error_z , 
            "calculate_positions":locations,"real_positions":real_positions}
            # error_distance,error_x,y,z calculate_positions,real_positions為list
            # error_distace表示real_position到calculate_position的距離
'''

if __name__ == '__main__':
    realpos = my_lsq([1.865, 0.613, 1.91, 2.594],
                     [(0, 0, 0), (-2.338373383814485e-10, 2.2819277183312483, -1.0649555015618262e-08), (2.2811277246200543, 2.2819279083869626, -1.818721351298791e-08), (2.2811281075343626, -0.011077128511786723, -9.585527442970698e-09)])

    # # try to use test 這個 function
    # anchor_num = 4
    # anchor_positions = [[0, 0, 0.0],
    #                     [0.288, 5.005, 0.0],
    #                     [1.974, 5.149, 0.0],
    #                     [2.245, 0, 0.0]]#[[0, 0, 0], [10, 0, 0], [0, 10, 0], [10, 10, 10]]
    # real_position =[7,7,9]
    # size = 1
    # method = "ToA"
    # position_type = "random"
    # noise_scale = 0.1
    # distances_to_anchors = calculate_distances(anchor_num,anchor_positions,real_position) + np.random.normal(0, noise_scale, anchor_num)
    # distances_to_anchors = np.array([311, 323, 343, 337]) / 100
    # print(distances_to_anchors)

    # Anchor_mean = np.mean(anchor_positions, axis=0)
    # Anchor = np.array(anchor_positions) - Anchor_mean
    # u, s, vh = np.linalg.svd(Anchor, full_matrices=True)
    # print(s)
    # #rotate
    # Target_vector = np.array([0,0,1])
    # Orinig_vector = vh[-1][0:3] / (np.linalg.norm(vh[-1][0:3]) + 1e-8)

    # #rotate matrix
    # rtx = rotation_matrix_from_vectors(Orinig_vector,Target_vector)
    # rotate_Anchor = (rtx.dot(Anchor[:,:3].T).T)
    # print('Rotate Anchor:\n', rotate_Anchor)

    # #Stage one
    # stage_one_result = lsq_method(distances_to_anchors, anchor_positions)
    # print('Stage one result:', stage_one_result)
    # print('RMSE:', np.sqrt(np.mean((stage_one_result-real_position)**2)))
    # #stage two
    # stage_two_result = two_stage(distances_to_anchors, rotate_Anchor)
    # print('stage Two: \n')
    # #print('Stage two result:', (np.linalg.inv(rtx).dot(stage_two_result.T)) + Anchor_mean)
    # #print('RMSE:', np.sqrt(np.mean(((np.linalg.inv(rtx).dot(stage_two_result.T)) + Anchor_mean-np.array(real_position))**2)))
    # for i in range(stage_two_result.shape[0]):
    #     print(np.linalg.inv(rtx).dot(stage_two_result[i].T) + Anchor_mean,)
    #     print('RMSE:', np.sqrt(np.mean((np.linalg.inv(rtx).dot(stage_two_result[i].T) + Anchor_mean-np.array(real_position))**2)), '\n')
