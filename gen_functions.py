#%%---------------------------------------------------------------------------------------------
# Importación de librerías
#-----------------------------------------------------------------------------------------------

import numpy as np
import math
from scipy.optimize import curve_fit

#%%---------------------------------------------------------------------------------------------
# Funciones originales de Erick/Daniel (Necesarias para EPG)
#-----------------------------------------------------------------------------------------------

#   Código de generación de señales sintéticas
#   @Author Daniel Vallejo Aldana
#   @Institution CIMAT / Ecole Polytechnique Federale de Lausanne (EPFL)
#   Bug fixing - Adjusting the T2 generation signals to a certain SNR
'''
@Author Erik Canales
'''
def fill_S(n):
    the_size = 3*n + 1
    #print(n)
    S = np.zeros((the_size,the_size))
    S[0,2]=1.0
    S[1,0]=1.0
    S[2,5]=1.0
    S[3,3]=1.0
    for o in range(2,n+1):
        offset1=( (o-1) - 1)*3 + 2
        offset2=( (o+1) - 1)*3 + 3
        if offset1<=(3*n+1):
            S[3*o-2,offset1-1] = 1.0  # F_k <- F_{k-1}
        # end
        if offset2<=(3*n+1):
            S[3*o-1,offset2-1] = 1.0  # F_-k <- F_{-k-1}
        # end
        S[3*o,3*o] = 1.0              # Z_order
    # end for
    return S
#end fun

def fill_T(n, alpha):
    T0      = np.zeros((3,3))
    T0[0,:] = [math.cos(alpha/2.0)**2, math.sin(alpha/2.0)**2,  math.sin(alpha)]
    T0[1,:] = [math.sin(alpha/2.0)**2, math.cos(alpha/2.0)**2, -math.sin(alpha)]
    T0[2,:] = [-0.5*math.sin(alpha),   0.5*math.sin(alpha),     math.cos(alpha)]

    T = np.zeros((3*n + 1, 3*n + 1))
    T[0,0] = 1.0
    T[1:3+1, 1:3+1] = T0
    for itn in range(n-1):
        T[(itn+1)*3+1:(itn+2)*3+1,(itn+1)*3+1:(itn+2)*3+1] = T0
    # end
    return T
#end fun

def fill_R(n, tau, R0, R2):
    R  = np.zeros((3*n + 1, 3*n + 1))
    R[0,0] = np.exp(-tau*R2)
    R[1:3+1, 1:3+1] = R0
    for itn in range(n-1):
        R[(itn+1)*3+1:(itn+2)*3+1,(itn+1)*3+1:(itn+2)*3+1] = R0
    # end
    return R
#end fun

#%%---------------------------------------------------------------------------------------------
# Código modificado por mí (original de Erick/Daniel) (Necesario para EPG)
#-----------------------------------------------------------------------------------------------

# Functions to generate the Dictionary of multi-echo T2 signals using the EPG model
def create_met2_design_matrix_epg(Npc, T2s, T1s, nEchoes, tau, flip_angle, TR, TE_start):
    '''
    Creates the Multi Echo T2 (spectrum) design matrix.
    Given a grid of echo times (numpy vector TEs) and a grid of T2 times
    (numpy vector T2s), it returns the deign matrix to perform the inversion.
    *** Here we use the epg model to simulate signal artifacts
    '''
    design_matrix = np.zeros((nEchoes, Npc))
    rad           = np.pi/180.0  # constant to convert degrees to radians
    for cols in range(Npc):
        signal = (1.0 - np.exp(-TR/T1s[cols])) * epg_signal(nEchoes, tau, np.array([1.0/T1s[cols]]), np.array([1.0/T2s[cols]]), flip_angle * rad, flip_angle/2.0 * rad, TE_start)
        #signal = (1.0 - np.exp(-TR/T1s[cols])) * epg_signal(nEchoes, tau, np.array([1.0/T1s[cols]]), np.array([1.0/T2s[cols]]), flip_angle * rad, 90.0 * rad)
        design_matrix[:, cols] = signal.flatten()
        # end for row
    return design_matrix
#end fun

def epg_signal(n, tau_in, R1vec, R2vec, alpha, alpha_exc, TE_start=0):

    nRates = R2vec.shape[0]
    #tau = tau_in / 2.0

    # Definir la matriz de señal
    H = np.zeros((n, nRates))

    # Matriz de mezcla RF
    T = fill_T(n, alpha)

    # Matriz de selección para mover todos los estados de coherencia
    S = fill_S(n)

    for iRate in range(nRates):
        # Relajación inicial para R1 y R2
        R2 = R2vec[iRate]
        R1 = R1vec[iRate]

         #Inicializar el vector de magnetización
        x = np.zeros((3 * n + 1, 1), dtype=np.float64)
        x[0] = np.sin(alpha_exc)  # Magnetización transversal inicial (F_0)
        x[1] = 0.0
        x[2] = np.cos(alpha_exc)  # Magnetización longitudinal inicial (Z_0)
        
        for iEcho in range(n):
            if iEcho == 0:
                tau = TE_start/2.0
            else:
                tau = tau_in/2.0
            R0 = np.zeros((3, 3))
            R0[0, 0] = np.exp(-tau * R2)  # Relajación transversal (T2)
            R0[1, 1] = np.exp(-tau * R2)  # Relajación transversal (T2)
            R0[2, 2] = np.exp(-tau * R1)  # Relajación longitudinal (T1)

            R = fill_R(n, tau, R0, R2)
            
            # Precesión y relajación
            P = np.dot(R, S)
            E = np.dot(np.dot(P, T), P)

            # Actualizar la magnetización
            x = np.dot(E, x)

            # Guardar la señal transversal correspondiente al tiempo de eco actual
            H[iEcho, iRate] = x[0][0]

    return H
