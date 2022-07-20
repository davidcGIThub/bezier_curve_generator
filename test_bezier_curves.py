from time import time
import numpy as np
import matplotlib.pyplot as plt
from bezier_curves import BezierCurve
import time
import random

order = 4
control_points = np.random.randint(10, size=(2,order+1)) # random
print("control_points: " , control_points)

t = 5
alpha = 0.1
derivative_order = 1
number_of_data_points = 5000
bcurve = BezierCurve(control_points,t,alpha)
start_time = time.time()
spline_data, time_data = bcurve.get_curve_data(1000)
derivative_data, time_data = bcurve.get_derivative_data(1000,derivative_order)

bcurve.plot_curve_data(number_of_data_points)
bcurve.plot_derivative_data(number_of_data_points,1)
bcurve.plot_derivative_magnitude_data(number_of_data_points, 2)
bcurve.plot_curvature(number_of_data_points)



