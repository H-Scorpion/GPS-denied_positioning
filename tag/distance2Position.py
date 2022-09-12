import numpy as np
import time
# from scipy import optimize
import sys
import collections
# from scipy.optimize import lsq_linear
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
    u, s, Vh = np.linalg.svd(A)
    Smat = np.zeros((3, 3))
    Smat[:3, :3] = np.diag(s)
    Smat_inv = np.linalg.inv(Smat)
    X = np.matmul(Vh.transpose(), Smat_inv)
    X = np.matmul(X, u.transpose())
    X = np.matmul(X, B)
    return X


def lsq_method(distances_to_anchors, anchor_positions):
    """Calculate relative position from 4 uwb distance,
    but height estimation is not accurate.

    Args:
        distances_to_anchors (list): 4 uwb distance
        anchor_positions (4*3 list): 4 uwb position, each with (e, n, u) relative to (0,0,0)

    Raises:
        ValueError: Can't read uwb distance, distances_to_anchors must never be zero. 

    Returns:
        1*3 list: tag position (e, n, u) relative to (0, 0, 0)
    """
    distances_to_anchors, anchor_positions = np.array(
        distances_to_anchors), np.array(anchor_positions)
    '''
    if not np.all(distances_to_anchors):
        raise ValueError(
            'Bad uwb connection. distances_to_anchors must never be zero. ' + str(distances_to_anchors))
    '''
    anchor_offset = anchor_positions[0]
    anchor_positions = anchor_positions[1:] - anchor_offset
    K = np.sum(np.square(anchor_positions), axis=1)  # ax=1 列加
    squared_distances_to_anchors = np.square(distances_to_anchors)
    squared_distances_to_anchors = (
        squared_distances_to_anchors - squared_distances_to_anchors[0])[1:]
    b = (K - squared_distances_to_anchors) / 2.

    res = np.linalg.lstsq(anchor_positions, b, rcond=None)[0]

    
    return res + anchor_offset


def costfun_method(distances_to_anchors, anchor_positions):
    """Calculate relative position from 4 uwb distance,
    getting better height estimation. 

    Args:
        distances_to_anchors (list): 4 uwb distance
        anchor_positions (4*3 list): 4 uwb position, each with (e, n, u) relative to (0,0,0)

    Returns:
        1*3 list: tag position (e, n, u) relative to (0, 0, 0)
    """
    distances_to_anchors, anchor_positions = np.array(
        distances_to_anchors), np.array(anchor_positions)
    tag_pos = lsq_method(distances_to_anchors, anchor_positions)
    anc_z_ls_mean = np.mean(np.array([i[2] for i in anchor_positions]))
    new_z = (np.array([i[2] for i in anchor_positions]) -
             anc_z_ls_mean).reshape(4, 1)
    new_anc_pos = np.concatenate(
        (np.delete(anchor_positions, 2, axis=1), new_z), axis=1)
    new_disto_anc = np.sqrt(abs(distances_to_anchors[:]**2 - (
        tag_pos[0] - new_anc_pos[:, 0])**2 - (tag_pos[1] - new_anc_pos[:, 1])**2))
    new_z = new_z.reshape(4,)

    a = (np.sum(new_disto_anc[:]**2) - 3 *
         np.sum(new_z[:]**2))/len(anchor_positions)
    b = (np.sum((new_disto_anc[:]**2) * (new_z[:])) -
         np.sum(new_z[:]**3))/len(anchor_positions)

    def cost(z): return np.sum(((z - new_z[:])**4 - 2*(((new_disto_anc[:])*(
        z - new_z[:]))**2) + new_disto_anc[:]**4))/len(anchor_positions)

    def function(z): return z**3 - a*z + b
    def derivative(z): return 3*z**2 - a

    def newton(function, derivative, x0, tolerance, number_of_max_iterations=50):
        x1, k = 0, 1
        if (abs(x0-x1) <= tolerance and abs((x0-x1)/x0) <= tolerance):
            return x0
        while(k <= number_of_max_iterations):
            x1 = x0 - (function(x0)/derivative(x0))
            if (abs(x0-x1) <= tolerance and abs((x0-x1)/x0) <= tolerance):
                return x1
            x0 = x1
            k = k + 1
            if (k > number_of_max_iterations):
                pass
                # print("ERROR: Exceeded max number of iterations")
        return x1

    ranges = (slice(0, 30, 0.05), )
    resbrute = newton(function, derivative,50,0.01)

    new_tag_pos = np.concatenate(
        (np.delete(np.array(tag_pos), 2), [resbrute] + anc_z_ls_mean))

    return np.around(new_tag_pos, 8)

