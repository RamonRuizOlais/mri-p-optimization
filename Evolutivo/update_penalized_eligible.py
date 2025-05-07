# -*- coding: utf-8 -*-

import distance
import os

def update_penalized_eligible(S_newpop, S_penalized, S_eligible, th, vect_TR):
    S_eligible_new = []

    for i2 in range(len(S_eligible)):
        individual_2 = S_eligible[i2][0]
        sigue_siendo_elegible = True

        for i1 in range(len(S_newpop)):
            individual_1 = S_newpop[i1][0]
            dist = distance.distancia_promedio(individual_1, individual_2, vect_TR, max_workers=os.cpu_count())

            # Si no cumple el umbral, se penaliza
            if dist < th:
                sigue_siendo_elegible = False
                break

        if sigue_siendo_elegible:
            # Si sigue siendo elegible, lo agregamos a la nueva lista de elegibles
            S_eligible_new.append(S_eligible[i2])
        else:
            if S_eligible[i2] not in S_penalized:
                # Si no, lo agregamos a los penalizados si no está ya presente
                S_penalized.append(S_eligible[i2])

    return S_penalized, S_eligible_new
