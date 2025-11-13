# -*- coding: utf-8 -*-

import single_sawp
import os
from concurrent.futures import ProcessPoolExecutor

def busqueda_local(args):
    x, TR, n, SNR, num_vox, vect_TR = args
    return single_sawp.single_sawp(x, TR, n, SNR, num_vox, vect_TR)

def ejecutar_busqueda_local(pop_in, n, SNR, num_vox, vect_TR):
    max_workers = 20
    #print(f"Núcleos visibles por este proceso: {max_workers}")
    args = [(ind[0], ind[1], n, SNR, num_vox, vect_TR) for ind in pop_in]

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        pop_out = list(executor.map(busqueda_local, args))

    return pop_out

