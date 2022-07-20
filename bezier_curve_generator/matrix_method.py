import numpy as np
from bezier_curve_generator.helper_functions import get_dimension, get_order

def matrix_method_evaluation(t,t0,alpha,control_points):
    order = get_order(control_points)
    T = get_T_vector(t,t0,alpha,order)
    M = get_M_matrix(order)
    return np.dot(control_points,np.dot(M,T))

def matrix_derivative_evaluation(t, t0, alpha, control_points, derivative_order):
    order = get_order(control_points)
    dT = get_T_derivative_vector(t, t0, derivative_order, alpha, order)
    M = get_M_matrix(order)
    return np.dot(control_points,np.dot(M,dT))
    
def get_M_matrix(order):
    M = np.array([])
    if order == 1:
        M = np.array([[-1 ,1],
                    [1  ,0]])
    elif order == 2:
        M = 0.5*np.array([[2 ,-4,2],
                        [-4,4 ,0],
                        [2 ,0 ,0]])
    elif order == 3:
        M = np.array([[-12 , 36  , -36 , 12],
                    [36  , -72 , 36  , 0],
                    [-36 , 36  , 0   , 0],
                    [12  , 0   , 0   , 0]])/12
    elif order == 4:
        M = np.array([[ 1  ,  -4 , 6   ,-4 , 1],
                    [ -4 ,  12 , -12 , 4 , 0],
                    [  6 , -12 ,  6  , 0 , 0],
                    [ -4 ,  4  , 0   , 0 , 0],
                    [1   ,   0 ,   0 , 0 , 0]])
    elif order == 5:
        M = np.array([[-1 , 5   , -10 , 10  , -5, 1],
                    [5  , -20 , 30  , -20 , 5 , 0],
                    [-10, 30  , -30 , 10  , 0 , 0],
                    [10 , -20 , 10  , 0   , 0 , 0],
                    [-5 , 5   , 0   , 0   , 0 , 0],
                    [1  , 0   , 0   , 0   , 0 , 0]])
    else:
        raise Exception("Matrix evaluation cannot be completed for a curve of order 6 or higher")
    return M

def get_T_vector(t,t0,alpha,order):
    T = np.array([])
    t_t0 = t-t0
    tau = t_t0/alpha
    if order == 1:
        T = np.array([[tau],[1]])
    elif order == 2:
        T = np.array([[tau**2],[tau],[1]])
    elif order == 3:
        T = np.array([[tau**3],[tau**2],[tau],[1]])
    elif order == 4:
        T = np.array([[tau**4],[tau**3],[tau**2],[tau],[1]])
    elif order == 5:
        T = np.array([[tau**5],[tau**4],[tau**3],[tau**2],[tau],[1]])
    else:
        raise Exception("Matrix evaluation cannot be completed for a curve of order 6 or higher")
    return T

def get_T_derivative_vector(t,t0,rth_derivative,scale_factor,order):
    T = np.ones((order+1,1))
    t_t0 = t-t0
    for i in range(order+1):
        if i > order-rth_derivative:
            T[i,0] = 0
        else:
            T[i,0] = (t_t0**(order-rth_derivative-i))/(scale_factor**(order-i)) * np.math.factorial(order-i)/np.math.factorial(order-i-rth_derivative)
    return T