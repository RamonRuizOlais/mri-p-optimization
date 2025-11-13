# -*- coding: utf-8 -*-

import random
import json
import pandas as pd
from itertools import combinations
from ordenar_solucion import ordenar_solucion
from concurrent.futures import ProcessPoolExecutor, as_completed


def distancias(df_matriz_vox, num_vox, num_grupos=50):
    columnas_vox = [col for col in df_matriz_vox.columns if "vox" in col]
    indices_vox = list(range(len(columnas_vox)))

    df_matriz_vox["error_ref"] = df_matriz_vox[columnas_vox].mean(axis=1)
    orden_ref = df_matriz_vox.sort_values("error_ref")["Semilla"].tolist()
    print(f'Orden de refrencia de las soluciones: {orden_ref}')

    distancias_resultado = {}
    grupos_por_x = {}

    for x in range(1, 51):
        print(f"Evaluando grupos de {x} voxeles...")

        grupos = set()
        while len(grupos) < num_grupos:
            grupo = tuple(sorted(random.sample(indices_vox, x)))
            grupos.add(grupo)

        grupos = [[columnas_vox[i] for i in grupo] for grupo in grupos]
        grupos_por_x[str(x)] = grupos

        distancias_por_grupo = []
        nombres_columnas = []

        for grupo in grupos:
            df_tmp = df_matriz_vox[["Semilla"] + grupo].copy()
            df_tmp["error_grupo"] = df_tmp[grupo].mean(axis=1)
            orden_actual = df_tmp.sort_values("error_grupo")["Semilla"].tolist()

            distancia = sum(abs(orden_actual.index(s) - orden_ref.index(s)) for s in orden_ref)
            distancias_por_grupo.append(distancia)
            nombres_columnas.append(str(tuple(grupo)))

        # Guardar distancias individuales por grupo
        df_individual = pd.DataFrame([distancias_por_grupo], columns=nombres_columnas)
        df_individual.to_csv(f"distancias_{x}_vox.csv", index=False)

        # Guardar promedio de distancias para ese x
        distancia_promedio = sum(distancias_por_grupo) / len(distancias_por_grupo)
        distancias_resultado[f"{x} grupos"] = distancia_promedio

    # Guardar archivo de distancias resumidas y los grupos usados
    df_distancias = pd.DataFrame([distancias_resultado])
    df_distancias.to_csv("distancias_ordenref_nueva.csv", index=False)

    with open("grupos_aleatorios_por_x.json", "w") as f:
        json.dump(grupos_por_x, f, indent=2)

    return df_distancias
















'''
def distancias(df_matriz_vox, num_vox, num_grupos=50):
    columnas_vox = [col for col in df_matriz_vox.columns if "vox" in col]
    indices_vox = list(range(len(columnas_vox)))

    # Vector de referencia basado en error promedio en todos los voxeles
    df_matriz_vox["error_ref"] = df_matriz_vox[columnas_vox].mean(axis=1)
    orden_ref = df_matriz_vox.sort_values("error_ref")["Semilla"].tolist()
    
    print(f'Orden de refrencia de las soluciones: {orden_ref}')

    distancias_resultado = {}
    grupos_por_x = {}

    for x in range(1, 51):
        print(f"Evaluando grupos de {x} voxeles...")

        grupos = set()
        while len(grupos) < num_grupos:
            grupo = tuple(sorted(random.sample(indices_vox, x)))
            grupos.add(grupo)

        grupos = [[columnas_vox[i] for i in grupo] for grupo in grupos]
        grupos_por_x[str(x)] = grupos

        distancias_por_grupo = []
        for grupo in grupos:
            df_tmp = df_matriz_vox[["Semilla"] + grupo].copy()
            df_tmp["error_grupo"] = df_tmp[grupo].mean(axis=1)
            orden_actual = df_tmp.sort_values("error_grupo")["Semilla"].tolist()

            distancia = sum(abs(orden_actual.index(s) - orden_ref.index(s)) for s in orden_ref)
            distancias_por_grupo.append(distancia)

        distancia_promedio = sum(distancias_por_grupo) / len(distancias_por_grupo)
        distancias_resultado[f"{x} grupos"] = distancia_promedio

    # Guardar archivo de distancias y los grupos usados
    df_distancias = pd.DataFrame([distancias_resultado])
    df_distancias.to_csv("distancias_ordenref.csv", index=False)

    with open("grupos_aleatorios_por_x.json", "w") as f:
        json.dump(grupos_por_x, f, indent=2)

    return df_distancias
'''

