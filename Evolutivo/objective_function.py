#%%---------------------------------------------------------------------------------------------
# Importing libraries
#-----------------------------------------------------------------------------------------------

import numpy as np
from gen_functions import *

#%%---------------------------------------------------------------------------------------------
# Objective function
#-----------------------------------------------------------------------------------------------
def run_experiments(TR, SNR, num_vox, seed_exp):
    """
    Generation of a “num_vox” amount of synthetic data and fitting to it given a noise “SNR” and a vector “TR”.

    Args:
        TR (np.arr): Array of TR values to be tested.
        SNR (float): Numerical value for noise (Signal to Noise Ratio)
        num_vox (int): Number of experiments to be performed

    Returns:
        avg_param_errors (np.arr): Array containing the average error of each individual parameter.
        avg_voxel_error (np.arr): Array containing the average error of each individual voxel.
        individual_errors (np.arr): Array containing the individual error of each parameter for each experiment.
    """
    
        #             k1     k2     T1_mye  T2_mye  T1_IE   T2_IE   flip_angle
    initial_params = [0.5,   0.5,   0.165,  0.015,  2.000,  0.045,  165]        # Initial values of the search range
                    
    lower_bounds = [  0.00,  0.00,  0.130,  0.010,  1.800,  0.030,  150]        # Lower limit of the search range
    upper_bounds = [  1.00,  1.00,  0.200,  0.025,  2.500,  0.060,  180]        # Upper limit of the search range
    
    
    np.random.seed(seed_exp) 
    popt_data = np.zeros((num_vox,10))
    real_data = np.zeros((num_vox,10))
    with open('TE.txt', 'r') as f:
        TE = np.array([float(x) for x in f.read().split()])
    
    for i in range(num_vox):

        mye_c = np.random.uniform(0.05, 0.3)
        csf_c = np.random.uniform(0.0, 0.15)
        ie_c = 1 - (mye_c + csf_c)
            
        #                         Mielina    IE       CSF
        contributions = np.array([mye_c,     ie_c,    csf_c])     # Contributions (Alpha, Beta, Gamma)

        T1 = np.array([[T1_myelin(lower_bounds, upper_bounds)], [T1_IE(lower_bounds, upper_bounds)], [4.0]])  # T1s
        T2 = np.array([[T2_myelin(lower_bounds, upper_bounds)], [T2_IE(lower_bounds, upper_bounds)], [0.2]])  # T2s


        flip = np.random.uniform(150, 180)                      # Flip angle in degrees

        epg_syn_data = gen_epg_data(contributions, T1, T2, flip, TR, TE)
        real = [contributions[0], contributions[1],  contributions[2], T1[0][0], T2[0][0], T1[1][0], T2[1][0], T1[2][0], T2[2][0], flip]
        
        noisy_epg = add_rician_noise(epg_syn_data, SNR)
        popt, _, _ = fit_params_epg(noisy_epg, TR, TE, initial_params, lower_bounds, upper_bounds)
        popt_data[i,:] = popt
        real_data[i,:] = real
        
    avg_param_errors, avg_vox_error, individual_errors = error_promedio(real_data, popt_data)
    
    return avg_param_errors, avg_vox_error, individual_errors

#%%


