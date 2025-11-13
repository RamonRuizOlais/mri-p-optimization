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
    print(f"Procesando generación {i}")
    return i, Do, meanmin, best[2], best[1]  # Generacion, Do, meanmin, error, TR


def main():
    # Parámetros
    n = 100
    max_workers = 20
    vect_TR = [x for x in range(100, 200 * n, 200)]

    # Cargar las poblaciones
    with open("POP_BNP_final.pkl", "rb") as f:
        POP_BNP = pickle.load(f)

    with open("POP_poblacional_final.pkl", "rb") as f:
        POP_SIN = pickle.load(f)

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
    df_Do_BNP.to_csv('Do_BNP.csv')
    df_meanmin_BNP.to_csv('meanmin_BNP.csv')
    df_best_BNP.to_csv('besterror_BNP.csv')
    df_TR_BNP.to_csv('TRbest_BNP.csv')

    df_Do_SIN.to_csv('Do_SIN.csv')
    df_meanmin_SIN.to_csv('meanmin_SIN.csv')
    df_best_SIN.to_csv('besterror_SIN.csv')
    df_TR_SIN.to_csv('TRbest_SIN.csv')


if __name__ == "__main__":
    main()

