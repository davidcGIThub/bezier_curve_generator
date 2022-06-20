from time import time
import numpy as np
import matplotlib.pyplot as plt
from bezier_curves import BezierCurve
import time

dimension = 2
if dimension == 1:
    control_points = np.array([1, 3, 4, 2, 5,9])
elif dimension == 2:
    control_points = np.array([[1, 3, 4, 2, 5,9],[1,2,4,6,6.5,7]]) #2d
else:
    control_points = np.array([[1, 3, 4, 2, 5,9],[1,2,4,6,6.5,7],[0, 3, 4, 3, 6,9]]) #3d

t = 5
alpha = 3
derivative_order = 0
number_of_data_points = 1000
bcurve = BezierCurve(control_points,t,alpha)
start_time = time.time()
spline_data, time_data = bcurve.get_curve_data(1000)
derivative_data, time_data = bcurve.get_derivative_data(1000,derivative_order)
print("--- %s seconds ---" % (time.time() - start_time))

bcurve.plot_curve_data(number_of_data_points)
bcurve.plot_derivative_data(number_of_data_points, derivative_order)