# -*- coding: utf-8 -*-

import time
import sys
from poblacional import MTTPPoblacional

def main(SNR, num_vox):
    # Parámetros fijos
    n = 100
    soluciones = 50
    M = 1  # solo una corrida para prueba
    vect_TR = [x for x in range(100, 200 * n, 200)]  # TRs simulados

    mttp_trajectory = MTTPPoblacional(soluciones)

    # Ejecución
    seed = 1
    #start_indv = time.time()

    history, best, iteraciones, D, meanmin, F_history = mttp_trajectory.mttp_poblacional(
        n, vect_TR, SNR, num_vox, seed, M
    )

    #end_indv = time.time()
    #tiempo_indv = end_indv - start_indv

    # ---------------- RESULTADOS ----------------
    print("========== RESULTADOS DE LA PRUEBA ==========")
    #print(f"Tiempo de ejecución de una corrida: {tiempo_indv:.2f} segundos")
    print(f"Mejor solución de todas: {best}")

if __name__ == "__main__":
    # Parámetros desde línea de comandos
    SNR = int(sys.argv[1])      # Ejemplo: 100
    num_vox = int(sys.argv[2])  # Ejemplo: 40

    main(SNR, num_vox)

