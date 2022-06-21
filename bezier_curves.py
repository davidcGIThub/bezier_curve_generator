"""
This module contains code to evaluate bezier curves 
using the matrix method and the de casteljau algorithm for curves 
higher than the 5th degree. 
"""

import numpy as np 
import matplotlib.pyplot as plt
from helper_functions import get_dimension, get_order
from matrix_method import matrix_method_evaluation, matrix_derivative_evaluation
from de_casteljaus_method import de_casteljaus_method_evaluation, de_casteljaus_derivative_evaluation

class BezierCurve:
    """
    This class contains code to evaluate bezier curves 
    using the matrix method and the de casteljau algorithm for curves 
    higher than the 5th degree.
    """

    def __init__(self, control_points, start_time = 0, scale_factor = 1):
        '''
        Constructor for the Bezier Curve class, each column of
        control_points is a control point. Start time should be an integer.
        '''
        self._control_points = control_points
        self._scale_factor = scale_factor
        self._start_time = start_time
        self._end_time = start_time + scale_factor
        self._order = get_order(control_points)
        self._dimension = get_dimension(control_points)

    def get_curve_data(self,number_of_data_points):
        '''
        Returns equally distributed data points for the curve, as well
        as time data for the parameterization
        '''
        time_data = np.linspace(self._start_time, self._end_time, number_of_data_points)
        if self._dimension == 1:
            curve_data = np.zeros(number_of_data_points)
        else:
            curve_data = np.zeros((self._dimension,number_of_data_points))
        for i in range(number_of_data_points):
            t = time_data[i]
            if self._dimension == 1:
                curve_data[i] = self.evaluate_curve_at_time(t)
            else:
                curve_data[:,i][:,None] = self.evaluate_curve_at_time(t)
        return curve_data, time_data

    def evaluate_curve_at_time(self, t):
        value = 0
        if self._order >= 6:
            value = de_casteljaus_method_evaluation(t,self._start_time,self._scale_factor,self._control_points)
        else:
            value = matrix_method_evaluation(t,self._start_time,self._scale_factor,self._control_points)
        return value

    def evaluate_derivative_at_time(self, t, derivative_order):
        result = 0
        if self._order >= 6:
            result = de_casteljaus_derivative_evaluation(t, self._start_time, self._scale_factor, self._control_points,derivative_order)
        else:
            result = matrix_derivative_evaluation(t, self._start_time, self._scale_factor, self._control_points, derivative_order)
        return result

    def evaluate_curvature_at_time(self, time):
        dimension = get_dimension(self._control_points)
        if dimension == 1:
            derivative_vector = np.array([1 , self.evaluate_derivative_at_time(time,1)[0]])
            derivative_2nd_vector = np.array([0 , self.evaluate_derivative_at_time(time,2)[0]])
        else:
            derivative_vector = self.evaluate_derivative_at_time(time,1)
            derivative_2nd_vector = self.evaluate_derivative_at_time(time,2)
        curvature = np.linalg.norm(np.cross(derivative_vector.flatten(), derivative_2nd_vector.flatten())) / np.linalg.norm(derivative_vector)**3
        return curvature

    def get_derivative_data(self,number_of_data_points,derivative_order):
        time_data = np.linspace(self._start_time, self._end_time, number_of_data_points)
        if self._dimension == 1:
            derivative_data = np.zeros(number_of_data_points)
        else:
            derivative_data = np.zeros((self._dimension,number_of_data_points))
        for i in range(number_of_data_points):
            t = time_data[i]
            if self._dimension == 1:
                derivative_data[i] = self.evaluate_derivative_at_time(t,derivative_order)
            else:
                derivative_data[:,i][:,None] = self.evaluate_derivative_at_time(t,derivative_order)
        return derivative_data, time_data

    def get_curvature_data(self, number_of_data_points):
        time_data = np.linspace(self._start_time, self._end_time, number_of_data_points)
        curvature_data = np.zeros(number_of_data_points)
        for i in range(number_of_data_points):
            t = time_data[i]
            curvature_data[i] = self.evaluate_curvature_at_time(t)
        return curvature_data, time_data

    def plot_curve_data(self, number_of_data_points):
        curve_data, time_data = self.get_curve_data(number_of_data_points)
        if self._dimension == 1:
            control_point_times = np.linspace(self._start_time, self._end_time, self._order+1)
            plt.figure()
            plt.plot(time_data,curve_data, label="Bezier Curve")
            plt.scatter([time_data[0],time_data[-1]], [curve_data[0],curve_data[-1]])
            plt.plot(control_point_times, self._control_points)
            plt.scatter(control_point_times, self._control_points,label="Control Points")
            plt.xlabel("time")
            plt.ylabel("B(t)")
            plt.legend()
            plt.show()
        elif self._dimension == 2:
            plt.figure()
            plt.plot(curve_data[0,:],curve_data[1,:],label="Bezier Curve")
            plt.scatter([curve_data[0,0],curve_data[0,-1]],[curve_data[1,0],curve_data[1,-1]],label="Control Points")
            plt.scatter(self._control_points[0,:],self._control_points[1,:],label="Control Points")
            plt.plot(self._control_points[0,:],self._control_points[1,:])
            plt.xlabel("x")
            plt.ylabel("y")
            plt.legend()
            plt.show()
        elif self._dimension == 3:
            ax = plt.axes(projection='3d')
            ax.set_box_aspect(aspect =(1,1,1))
            ax.plot(curve_data[0,:], curve_data[1,:],curve_data[2,:],label="Bezier Curve")
            ax.scatter([curve_data[0,0],curve_data[0,-1]], [curve_data[1,0],curve_data[1,-1]], \
                [curve_data[2,0],curve_data[2,-1]])
            ax.plot(self._control_points[0,:], self._control_points[1,:],self._control_points[2,:])
            ax.scatter(self._control_points[0,:], self._control_points[1,:],self._control_points[2,:], \
                label="Control Points")
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            plt.legend()
            plt.show()

    def plot_derivative_data(self, number_of_data_points, derivative_order):
        figure_title = str(derivative_order) + " Order Derivative"
        plt.figure()
        derivative_data, time_data = self.get_derivative_data(number_of_data_points,derivative_order)
        for i in range(self._dimension):
            if self._dimension == 1:
                plt.plot(time_data,derivative_data[:], label="dimesion " + str(i))
            else:
                plt.plot(time_data,derivative_data[i,:], label="dimesion " + str(i))
        plt.xlabel("time")
        plt.ylabel("derivative")
        plt.legend()
        plt.title(figure_title)
        plt.show()

    def plot_curvature(self, number_of_data_points):
        curvature_data, time_data = self.get_curvature_data(number_of_data_points)
        plt.figure("Curvature")
        plt.plot(time_data, curvature_data)
        plt.xlabel('time')
        plt.ylabel('curvature')
        plt.title("Curvature")
        plt.show()