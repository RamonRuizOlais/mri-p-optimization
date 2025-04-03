# -*- coding: utf-8 -*-

import time
import objective_function as simulador

def error(TR, SNR, num_vox, seed_exp=42):
    resultado = simulador.run_experiments(TR, SNR, num_vox, seed_exp)[0][0]  # Tomamos error promedio alpha   
    return resultado

