# -*- coding: utf-8 -*-

import random
import time
import os
import numpy as np
import pandas as pd
import sys
import itertools
from concurrent.futures import ProcessPoolExecutor, as_completed
import single_sawp as ssn  # Corrección del import

def convertir_data(datafeo):
  nombre = datafeo + ".csv"
  data_feo_nombre = pd.read_csv(nombre)

  # Crear un DataFrame con una única fila, extrayendo los valores no NaN
  condensed_row = pd.Series(dtype=object, index=data_feo_nombre.columns)

  for col in data_feo_nombre.columns:
     non_nan_values = data_feo_nombre[col].dropna().values
     if non_nan_values.size > 0:
        condensed_row[col] = non_nan_values[0]  # Tomar el primer valor no NaN

  # Convertir la serie en DataFrame con una única fila
  data_feo_nombre = pd.DataFrame([condensed_row])
  data_feo_nombre.to_csv(nombre, index=False)


  # Mostrar el DataFrame
  from IPython.display import display
  display(data_feo_nombre)
  #return data_feo_nombre

def main(SNR, num_vox):
    # Parámetros Fijos
    n = 100
    n_semillas = 30
    
    
    # Crear DataFrames con columnas como enteros
    df_best_error = pd.DataFrame(columns=range(1, n_semillas + 1))
    df_best_entero = pd.DataFrame(columns=range(1, n_semillas + 1))
    
    # Usar número óptimo de workers para no saturar la CPU
    max_workers = min(n_semillas, os.cpu_count())
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(ssn.single_sawp, n, seed, SNR, num_vox): seed  
            for seed in range(1, n_semillas + 1)
        }

        for future in as_completed(futures):
            seed = futures[future]
            
            try:
                best_entero, best_error = future.result()
                
                # Agregar resultados a los DataFrames sin sobrescribir
                df_best_entero.loc[len(df_best_entero), seed] = best_entero
                df_best_error.loc[len(df_best_error), seed] = best_error
                
                print(f"Semilla {seed} completada: Entero = {best_entero}, Error = {best_error}")

            except Exception as e:
                print(f"Error en la semilla {seed}: {e}")
    
    
    # Guardar resultados
    df_best_entero.to_csv("best_results_enteros.csv", index=False)
    df_best_error.to_csv("best_results_errores.csv", index=False)

    # Arreglar formato
    convertir_data(datafeo='best_results_errores')
    convertir_data(datafeo='best_results_enteros')
    
    print("Ejecución completada. Resultados guardados.")
    
    
    #print(ssn.single_sawp(100, 3, SNR, num_vox))

if __name__ == "__main__":
    # Parámetros obligatorios
    SNR = int(sys.argv[1])  # Ejemplo: 400
    num_vox = int(sys.argv[2])  # Ejemplo: 2
    
    main(SNR, num_vox)

