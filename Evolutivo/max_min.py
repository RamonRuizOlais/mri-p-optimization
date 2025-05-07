# -*- coding: utf-8 -*-

import distance
import os

def max_min(S_newpop, S_penalized, vect_TR):
    eligible_idv = {
        i2: [
            distance.distancia_promedio(S_newpop[i1][0], S_penalized[i2][0], vect_TR, max_workers=os.cpu_count())
            for i1 in range(len(S_newpop))
        ]
        for i2 in range(len(S_penalized))
    }

    # Obtener el índice del individuo con la máxima de las mínimas distancias
    min_values = {key: min(value) for key, value in eligible_idv.items()}
    key_with_max_value = max(min_values.items(), key=lambda x: x[1])

    return S_penalized[key_with_max_value[0]]
    
