# -*- coding: utf-8 -*-
import random 
import feasible as feas
import error

def crossover_two_points(parents, vect_TR, SNR, num_vox):
    # Variables
    n = len(parents[0][0])
    pop_sons = []

    # Emparejamiento de los padres en índices pares e impares
    for (p1, _, _), (p2, _, _) in zip(parents[::2], parents[1::2]):

      # Particiones
      partitions = random.choices(range(n), k=2)
      partitions.sort()
      i1, i2 = partitions

      # Alternar partes de los padres a cada hijo
      s1 = p1[:i1] + p2[i1:i2] + p1[i2:]
      s2 = p2[:i1] + p1[i1:i2] + p2[i2:]

      # Hacer factibles a los hijos (x factible, TR)
      s1_feasible, tr_s1 = feas.ensure_feasible(s1, vect_TR, convert=True)
      s2_feasible, tr_s2 = feas.ensure_feasible(s2, vect_TR, convert=True)

      # Añadir hijos factibles (x, tr, error)
      pop_sons.append((s1_feasible, tr_s1, error.error(tr_s1, SNR, num_vox)))
      pop_sons.append((s2_feasible, tr_s2, error.error(tr_s2, SNR, num_vox)))

    return pop_sons
