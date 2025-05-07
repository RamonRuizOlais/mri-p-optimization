# -*- coding: utf-8 -*-

import time

from poblacional import MTTPPoblacional



def main(SNR, num_vox):
    # Parámetros Fijos
    n = 100
    
    soluciones = 50 # 50
    M = 1 #200
    vect_TR = [x for x in range(100, 200 * n, 200)]
    
    mttp_trajectory = MTTPTrajectory(soluciones)
    
    # Ejecucion prueba
    seed = 10
    
    start_indv = time.time()
    
    history, best, iteraciones, D, meanmin, F_history =  mttp_trajectory.mttp_poblacional(
    n, vect_TR, SNR, num_vox, seed, M)
    
    end_indv = time.time()
    tiempo_indv = end_indv - start_indv
    
    # ---------------- RESULTADOS ----------------
    print("========== RESULTADOS DE LA PRUEBA ==========")
    print(f'Tiempo de ejecucion de una corrida: {tiempo_indv}')
    print(f'Mejor solucion de todas: {best}')


if __name__ == "__main__":
    # Parámetros obligatorios
    SNR = int(sys.argv[1])  # Real: 100
    num_vox = int(sys.argv[2])  # Real: 40
    
    main(SNR, num_vox)