def chan_algo(dis_list, anchor_pos):
    SD = 0.1
    G_alpha = []
    H_mat = []
    K_i = []
    # Use measured data in B
    B_mat = np.diag(dis_list)
    Q_mat = np.diag([SD**2 for _ in range(len(anchor_pos)) ])
    
    big_psi = np.matmul(4*B_mat, Q_mat)
    big_psi = np.matmul(big_psi, B_mat)
    
    # initialize G_alpha
    for i in range(len(anchor_pos)):
        K_i.append(anchor_pos[i][0]**2 + anchor_pos[i][1]**2 +anchor_pos[i][2]**2)
        G_alpha.append([-2*anchor_pos[i][0], -2*anchor_pos[i][1], -2*anchor_pos[i][2], 1])
        H_mat.append([dis_list[i]**2-K_i[i]])
        
    G_alpha = np.array(G_alpha)
        
    Z_alpha = np.matmul(np.transpose(G_alpha),np.linalg.inv(big_psi))
    Z_alpha = np.matmul(Z_alpha, G_alpha)
    Z_alpha = np.linalg.pinv(Z_alpha)
    Z_alpha = np.matmul(Z_alpha, np.transpose(G_alpha))
    Z_alpha = np.matmul(Z_alpha, np.linalg.inv(big_psi))
    Z_alpha = np.matmul(Z_alpha, H_mat)
    # return Z_alpha[0][0], Z_alpha[1][0], Z_alpha[2][0]
    # print(Z_alpha)
    
    cov_Z_alpha = np.matmul(np.transpose(G_alpha), np.linalg.inv(big_psi))
    cov_Z_alpha = np.matmul(cov_Z_alpha, G_alpha)
    cov_Z_alpha = np.linalg.pinv(cov_Z_alpha)
    
    H_prime = np.array([[Z_alpha[0][0]**2],
                        [Z_alpha[1][0]**2],
                        [Z_alpha[2][0]**2],
                        [Z_alpha[3][0]**2]])
    G_alpha_prime = [[1,0,0],
                     [0,1,0],
                     [0,0,1],
                     [1,1,1]]
    B_prime = np.diag([Z_alpha[0][0], Z_alpha[1][0], Z_alpha[2][0],0.5])
    
    big_psi_prime = np.matmul(4*B_prime,cov_Z_alpha)
    big_psi_prime = np.matmul(big_psi_prime, B_prime)
    
    Z_alpha_prime = np.matmul(np.transpose(G_alpha_prime), np.linalg.pinv(big_psi_prime))
    Z_alpha_prime = np.matmul(Z_alpha_prime, G_alpha_prime)
    Z_alpha_prime = np.linalg.inv(Z_alpha_prime)
    Z_alpha_prime = np.matmul(Z_alpha_prime,np.transpose(G_alpha_prime))
    Z_alpha_prime = np.matmul(Z_alpha_prime, np.linalg.pinv(big_psi_prime))
    Z_alpha_prime = np.matmul(Z_alpha_prime, H_prime)
    
    x_est = Z_alpha_prime[0]**0.5 if Z_alpha_prime[0] else -Z_alpha_prime[0]**0.5
    y_est = Z_alpha_prime[1]**0.5 if Z_alpha_prime[1] else -Z_alpha_prime[1]**0.5
    z_est = Z_alpha_prime[2]**0.5 if Z_alpha_prime[2] else -Z_alpha_prime[2]**0.5
    # print(Z_alpha_prime)
    
    return [x_est[0], y_est[0], z_est[0]]


if __name__ == '__main__':
    # realpos = costfun_method([7.071, 7.071, 7.071, 7.071], [
    #                          (20, 20, 0), (30, 20, 0), (30, 30, 0), (20, 30, 0)])
    # realpos = costfun_method([673, 269, 553, 782],
    #                          [(0, 0, 0), (-880.1274020054734, 122.98658630120735, -0.06188017960501924), (-990.1884056935132, -499.5511201510228, -0.09647551304698254), (-149.3876144609321, -626.9752475078211, -0.03271644687936259)])
    # [-647.085   -33.9212  141.7757]
    realpos = costfun_method([1.865,0.613, 1.91, 2.594],
                            [(0, 0, 0), (-2.338373383814485e-10, 2.2819277183312483, -1.0649555015618262e-08), (2.2811277246200543, 2.2819279083869626, -1.818721351298791e-08), (2.2811281075343626, -0.011077128511786723, -9.585527442970698e-09)])
    realpos = lsq_method([1.865,0.613, 1.91, 2.594],
                            [(0, 0, 0), (-2.338373383814485e-10, 2.2819277183312483, -1.0649555015618262e-08), (2.2811277246200543, 2.2819279083869626, -1.818721351298791e-08), (2.2811281075343626, -0.011077128511786723, -9.585527442970698e-09)])
    print(realpos)

    
