from statistics import mean

def ordenar_solucion(fila, grupos_por_x):
    semilla = fila["Semilla"]
    resultados = {"Semilla": semilla}

    for x, grupos in grupos_por_x.items():
        errores_en_grupos = []

        for grupo in grupos:
            if len(grupo) == 1:
                errores_en_grupos.append(fila[grupo[0]])
            else:
                errores_en_grupos.append(fila[grupo].mean())

        error_promedio = mean(errores_en_grupos)
        resultados[f"{x} grupos"] = error_promedio

    return resultados

