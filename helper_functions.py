import numpy as np

def get_dimension(control_points):
    if control_points.ndim == 1:
        dimension = 1
    else:
        dimension = len(control_points)
    return dimension

def get_order(control_points):
    if control_points.ndim == 1:
        order = len(control_points) -1 
    else:
        order = np.shape(control_points)[1] - 1
    return order

def get_num_control_points(control_points):
    if control_points.ndim == 1:
        num_control_points = len(control_points)
    else:
        num_control_points = np.shape(control_points)[1]
    return num_control_points