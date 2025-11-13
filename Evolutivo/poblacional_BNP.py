# -*- coding: utf-8 -*-

import random
import time
import numpy as np
import pickle

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


class RMPoblacional_BNP:

    def __init__(self, soluciones):

        self.soluciones = soluciones
        
    def rm_poblacional_bnp(self, n, vect_TR, SNR, num_vox, seed, M=100):
        random.seed(seed)

        # Genera población inicial y asegura factibilidad
        pop_unfeasible = [rs.random_solution(n, vect_TR) for _ in range(self.soluciones)]
        pop_feasible = [feas.ensure_feasible(x, vect_TR, convert=True) for x in pop_unfeasible]

        # Búsqueda local en la población inicial
        pop = ls.ejecutar_busqueda_local(pop_feasible, n, SNR, num_vox, vect_TR)

        # Almacenar valores iniciales
        POP = [pop]
        best = bp.best_individual(pop)
        history = [best[2]]
        F_history = [[f for x, t, f in pop]]

        # Diversidad inicial
        matrix = dis.distance_matrix(pop, vect_TR)
        D_0 = np.nanmean(matrix)
        th = D_0

        for m in range(M):
            start_indv = time.time()

            parents = select.selection(pop, self.soluciones)
            sons = ct.crossover_two_points(parents, vect_TR, SNR, num_vox)
            sons_ls = ls.ejecutar_busqueda_local(sons, n, SNR, num_vox, vect_TR)

            th = Th.Th(m, M, D_0)
            eligible_pop = sons_ls[:] + pop[:]
            pop = BNP.BNP(eligible_pop, th, vect_TR, self.soluciones)

            best_current = bp.best_individual(pop)
            best = cp.comparison(best[0], best[1], best[2], best_current[0], best_current[1], best_current[2])

            tiempo_indv = time.time() - start_indv
            print(f"Tiempo de ejecución corrida BNP {m}: {tiempo_indv} segundos")

            POP.append(pop)
            history.append(best[2])
            F_history.append([f for x, t, f in pop])

            # Guardar en .pkl cada 10 iteraciones
            if m % 20 == 0:
                with open(f"POP_BNP_iter{m}_seed{seed}.pkl", "wb") as f:
                    pickle.dump(POP, f)

        # Guardar versión final al terminar
        with open(f"POP_BNP_final_{seed}.pkl", "wb") as f:
            pickle.dump(POP, f)

        '''
        POP: lista de las poblaciones (listas de tuplas (x, tr, f))
        history: contiene el mejor error encontrado en cada generación
        best: mejor solución encontrada
        F_history: todos los errores de la población en cada generación
        '''
        return POP, best, history, F_history

