# -*- coding: utf-8 -*-

import time
import objective_function as simulador

def error(TR, SNR, num_vox, seed_exp=42):
    TR_s = [tr/1000 for tr in TR]
    resultado = simulador.run_experiments(TR_s, SNR, num_vox, seed_exp)[0][0]  # Tomamos error promedio alpha   
    return resultado

