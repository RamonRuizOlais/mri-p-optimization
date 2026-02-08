# -*- coding: utf-8 -*-

import pandas as pd
import random
import error
import comparison
import feasible as feas
import random_solution as rs

def single_sawp(n, seed, SNR, num_vox):
    random.seed(seed)

    with open('TR.txt', 'r') as f:
        vect_TR = [int(x) for x in f.read().split()]
        
    x = rs.random_solution(n, vect_TR)
    x, TR = feas.ensure_feasible(x, vect_TR, convert=True)
    
    # DataFrame
    name = f"single_sawp_{seed}.csv"
    columnas = ['Entero', 'Suma', 'Error', 'No. Voxeles']
    df = pd.DataFrame(columns=columnas)
    
    # Evaluar solución inicial
    best_x = x[:]
    best_TR = TR[:]
    best_entero = int(''.join(map(str, x)), 2)
    best_error = error.error(TR, SNR, num_vox)
    df.loc[len(df)] = [best_entero, sum(best_TR), best_error, num_vox]
    
    # Bandera 
    mejora = True
    indices = random.sample(range(n), n)  # Permutación 
    
    while mejora:
        mejora = False
        
        for i in indices:
            x_temp = best_x[:]
            x_temp[i] = 1 - best_x[i]  # Cambio 0 <-> 1
            
            # Verificar factibilidad
            flag, TR_waiting = feas.ensure_feasible(x_temp, vect_TR)
            if flag:
                df.loc[len(df)] = [int(''.join(map(str, x_temp)), 2), sum(TR_waiting), error.error(TR_waiting, SNR, num_vox), num_vox]
                
                # Comparar soluciones y decidir si mantener el cambio
                x_best, TR_best, error_best = comparison.comparison(best_x, best_TR, x_temp, TR_waiting, SNR, num_vox)
                
                if x_best == x_temp:
                    best_x, best_TR, best_error, best_entero = x_temp, TR_best, error_best, int(''.join(map(str, x_temp)), 2)
                    
                    mejora = True  # Hubo mejora, seguimos iterando
                    
                    # Cambio aleatorio circular sobre la nueva solución
                    indices = random.sample(list(range(i + 1, n)) + list(range(0, i)), n - 1) 
                    break  # Reiniciamos la iteración con la nueva mejor solución
    
    df.to_csv(name, index=False)
    
    return best_entero, best_error

