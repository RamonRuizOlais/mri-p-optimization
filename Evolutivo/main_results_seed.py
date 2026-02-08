# -*- coding: utf-8 -*-

import pickle
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor

import distance as dis
import best_in_pop as bp

def procesar_poblacion_indexed(indexed, vect_TR):
    i, poblacion = indexed
    matrix = dis.distance_matrix(poblacion, vect_TR)
    Do = np.nanmean(matrix)
    meanmin = np.mean(np.nanmin(matrix, axis=0))
    best = bp.best_individual(poblacion)
    return i, Do, meanmin, best[2], best[1]  # Generacion, Do, meanmin, error, TR


def main():
    # Parámetros
    n = 100
    max_workers = 20
    with open('TR.txt', 'r') as f:
        vect_TR = [int(x) for x in f.read().split()]

    # Cargar las poblaciones
    for w in range(10):
       with open(f"POP_final_{w}.pkl", "rb") as f:
          POP_SIN = pickle.load(f)
          
       with open(f"POP_BNP_final_{w}.pkl", "rb") as f:
          POP_BNP = pickle.load(f)
          
       print(f"Procesando semilla {w} BNP y POP")


       # Datas
       cols = [f'G{i}' for i in range(len(POP_BNP))]
       df_Do_BNP = pd.DataFrame(columns=cols, index=['Do'])
       df_meanmin_BNP = pd.DataFrame(columns=cols, index=['meanmin'])
       df_best_BNP = pd.DataFrame(columns=cols, index=['besterror'])
       df_TR_BNP = pd.DataFrame(columns=cols, index=['TRbest'])

       df_Do_SIN = pd.DataFrame(columns=cols, index=['Do'])
       df_meanmin_SIN = pd.DataFrame(columns=cols, index=['meanmin'])
       df_best_SIN = pd.DataFrame(columns=cols, index=['besterror'])
       df_TR_SIN = pd.DataFrame(columns=cols, index=['TRbest'])


       # Formato Generaciones (i, [pop])
       pop_bnp_indexed = list(enumerate(POP_BNP))
       pop_sin_indexed = list(enumerate(POP_SIN))

       with ProcessPoolExecutor(max_workers=max_workers) as executor:
          resultados_bnp = list(executor.map(procesar_poblacion_indexed, pop_bnp_indexed, [vect_TR] * len(pop_bnp_indexed)))
          resultados_sin = list(executor.map(procesar_poblacion_indexed, pop_sin_indexed, [vect_TR] * len(pop_sin_indexed)))


       # Insertar resultados en la posición correspondiente
       for i, Do, meanmin, besterror, TR in resultados_bnp:
          df_Do_BNP[f'G{i}'] = Do
          df_meanmin_BNP[f'G{i}'] = meanmin
          df_best_BNP[f'G{i}'] = besterror
          df_TR_BNP[f'G{i}'] = [TR]

       for i, Do, meanmin, besterror, TR in resultados_sin:
          df_Do_SIN[f'G{i}'] = Do
          df_meanmin_SIN[f'G{i}'] = meanmin
          df_best_SIN[f'G{i}'] = besterror
          df_TR_SIN[f'G{i}'] = [TR]


       # Crear datas a .csv
       df_Do_BNP.to_csv(f'Do_BNP_{w}.csv')
       df_meanmin_BNP.to_csv(f'meanmin_BNP_{w}.csv')
       df_best_BNP.to_csv(f'besterror_BNP_{w}.csv')
       df_TR_BNP.to_csv(f'TRbest_BNP_{w}.csv')

       df_Do_SIN.to_csv(f'Do_POP_{w}.csv')
       df_meanmin_SIN.to_csv(f'meanmin_POP_{w}.csv')
       df_best_SIN.to_csv(f'besterror_POP_{w}.csv')
       df_TR_SIN.to_csv(f'TRbest_POP_{w}.csv')


if __name__ == "__main__":
    main()

