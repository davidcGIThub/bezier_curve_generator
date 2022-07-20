"""
This module contains code that converts b-spline control points
to Bezier curve control points
"""
import numpy as np
from bsplinegenerator.helper_functions import count_number_of_control_points

def convert_to_bezier_control_points(bspline_control_points):
    number_of_control_points = count_number_of_control_points(bspline_control_points)
    order = number_of_control_points + 1
    conversion_matrix = get_bezier_to_bspline_conversion_matrix(order)
    bezier_control_points = np.transpose(np.dot(conversion_matrix, np.transpose(bspline_control_points)))
    return bezier_control_points

def get_bezier_to_bspline_conversion_matrix(order):

    conversion_matrix = np.array([])
    if order == 1:
        conversion_matrix = np.array([[1,0],
                                      [0,1]])
    elif order == 2:
        conversion_matrix = np.array([[2,-1,0],
                                      [0,1,0],
                                      [0,-1,2]])                         
    elif order == 3:
        conversion_matrix = np.array([[6,-7,2,0],
                                      [0,2,-1,0],
                                      [0,-1,2,0],
                                      [0,2,-7,6]])
    elif order == 4:
        conversion_matrix = np.array([[24, -46, 29, -6, 0],
                                      [0, 6, -7, 2, 0],
                                      [0, -2, 5, -2, 0],
                                      [0, 2, -7, 6, 0],
                                      [0, -6, 29, -46, 24]])
    elif order == 5:
        conversion_matrix = np.array([[120,-326,329,-146,24,0],
                                      [0,24,-46,29,-6,0],
                                      [0,-6,19,-16,4,0],
                                      [0,4,-16,19,-6,0],
                                      [0,-6,29,-46,24,0],
                                      [0,24,-146,329,-326,120]])
    else:
        raise Exception("Can only retrieve conversion matrix for curves of order 1-5")
    return conversion_matrix