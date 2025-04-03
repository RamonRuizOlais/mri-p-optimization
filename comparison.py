# -*- coding: utf-8 -*-

import error

def comparison(x1, TR1, x2, TR2, SNR, num_vox, seed_exp = 42, epsilon=0.002):
    error_1 = error.error(TR1, SNR, num_vox, seed_exp)
    error_2 = error.error(TR2, SNR, num_vox, seed_exp)
    d = abs(error_1 - error_2)

    if d > epsilon:
        # Si la diferencia de error es mayor que epsilon, elige el menor error
        return (x1, TR1, error_1) if error_1 < error_2 else (x2, TR2, error_2)
        
    # Si la diferencia de error es menor o igual a epsilon, elige el menor TR
    return (x1, TR1, error_1) if sum(TR1) < sum(TR2) else (x2, TR2, error_2)