#end fun

#%%---------------------------------------------------------------------------------------------
# Funciones definidas por mi
#-----------------------------------------------------------------------------------------------

# Generador de valores de T2 para la mielina
def T2_myelin(lower_bounds, upper_bounds):
    valores_T2 = np.linspace(lower_bounds[3], upper_bounds[3], num=100)  # ajusta el número de valores según sea necesario
    return np.random.choice(valores_T2)

# Generador de valores de T2 para intra-extra
def T2_IE(lower_bounds, upper_bounds):
    valores_T2 = np.linspace(lower_bounds[5], upper_bounds[5], num=100)  # ajusta el número de valores según sea necesario
    return np.random.choice(valores_T2)

# Generador de valores de T2 para CSF
def T2_CSF(lower_bounds, upper_bounds):
    valores_T2 = np.linspace(lower_bounds[7], upper_bounds[7], num=100)  # ajusta el número de valores según sea necesario
    return np.random.choice(valores_T2)

# Generador de valores de T1 para la mielina
def T1_myelin(lower_bounds, upper_bounds):
    valores_T1 = np.linspace(lower_bounds[2], upper_bounds[2], num=100)  # ajusta el número de valores según sea necesario
    return np.random.choice(valores_T1)

# Generador de valores de T1 para intra-extra
def T1_IE(lower_bounds, upper_bounds):
    valores_T1 = np.linspace(lower_bounds[4], upper_bounds[4], num=100)  # ajusta el número de valores según sea necesario
    return np.random.choice(valores_T1)

# Generador de valores de T1 para CSF
def T1_CSF(lower_bounds, upper_bounds):
    valores_T1 = np.linspace(lower_bounds[6], upper_bounds[6], num=100)  # ajusta el número de valores según sea necesario
    return np.random.choice(valores_T1)

# Función para agregar ruido riciano dado un SNR
def add_rician_noise(data, SNR):
    sigma = np.max(data)/SNR
    noisy_data = np.sqrt((data + np.random.normal(0, sigma, data.shape))**2 + np.random.normal(0, sigma, data.shape)**2)
    return noisy_data

# Generar la matriz de diseño EPG para cada TR
def generate_epg_matrix(TR_values, Npc, T2s, T1s, nEchoes, tau, flip_angle, TE_start):
    design_matrices = []
    for tr in TR_values:
        design_matrix_tr = create_met2_design_matrix_epg(
            Npc=Npc,
            T2s=T2s,
            T1s=T1s,
            nEchoes=nEchoes,
            tau=tau,
            flip_angle=flip_angle,
            TR=tr,
            TE_start=TE_start
        )
        design_matrices.append(design_matrix_tr)
    return design_matrices

# Reorganizamos la matriz a un formato con el que ya he estado trabajando
def reorganize_design_matrices(design_matrices):

    # Extraemos el número de TR (número de matrices en la lista)
    num_TR = len(design_matrices)
    
    # Extraemos el número de TE (número de filas en cada matriz individual)
    num_TE = design_matrices[0].shape[0]
    
    # Crear una matriz vacía con el tamaño adecuado (6 x 5)
    reorganized_matrix = np.zeros((num_TR, num_TE))
    
    # Llenar la matriz reorganizada con los valores de cada matriz en la lista
    for i, matrix in enumerate(design_matrices):
        reorganized_matrix[i, :] = matrix.flatten()  # Convertimos cada columna en un renglón
    
    return reorganized_matrix

# Función para restringir los porcentajes de tejido Alpha, Beta y Gamma entre 0 y 1
def k_to_simplex(k1, k2):

    f1 = k2*np.sqrt(k1)
    f2 = (1 - k2)*np.sqrt(k1)
    f3 = 1 - np.sqrt(k1)

    return f1, f2, f3

