# -*- coding: utf-8 -*-
import sys
from poblacional import RMPoblacional

def main(SNR, num_vox, seed):
    # Parámetros fijos
    n = 100
    soluciones = 30
    M = 100
    with open('TR.txt', 'r') as f:
        vect_TR = [int(x) for x in f.read().split()]

    print("Inicia ejecución del algoritmo sin BNP")

    rm_pop = RMPoblacional(soluciones)
    POP, best, history, F_history = rm_pop.rm_poblacional(n, vect_TR, SNR, num_vox, seed, M)

    print("Termina ejecución del algoritmo sin BNP")
    print()
    print(best)

if __name__ == "__main__":
    SNR = int(sys.argv[1])      # Ejemplo: 100
    num_vox = int(sys.argv[2])  # Ejemplo: 40
    seed = int(sys.argv[3])     # Semilla de ejecucion
    main(SNR, num_vox, seed)

