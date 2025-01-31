#%%---------------------------------------------------------------------------------------------
# Importing libraries
#-----------------------------------------------------------------------------------------------

import numpy as np
from gen_functions import *

#%%---------------------------------------------------------------------------------------------
# Objective function
#-----------------------------------------------------------------------------------------------
def run_experiments(TR, SNR, num_vox):
    """
    Generation of a “num_vox” amount of synthetic data and fitting to it given a noise “SNR” and a vector “TR”.

    Args:
        TR (np.arr): Array of TR values to be tested.
        SNR (float): Numerical value for noise (Signal to Noise Ratio)
        num_vox (int): Number of experiments to be performed

    Returns:
        avg_error (np.arr): Array containing the average error of each individual parameter vector “TR”.
    """
    
        #             k1     k2     T1_mye  T2_mye  T1_IE   T2_IE   T1_CSF  T2_CSF  flip_angle
    initial_params = [0.5,   0.5,   0.165,  0.015,  2.000,  0.045,  4.000,  0.200,  165]        # Initial values of the search range
                    
    lower_bounds = [  0.00,  0.00,  0.130,  0.010,  1.800,  0.030,  3.950,  0.195,  150]        # Lower limit of the search range
    upper_bounds = [  1.00,  1.00,  0.200,  0.025,  2.500,  0.060,  4.050,  0.205,  180]        # Upper limit of the search range
        
    popt_data = np.zeros((num_vox,10))
    real_data = np.zeros((num_vox,10))
    TE = np.array([0.007, 0.014, 0.021, 0.028, 0.035, 0.042, 0.049, 0.056, 0.063, 0.070])     # TE values

    for i in range(num_vox):

        mye_c = np.random.uniform(0.05, 0.3)
        csf_c = np.random.uniform(0.0, 0.15)
        ie_c = 1 - (mye_c + csf_c)
            
        #                         Mielina    IE       CSF
        contributions = np.array([mye_c,     ie_c,    csf_c])     # Contributions (Alpha, Beta, Gamma)

        T1 = np.array([[T1_myelin(lower_bounds, upper_bounds)], [T1_IE(lower_bounds, upper_bounds)], [T1_CSF(lower_bounds, upper_bounds)]])  # T1s
        T2 = np.array([[T2_myelin(lower_bounds, upper_bounds)], [T2_IE(lower_bounds, upper_bounds)], [T2_CSF(lower_bounds, upper_bounds)]])  # T2s


        flip = np.random.uniform(150, 180)                      # Flip angle in degrees

        epg_syn_data = gen_epg_data(contributions, T1, T2, flip, TR, TE)
        real = [contributions[0], contributions[1],  contributions[2], T1[0][0], T2[0][0], T1[1][0], T2[1][0], T1[2][0], T2[2][0], flip]
        
        noisy_epg = add_rician_noise(epg_syn_data, SNR)
        popt, _, _ = fit_params_epg(noisy_epg, TR, TE, initial_params, lower_bounds, upper_bounds)
        popt_data[i,:] = popt
        real_data[i,:] = real
        
    avg_error, _ = error_promedio(real_data, popt_data)
    
    return avg_error

#%%
