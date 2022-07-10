import numpy as np
import time
# from scipy import optimize
import sys
import collections
# from scipy.optimize import lsq_linear


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


if __name__ == '__main__':
    # realpos = costfun_method([7.071, 7.071, 7.071, 7.071], [
    #                          (20, 20, 0), (30, 20, 0), (30, 30, 0), (20, 30, 0)])
    # realpos = costfun_method([673, 269, 553, 782],
    #                          [(0, 0, 0), (-880.1274020054734, 122.98658630120735, -0.06188017960501924), (-990.1884056935132, -499.5511201510228, -0.09647551304698254), (-149.3876144609321, -626.9752475078211, -0.03271644687936259)])
    # [-647.085   -33.9212  141.7757]
    realpos = lsq_method([673, 269, 553, 782],
                             [(0, 0, 0), (-880.1274020054734, 122.98658630120735, -0.06188017960501924), (-990.1884056935132, -499.5511201510228, -0.09647551304698254), (-149.3876144609321, -626.9752475078211, -0.03271644687936259)])
    print(realpos)

    
