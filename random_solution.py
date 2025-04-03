# -*- coding: utf-8 -*-

import random 

def random_solution(n,  vect_TR, tr_lim =  10_000):
    indices_permitidos = [i for i in range(n) if vect_TR[i] <= tr_lim]  # Índices válidos
    num_seleccionados = random.randint(1, len(indices_permitidos)) 
    seleccionados = set(random.sample(indices_permitidos, num_seleccionados))  
    
    return [1 if i in seleccionados else 0 for i in range(n)]  

    #return random.choices([0, 1], k=n)
