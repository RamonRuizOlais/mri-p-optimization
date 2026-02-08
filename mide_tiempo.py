# -*- coding: utf-8 -*-

import error
import time
import numpy as np

import random
import comparison
import feasible as feas
import random_solution as rs

n = 100
random.seed(1)

with open('TR.txt', 'r') as f:
        vect_TR = [int(x) for x in f.read().split()]
    
tiempos = []

pop_prueba = [rs.random_solution(n, vect_TR) for _ in range(30)]
pop_feasible_prueba = [feas.ensure_feasible(x, vect_TR, convert=True) for x in pop_prueba]


for indx, indv in enumerate(pop_feasible_prueba):
    print(indv[1])
    start_indv = time.time()
    error_indv = error.error(indv[1], 100, 40) # SNR 100  || NUM_VOX = 40
    end_indv = time.time()
    tiempo_indv = end_indv - start_indv

    print(f'Error del individuo {indx} = {error_indv}')
    
    tiempos.append(tiempo_indv)
    print(f'Tiempo tardado: {tiempo_indv}')
    print()

print(f'Tiempo promedio {np.mean(tiempos)}')
    



