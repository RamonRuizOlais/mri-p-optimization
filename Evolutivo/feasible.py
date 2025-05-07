# -*- coding: utf-8 -*-

import convert_TR as ctr
import random

def ensure_feasible(x, vect_TR, convert=False, tr_lim=50_000):
    x_copy = x[:]
    sum_tr_copy = sum(vect_TR[i] for i, val in enumerate(x_copy) if val == 1)
    
    # Si la suma de TRs excede el límite, ajustar eliminando TRs hasta que sea factible
    if sum_tr_copy > tr_lim:
        if not convert:
            return False, None

        # Lista de índices seleccionados
        S = [i for i, val in enumerate(x_copy) if val == 1]
        random.shuffle(S)  

        for i in S:
            x_copy[i] = 0  # Quitar TR
            #sum_tr_copy -= vect_TR[i]
            sum_tr_copy  = sum(vect_TR[i] for i, val in enumerate(x_copy) if val == 1)

            # Si la solución ya es factible, detenerse y retornar
            if sum_tr_copy <= tr_lim and sum_tr_copy > 0:
                return (x_copy, ctr.convert_to_TR(x_copy, vect_TR))
    
    # Si se eliminaron todos los TRs, seleccionar uno válido aleatorio
    posibles_indices = [i for i in range(len(vect_TR)) if vect_TR[i] <= tr_lim]  # TRs que caben en el límite
    if not any(x_copy) and posibles_indices:
        idx = random.choice(posibles_indices)  # Seleccionamos uno aleatoriamente
        x_copy[idx] = 1
        sum_tr_copy = vect_TR[idx]
    
    # Recalcular sum_tr_copy después de corrección final
    sum_tr_copy = sum(vect_TR[i] for i, val in enumerate(x_copy) if val == 1)
    
    return (x_copy, ctr.convert_to_TR(x_copy, vect_TR)) if convert else (True, ctr.convert_to_TR(x_copy, vect_TR))

