# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

import sys
import os
import itertools

from statistics import mean
from concurrent.futures import ProcessPoolExecutor, as_completed

from distancias import distancias
import calculate_error as ce
    
def matriz_vox(SNR, num_vox):
    # Parámetros fijos
    n = 100
    n_semillas = 200
    
    registros = []
    orden_ref = []  
    columnas = ['Semilla', 'TR'] + [f"{i+1}vox" for i in range(num_vox)]

    max_workers = min(n_semillas, os.cpu_count())
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(ce.calculate_error, n, seed, SNR, num_vox): seed
            for seed in range(1, n_semillas + 1)
        }

        for future in as_completed(futures):
            seed = futures[future]
            try:
                TR, alpha_errors = future.result()
                
                # Calcular y guardar promedio del error alpha por solución
                media_error = mean(alpha_errors)
                orden_ref.append((seed, media_error))

                # Crear la fila con: [semilla, TR, error1, error2, ..., errornum_vox]
                fila = [seed, TR] + list(alpha_errors)
                registros.append(fila)

            except Exception as e:
                print(f"Error en la semilla {seed}: {e}")

    # Crear DataFrame y guardar
    df_matriz_vox = pd.DataFrame(registros, columns=columnas)
    df_matriz_vox.to_csv(f"matriz_vox_{num_vox}.csv", index=False)
    print(f"Matriz guardada")
    
    # Ordenar semillas por menor error promedio
    orden_ref.sort(key=lambda x: x[1])  
    orden_seed_ref = [elem[0] for elem in orden_ref]

    return df_matriz_vox, orden_seed_ref


def main(SNR, num_vox):
    
    print("Obtenuendo matriz de errores")
    df_matriz_vox, orden_seed_ref = matriz_vox(SNR, num_vox)
    print()
    #print("Columnas de df_matriz_vox:", df_matriz_vox.columns.tolist())

    print("Obteniendo ordenamientos y distancias")
    df_distancias = distancias(df_matriz_vox, num_vox)

    print()
    print("Finalizado")


if __name__ == "__main__":
    # Parámetros obligatorios
    SNR = int(sys.argv[1])  # Ejemplo: 100
    num_vox = int(sys.argv[2])  # Ejemplo: 200
    main(SNR, num_vox)

