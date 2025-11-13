# -*- coding: utf-8 -*-
import pandas as pd
import multiprocessing
import error  # Importar la librería de error

def process_row(args):
    binary, old_error, vect_TR, SNR, num_vox = args  # Se mantiene el error previo para comparación
    selected_TRs = [tr for bit, tr in zip(binary, vect_TR) if bit == 1]
    new_error = error.error(selected_TRs, SNR, num_vox)  # Calcular el nuevo error
    binary_TR = int("".join(map(str, binary)), 2)  # Convertir TR binario a entero
    print(f"Nuevo error calculado: {new_error}")  # Imprimir el nuevo error en consola
    return (old_error, new_error, binary_TR)

def main():
    # Parámetros para el cálculo del error
    SNR = 400
    num_vox = 20
    
    # Cargar el archivo CSV
    file_path = "Data_vox2.csv"
    single_sawp_vox2 = pd.read_csv(file_path, dtype={"Entero": str})  # Leer 'Entero' como string para evitar OverflowError
    single_sawp_vox2["Entero"] = single_sawp_vox2["Entero"].apply(lambda x: int(float(x)))  # Convierte de float a int 

    vect_TR = [i for i in range(100, 20000, 200)]
    
    # Filtrar el DataFrame con los mejores 3 errores y hacer una copia explícita
    #best_error_values = single_sawp_vox2.nsmallest(3, 'Error')['Error'].unique()
    best_error_values = (single_sawp_vox2['Error'].sort_values()).unique()[:3]
    filtered_df = single_sawp_vox2[single_sawp_vox2['Error'].isin(best_error_values)].copy()

    
    # Convertir los valores enteros en listas binarias de longitud fija
    filtered_df['Entero'] = filtered_df['Entero'].apply(lambda x: int(float(x)))  # Convertir de forma segura
    max_length = len(bin(filtered_df['Entero'].max())[2:])  # Longitud máxima del binario
    binary_lists = [list(map(int, bin(num)[2:].zfill(max_length))) for num in filtered_df['Entero']]
    
    # Obtener los errores originales
    error_list = filtered_df['Error'].tolist()
    
    #print(error_list)
    
    # Preparar los datos para el procesamiento paralelo
    data = list(zip(binary_lists, error_list, [vect_TR] * len(binary_lists), [SNR] * len(binary_lists), [num_vox] * len(binary_lists)))
    
    # Usar multiprocessing para paralelizar la conversión y cálculo del error
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        new_error_data = pool.map(process_row, data)
    
    # Crear un nuevo DataFrame con errores y TR binario convertido a entero
    new_error_df = pd.DataFrame(new_error_data, columns=['Old_Error', 'New_Error', 'Binary_TR'])
    
    # Guardar el resultado en un nuevo CSV
    print(new_error_df)
    new_error_df.to_csv("new_error_results.csv", index=False)
    
    print("Procesamiento completado en paralelo. Resultados guardados en new_error_results.csv")


if __name__ == "__main__":
    main()
