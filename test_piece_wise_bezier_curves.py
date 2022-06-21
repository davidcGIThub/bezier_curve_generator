from time import time
import numpy as np
import matplotlib.pyplot as plt
from piecewise_bezier_curve import PiecewiseBezierCurve
import time

# dimension = 1
# if dimension == 1:
#     control_points = np.array([1, 3, 4, 2, 5,9])
# elif dimension == 2:
#     control_points = np.array([[1, 3, 4, 2, 5,9],[1,2,4,6,6.5,7]]) #2d
# else:
#     control_points = np.array([[1, 3, 4, 2, 5,9],[1,2,4,6,6.5,7],[0, 3, 4, 3, 6,9]]) #3d

control_points = np.array([[1, 3, 4, 2, 5,9,7],[1,2,4,6,6.5,7,6]]) #2d

t = 5
alpha = 6
order = 2
number_of_data_points = 100
p_bcurve = PiecewiseBezierCurve(control_points,order,t,alpha)
spline_data, time_data = p_bcurve.get_curve_data(number_of_data_points)


p_bcurve.plot_curve_data(number_of_data_points)