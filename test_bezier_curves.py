from time import time
import numpy as np
import matplotlib.pyplot as plt
from bezier_curves import BezierCurve
import time

# dimension = 1
# if dimension == 1:
#     control_points = np.array([1, 3, 4, 2, 5,9])
# elif dimension == 2:
#     control_points = np.array([[1, 3, 4, 2, 5,9],[1,2,4,6,6.5,7]]) #2d
# else:
#     control_points = np.array([[1, 3, 4, 2, 5,9],[1,2,4,6,6.5,7],[0, 3, 4, 3, 6,9]]) #3d

control_points = np.array([[0,0.5,2],[0,.2,0]])
p0 = np.array([control_points[0,0], control_points[1,0]])
p1 = np.array([control_points[0,1], control_points[1,1]])
p2 = np.array([control_points[0,2], control_points[1,2]])

t = 5
alpha = 6
derivative_order = 1
number_of_data_points = 1000
bcurve = BezierCurve(control_points,t,alpha)
start_time = time.time()
spline_data, time_data = bcurve.get_curve_data(1000)
derivative_data, time_data = bcurve.get_derivative_data(1000,derivative_order)
print("--- %s seconds ---" % (time.time() - start_time))

def get_c_max(p0,p1,p2):
    m = (p0+p2)/2
    leg_start = p1-p0
    leg_middle = p1-m
    leg_end = p1-p2
    A = np.linalg.norm(np.cross(leg_start,leg_end))/2
    if np.dot(leg_start,leg_middle) <= 0:
        c_max = A/np.linalg.norm(leg_start)**3
    elif np.dot(leg_middle,leg_end) <= 0:
        c_max = A/np.linalg.norm(leg_end)**3
    else:
        c_max = np.linalg.norm(leg_middle)**3 / A**2
    return c_max


c_max = get_c_max(p0,p1,p2)
print("c_max: " , c_max)

bcurve.plot_curve_data(number_of_data_points)
# bcurve.plot_derivative_data(number_of_data_points, derivative_order)
bcurve.plot_curvature(number_of_data_points)