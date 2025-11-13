# -*- coding: utf-8 -*-

import random 
import time

import error 
import comparison
import feasible as feas
import random_solution as rs
import convert_TR as ctr

import set_sawp as setsawp

class RMTrajectory:
    def __init__(self, p):
        self.p = p


    def disturbance(self, x, vect_TR):
        realized = [i for i, e in enumerate(x) if e == 1]
        deselect = random.sample(realized, int(round(self.p * len(realized))))

        x_copy = [0 if i in deselect else x[i] for i, e in enumerate(x)]

        return x_copy, ctr.convert_to_TR(x_copy, vect_TR)



    def ls_disturbance(self, n, SNR, num_vox, seed, tiempo_limite):
        random.seed(seed)
        vect_TR = [x for x in range(100, 100*(n + 1), 100)]

        x = rs.random_solution(n)
        x, TR = feas.ensure_feasible(x, vect_TR, convert=True)

        # Valores iniciales (minuto 0)
        x_best = x[:]
        TR_best = TR[:]
        f_best = error.error(TR_best, SNR, num_vox)
        history_f = [f_best]
        history_tr = [TR_best]

        # Tiempo de inicio
        tiempo_inicio = time.time()
        iteracion = 0

        ultimo_registro = tiempo_inicio

        while True:
            tiempo_transcurrido = time.time() - tiempo_inicio

            # 120 en vez de 2
            if time.time() - ultimo_registro >= 120:
              # Valores cada 2 minutos
              f_best = error.error(TR_best, SNR, num_vox)
              history_f.append(f_best)
              history_tr.append(TR_best)
              ultimo_registro += 120

            # Verificar si se ha alcanzado el límite de tiempo
            if tiempo_transcurrido >= tiempo_limite:
                break

            iteracion += 1
            x_ls, TR_ls = setsawp.set01_sawp01(x_best, TR_best, vect_TR, SNR, num_vox)
            x_p, TR_p = self.disturbance(x_ls, vect_TR)
            x_f, TR_f = setsawp.set01_sawp01(x_p, TR_p, vect_TR, SNR, num_vox)

            #¿Cuál es mejor?
            x_win, TR_win = comparison.comparison( x_ls, TR_ls , x_f, TR_f, SNR, num_vox)

            if x_win == x_ls:
              new_best_x, new_TR_best = x_ls, TR_ls
            else:
              new_best_x, new_TR_best, = x_f, TR_f
            
            #¿Cuál es mejor?
            x_maxwin, TR_maxwin = comparison.comparison(new_best_x, new_TR_best, x_best, TR_best, SNR, num_vox)

            if x_maxwin == new_best_x:
              x_best, TR_best = new_best_x, new_TR_best

        '''
        history: contiene la mejor solución hasta el momento cada 2 minutos
        (x_best, TR_best): mejor solución encontrada
        '''
        return history_f, history_tr, (x_best, TR_best), iteracion
