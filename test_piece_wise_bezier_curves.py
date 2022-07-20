import numpy as np
import matplotlib.pyplot as plt
from bezier_curve_generator.piecewise_bezier_curve import PiecewiseBezierCurve

control_points = np.array([[1, 3, 4, 2, 5,9,7],[1,2,3,6,6.5,7,6]]) #2d

t = 5
alpha = 6
order = 2
derivative_order = 1
number_of_data_points = 100
p_bcurve = PiecewiseBezierCurve(control_points,order,t,alpha)
spline_data, time_data = p_bcurve.get_curve_data(number_of_data_points)

p_bcurve.plot_curve_data(number_of_data_points)
p_bcurve.plot_derivative_data(number_of_data_points, 0)
p_bcurve.plot_curvature(number_of_data_points)