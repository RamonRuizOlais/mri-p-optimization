# -*- coding: utf-8 -*-

import time
import objective_function as simulador

def error(TR, SNR, num_vox, seed_exp=42):
    TR_s = [tr/1000 for tr in TR] # conversion de unidades
    avg_errors_columns, avg_errors, indv_errors_vox = simulador.run_experiments(TR_s, SNR, num_vox, seed_exp)
    
    alpha_errors = indv_errors_vox[:, 0] # Tomamos el error alpha por voxel (1 a num_vox)
    return alpha_errors

