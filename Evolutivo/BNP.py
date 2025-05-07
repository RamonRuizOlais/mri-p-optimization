# -*- coding: utf-8 -*-

import max_min
import update_penalized_eligible as upe

import best_in_pop as bp

# S_eligible: Union de la nueva generacion con la antigua generacion
# th: parámetro de mínima distancia
# indv: cantidad de individuos para la nueva población

def BNP(S_eligible, th, vect_TR, indv):
    S_penalized = []
    S_newpop = []

    while len(S_newpop) < indv:
        if S_eligible:
            best = bp.best_individual(S_eligible)  
            S_newpop.append(best)
            S_eligible.remove(best)
            
            # Calcular distancias de los elementos de la nueva población vs los elegibles
            S_penalized, S_eligible = upe.update_penalized_eligible(S_newpop, S_penalized, S_eligible, th, vect_TR)
            
        else:
            eligible_idv = max_min.max_min(S_newpop, S_penalized, vect_TR)
            S_newpop.append(eligible_idv)
            S_penalized.remove(eligible_idv)
    
    #print()
    #print(f'S_newpop: {len(S_newpop)}')
    #print(f'S_penalized: {len(S_penalized)}')
    #print(f'S_eligible: {len(S_eligible)}')
    #print()

    return S_newpop
    
