import numpy as np
from helper_functions import get_dimension, get_order

def de_casteljaus_method_evaluation(t,t0,alpha,control_points):
    t_t0 = t-t0
    tau = t_t0/alpha
    dimension = get_dimension(control_points)
    order = get_order(control_points)
    if dimension == 1:
        table = de_casteljaus_single_dimension(tau,order,control_points)
        result = table[0,order]
    else:
        table = de_casteljaus_multi_dimension(tau,order,control_points)
        result = table[0,order,:][:,None]
    return result

def de_casteljaus_single_dimension(tau,order,control_points):
    recursion_table = np.zeros((order+1, order+1))
    recursion_table[:,0][:,None] = control_points[:,None]
    # loop through columns
    for j in range(1,order+1):
        # loop through rows
        for i in range(0,order+1-j):
            value = recursion_table[i,j-1]*(1-tau) + recursion_table[i+1,j-1]*tau
            recursion_table[i,j] = value
    return recursion_table

def de_casteljaus_multi_dimension(tau,order,control_points):
    dimension = get_dimension(control_points)
    recursion_table = np.zeros((order+1, order+1,dimension))
    recursion_table[:,0,:] = control_points.T
    # loop through columns
    for j in range(1,order+1):
        # loop through rows
        for i in range(0,order+1-j):
            value = recursion_table[i,j-1,:]*(1-tau) + recursion_table[i+1,j-1,:]*tau
            recursion_table[i,j,:] = value.T
    return recursion_table

def de_casteljaus_derivative_evaluation(t,t0,alpha,control_points,derivative_order):
    t_t0 = t-t0
    tau = t_t0/alpha
    order = get_order(control_points)
    dimension = get_dimension(control_points)
    if dimension == 1:
        d_table = de_casteljaus_derivative_single_dimension(tau, order, control_points, derivative_order, alpha)
        result = d_table[0,order]
    else:
        d_table = de_casteljaus_derivative_multi_dimension(tau, order, control_points, derivative_order, alpha)
        result = d_table[0,order,:][:,None]
    return result

def de_casteljaus_derivative_single_dimension(tau, order, control_points, rth_derivative, scale_factor):
    table = de_casteljaus_single_dimension(tau,order,control_points)
    if rth_derivative == 0:
        return table
    d_table = np.zeros((order+1, order+1))
    for r in range(1, rth_derivative+1):
        # loop through columns
        for j in range(1,order+1):
        # loop through rows
            for i in range(0,order+1-j):
                value = d_table[i,j-1]*(1-tau) - r*table[i,j-1]/scale_factor + \
                    d_table[i+1,j-1]*tau + r*table[i+1,j-1]/scale_factor
                d_table[i,j] = value
        if r == rth_derivative:
            break 
        else:
            table = d_table
            d_table = np.zeros((order+1, order+1))
    return d_table

def de_casteljaus_derivative_multi_dimension(tau, order, control_points, rth_derivative, scale_factor):
    table = de_casteljaus_multi_dimension(tau,order,control_points)
    if rth_derivative == 0:
        return table
    dimension = get_dimension(control_points)
    d_table = np.zeros((order+1, order+1,dimension))
    for r in range(1, rth_derivative+1):
        # loop through columns
        for j in range(1,order+1):
        # loop through rows
            for i in range(0,order+1-j):
                values = d_table[i,j-1,:]*(1-tau) - r*table[i,j-1,:]/scale_factor + \
                    d_table[i+1,j-1,:]*tau + r*table[i+1,j-1,:]/scale_factor
                d_table[i,j] = values.T
        if r == rth_derivative:
            break
        else:
            table = d_table
            d_table = np.zeros((order+1, order+1,dimension))
    return d_table