import numpy as np
from bezier_curve_generator.helper_functions import get_order

def bernstein_method_evaluation(t, control_points):
    summation = 0
    order = get_order(control_points)
    for i in range(order+1):
        B_i = control_points[i]
        eta_i_t = basis_function_evaluation(t,i,order)
        summation += B_i*eta_i_t
    return summation

def basis_function_evaluation(t, i, order):
    binomial = binomial_theorem(order, i)
    result = binomial *(t**i) * (1-t)**(order-i)
    return result

def binomial_theorem(coefficient_1, coefficient_2):
    numerator = np.math.factorial(coefficient_1)
    denominator =  np.math.factorial(coefficient_2) * np.math.factorial(coefficient_1 \
        - coefficient_2)
    result = numerator / denominator
    return result