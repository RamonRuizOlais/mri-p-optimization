# -*- coding: utf-8 -*-

import numpy as np
import itertools
import os
from concurrent.futures import ProcessPoolExecutor

# Obtener el TR más cercano de x_basea a x_comp
def distancia_individual(i, x_base, x_comp, vector_TR):
    if x_comp[i] == 1:
        return 0

    n = len(vector_TR)
    min_dist = float('inf')

    for j in range(i - 1, -1, -1):
        if x_comp[j] == 1:
            min_dist = abs(vector_TR[i] - vector_TR[j])
            break

    for j in range(i + 1, n):
        if x_comp[j] == 1:
            dist = abs(vector_TR[i] - vector_TR[j])
            min_dist = min(min_dist, dist)
            break

    if min_dist == float('inf'):
        return vector_TR[i]

    return min_dist



def calculate_distance(args):
    return distancia_individual(*args)
    

# Obtener distancia de x1 a x2 y de x2 a x1
def distancia_promedio(x1, x2, vector_TR, max_workers=None):
    n = len(vector_TR)
    indices_1 = [i for i in range(n) if x1[i] == 1]
    indices_2 = [i for i in range(n) if x2[i] == 1]

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
    
        args_1 = [(i, x1, x2, vector_TR) for i in indices_1]
        args_2 = [(i, x2, x1, vector_TR) for i in indices_2]

        distancias_1 = list(executor.map(calculate_distance, args_1))
        distancias_2 = list(executor.map(calculate_distance, args_2))

    total_dist = sum(distancias_1) + sum(distancias_2)
    total_ops = len(distancias_1) + len(distancias_2)

    return total_dist / total_ops if total_ops > 0 else 0.0
    
    

def distance_matrix(pop, vect_TR):
    individuals = len(pop)
    matrix = np.full((individuals, individuals), np.nan)

    for i1, i2 in itertools.combinations(range(individuals), 2):
        individual_1 = pop[i1][0]  # Lista de TRs seleccionados del individuo i1
        individual_2 = pop[i2][0]  # Lista de TRs seleccionados del individuo i2
        distancia = distancia_promedio(individual_1, individual_2, vect_TR, max_workers=os.cpu_count())
        matrix[i1][i2] = distancia
        matrix[i2][i1] = distancia

    return matrix