def error_promedio(real, fit):
    n = len(fit)
    avg_errors = np.zeros(n)
    
    errors = np.zeros((n, 10))  # Array para almacenar todos los errores

    for i in range(n):
        errors[i, 0] = np.abs(real[i][0] - fit[i][0]) / real[i][0]  # alpha
        errors[i, 1] = np.abs(real[i][1] - fit[i][1]) / real[i][1]  # beta
        errors[i, 2] = np.abs(real[i][2] - fit[i][2]) / real[i][2]  # gamma
        errors[i, 3] = np.abs(real[i][3] - fit[i][3]) / real[i][3]  # t1_mye
        errors[i, 4] = np.abs(real[i][4] - fit[i][4]) / real[i][4]  # t2_mye
        errors[i, 5] = np.abs(real[i][5] - fit[i][5]) / real[i][5]  # t1_ie
        errors[i, 6] = np.abs(real[i][6] - fit[i][6]) / real[i][6]  # t2_ie
        errors[i, 7] = np.abs(real[i][7] - fit[i][7]) / real[i][7]  # t1_csf
        errors[i, 8] = np.abs(real[i][8] - fit[i][8]) / real[i][8]  # t2_csf
        errors[i, 9] = np.abs(real[i][9] - fit[i][9]) / real[i][9]  # flip
        
    avg_errors = np.mean(errors, axis=1)  # Promedio de cada fila
    avg_errors_columns = np.mean(errors[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]], axis=0)  # Promedio de columnas (promedio de cada parámetro)
    
        
    return avg_errors_columns, avg_errors, errors

# Función para generar o ajustar los datos EPG
def gen_epg_data(contributions_in, T1, T2, flip_angle, TR, TE, fit = False):
    
    TE_start = TE[0]        # Primer TE para generar los datos EPG.
    
    if fit == False:        # Bandera para verificar si se está utilizando la función para generar o ajustar.
        contributions = contributions_in
    else:                   # En caso de que se utilice para ajustar, la función tomará de entrada k1 y k2.
        k1 = contributions_in[0]
        k2 = contributions_in[1]
        f1, f2, f3 = k_to_simplex(k1, k2)
        contributions = [f1, f2, f3]
    
    tau = (TE[2] - TE[1])   # Separación de los valores de TE (En nuestro caso las mediciones son equi-espaciadas)
    Npc = 1                 # Número de datos generados
    nEchoes = len(TE)       # Número de mediciones en TE
    
    # Generamos las matrices para cada tejido
    myelin_epg_o = generate_epg_matrix(TR, Npc, T2[0], T1[0], nEchoes, tau, flip_angle, TE_start)
    IE_epg_o = generate_epg_matrix(TR, Npc, T2[1], T1[1], nEchoes, tau, flip_angle, TE_start)
    CSF_epg_o = generate_epg_matrix(TR, Npc, T2[2], T1[2], nEchoes, tau, flip_angle, TE_start)
    
    # Reorganizamos las matrices para acomodar TR por renglón y TE por columna
    myelin_epg = reorganize_design_matrices(myelin_epg_o)
    IE_epg = reorganize_design_matrices(IE_epg_o)
    CSF_epg = reorganize_design_matrices(CSF_epg_o)

    # Sumamos las señales individuales con su respectiva contribución
    EPG_signal = contributions[0]*myelin_epg + contributions[1]*IE_epg + contributions[2]*CSF_epg
    
    return np.array(EPG_signal)

# Función para realizar un ajuste de parámetros a los datos usando gen_epg_data
def fit_params_epg(data, TR, TE, initial_params, lower_bounds, upper_bounds):

    data_flat = data.ravel()             # Aplanamos los datos para pasarlos a curve_fit
    
    # Ajuste de curva usando gen_epg_data como función objetivo
    popt, pcov = curve_fit(lambda t, k1, k2, T1_1, T2_1, T1_2, T2_2, T1_3, T2_3, flip_angle: 
                    gen_epg_data([k1, k2], 
                                 [[T1_1], [T1_2], [T1_3]], 
                                 [[T2_1], [T2_2], [T2_3]], 
                                 flip_angle, TR, TE, fit = True).ravel(),
                    None, data_flat, p0=initial_params, maxfev=20000, bounds=(lower_bounds, upper_bounds))

    k1_fit, k2_fit, T1_1_fit, T2_1_fit, T1_2_fit, T2_2_fit, T1_3_fit, T2_3_fit, flip_angle_fit = popt
    
    f1, f2, f3 = k_to_simplex(k1_fit, k2_fit)   # Calculamos las contribuciones con la función que toma los k de entrada
    popt_out = [f1, f2, f3, T1_1_fit, T2_1_fit, T1_2_fit, T2_2_fit, T1_3_fit, T2_3_fit, flip_angle_fit] # Redefinimos los parámetros de salida cambiando los k por las contribuciones
    
    # Generar los datos ajustados usando los parámetros óptimos
    fitted_data = gen_epg_data([k1_fit, k2_fit], 
                               [[T1_1_fit], [T1_2_fit], [T1_3_fit]], 
                               [[T2_1_fit], [T2_2_fit], [T2_3_fit]], 
                               flip_angle_fit, TR, TE, fit = True)

    fitted_data_flat = fitted_data.ravel()

    # Cálculo del MSE
    mse = np.sum((data_flat - fitted_data_flat)**2) / len(data_flat)

    return popt_out, fitted_data, mse
