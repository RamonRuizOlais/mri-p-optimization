# -*- coding: utf-8 -*-

import pandas as pd
import random
import error
import comparison as cp
import feasible as feas
import random_solution as rs
import time

def single_sawp(x, TR, n, SNR, num_vox, vect_TR):
    start_ls = time.time()
    time_limit = 1800  # 30 minutos en segundos
    
    # Lo mejor hasta ahora
    x_best = x[:]
    TR_best = TR[:]
    f_best = error.error(TR_best, SNR, num_vox) #1.5 minutos aprox


    # Bandera
    mejora = True
    indices = random.sample(range(n), n)  # Permutación

    while mejora and (time.time() - start_ls < time_limit):
        mejora = False

        for i in indices:
            x_temp = x_best[:]
            x_temp[i] = 1 - x_best[i]  # Cambio 0 <-> 1

            # Verificar factibilidad
            flag, TR_waiting = feas.ensure_feasible(x_temp, vect_TR)

            if flag:
                # Comparar soluciones y decidir si mantener el cambio
                f_temp = error.error(TR_waiting, SNR, num_vox) #1.5 minutos aprox
                x_win, TR_win, f_win = cp.comparison(x_best, TR_best, f_best, x_temp, TR_waiting, f_temp)

                if x_win == x_temp:
                    x_best, TR_best, f_best = x_temp, TR_win, f_win

                    mejora = True  # Hubo mejora, seguimos iterando
                    #print('Sigo mejorando')

                    # Cambio aleatorio circular sobre la nueva solución
                    indices = random.sample(list(range(i + 1, n)) + list(range(0, i)), n - 1)
                    break  # Reiniciamos la iteración con la nueva mejor solución

    #print(f'TERMINA: {TR_best} con {f_best}')
    end_ls = time.time()
    tiempo_ls = end_ls - start_ls
    print(f'Tiempo de la busqueda local: {tiempo_ls}')
    
    return x_best, TR_best, f_best

