# -*- coding: utf-8 -*-

import random
import time
import numpy as np


import feasible as feas
import random_solution as rs
import distance as dis

import local_search as ls
import best_in_pop as bp
import comparison as cp

import selection as select
import crossover_two_points as ct


import Th
import BNP


class MTTPPoblacional:

    def __init__(self, soluciones):

        self.soluciones = soluciones


    def mttp_poblacional(self, n, vect_TR, SNR, num_vox, seed, M = 200):

        random.seed(seed)

        # Genera población inicial y asegura factibilidad
        pop_unfeasible = [rs.random_solution(n, vect_TR) for _ in range(self.soluciones)]
        pop_feasible = [feas.ensure_feasible(x, vect_TR, convert=True) for x in pop_unfeasible]

        # Busqueda local en la poblacion inicial (x, tr, f)
        star_bl= time.time()
        pop = ls.ejecutar_busqueda_local(pop_feasible, n, SNR, num_vox, vect_TR) 
       
        print(f'Termina la primera busqueda local: {time.time() - star_bl}')
        print()
        
     
        matrix = dis.distance_matrix(pop, vect_TR)
        D_0 = np.nanmean(matrix)
        meanmin_0 = np.mean(np.nanmin(matrix, axis=0))


        # Valores iniciales (minuto 0)
        best = bp.best_individual(pop)
        history = [best[2]]
        F_history = [[f for x, t, f in pop]]

        # Diversidad (minuto 0)
        th = D_0
        TH_LIST = [th]
        D = [D_0]
        meanmin = [meanmin_0]


        for m in range(M):
            start_indv = time.time()
            #tiempo_transcurrido = time.time() - tiempo_inicio

            if m != 20:
              # Valores cada 20 iteraciones
              matrix = dis.distance_matrix(pop, vect_TR)
              D_i = np.nanmean(matrix)
              meanmin_i = np.mean(np.nanmin(matrix, axis=0))

              D.append(D_i)
              meanmin.append(meanmin_i)
              TH_LIST.append(th)
              history.append(best[2])
              F_history.append([f for x, t, f in pop])


            # Poblacional
            parents = select.selection(pop, self.soluciones)
            sons = ct.crossover_two_points(parents, vect_TR, SNR, num_vox)
            
            star_bl= time.time()
            sons_ls = ls.ejecutar_busqueda_local(sons, n, SNR, num_vox, vect_TR)
            
            print(f'Termina la {m} busqueda local: {time.time() - star_bl}')
            print()
            
            th = Th.Th(m, M, D_0)


            #Crear nueva generacion
            eligible_pop = sons_ls[:] + pop[:]
            pop = BNP.BNP(eligible_pop, th, vect_TR, self.soluciones)

            # Actualizar la mejor solucion
            best_current = bp.best_individual(pop)
            best = cp.comparison(best[0], best[1], best[2], best_current[0], best_current[1], best_current[2])
            
            end_indv = time.time()
            tiempo_indv = end_indv - start_indv
            print(f"Tiempo de ejecución corrida {m}: {tiempo_indv} segundos")
            print()


        '''
        history: contiene la mejor solución hasta el momento cada 20 iteraciones
        D: lista de valores de diversidad (promedio de la matriz de distancias)
        best: mejor solución encontrada
        meanmin: promedio de las distancias mínimas de cada individuo
        '''
        return history, best, D, meanmin, F_history
