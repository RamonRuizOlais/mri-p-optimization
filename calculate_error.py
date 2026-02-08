# -*- coding: utf-8 -*-


#import pandas as pd
import random
import error_vox as evox
#import comparison
import feasible as feas
import random_solution as rs

def calculate_error(n, seed, SNR, num_vox):
    random.seed(seed)
    
    with open('TR.txt', 'r') as f:
        vect_TR = [int(x) for x in f.read().split()]
        
    x = rs.random_solution(n, vect_TR)
    x, TR = feas.ensure_feasible(x, vect_TR, convert=True)
    
    # Obtener errores por voxel (1 a num_vox)
    ind_error_vox = evox.error(TR, SNR, num_vox)
    
    return TR, ind_error_vox 
    
    
    

