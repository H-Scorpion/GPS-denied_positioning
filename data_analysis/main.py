import joblib
import pyubx2
import matplotlib.pyplot as plt
import numpy as np
if __name__ == '__main__':
    data = joblib.load('./data_analysis/tagPosData_20220911-203242.pkl')
    # print(data)
    data = np.array(data)
    
    a0_dis = [d[0] for d in data[:,1]]
    a1_dis = [d[1] for d in data[:,1]]
    a2_dis = [d[2] for d in data[:,1]]
    a3_dis = [d[3] for d in data[:,1]]
    
    e_list = [pos[0] for pos in data[:,2]]
    n_list = [pos[1] for pos in data[:,2]]

    
    fig, axs = plt.subplots(2)
    axs[0].plot(data[:,0], a0_dis)
    axs[0].plot(data[:,0], a1_dis)
    axs[0].plot(data[:,0], a2_dis)
    axs[0].plot(data[:,0], a3_dis)
    axs[1].plot(data[:,0], e_list)
    axs[1].plot(data[:,0], n_list)
    plt.tight_layout()
    plt.show()