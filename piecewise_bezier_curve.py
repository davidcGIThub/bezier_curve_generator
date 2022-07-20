from logging import raiseExceptions
import numpy as np 
import matplotlib.pyplot as plt
from bezier_curves import BezierCurve
from helper_functions import get_dimension


class PiecewiseBezierCurve:

    def __init__(self, control_points, order, start_time = 0, scale_factor = 1):
        '''
        Constructor for the Bezier Curve class, each column of
        control_points is a control point. Start time should be an integer.
        '''
        self._control_points = control_points
        self._scale_factor = scale_factor
        self._start_time = start_time
        if self.check_valid_order(order, control_points):
            self._order = order
        else:
            raise Exception("Order is invalid for the number of control points")
        self._num_curves = self.get_num_curves(control_points, order)
        self._end_time = start_time + scale_factor*self._num_curves
        self._dimension = get_dimension(control_points)
        self._curve_list = self.create_curve_list(control_points, order, start_time, scale_factor)

    def get_curve_data(self,number_of_data_points):
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

    def get_curvature_data(self,number_of_data_points):
        time_data = np.linspace(self._start_time, self._end_time, number_of_data_points)
        curvature_data = np.zeros(number_of_data_points)
        for i in range(number_of_data_points):
            t = time_data[i]
            curvature_data[i] = self.evaluate_curvature_at_time(t)
        return curvature_data, time_data

    def get_num_control_points(self, control_points):
        if control_points.ndim == 1:
            num_control_points = len(control_points)
        else:
            num_control_points = np.shape(control_points)[1]
        return num_control_points

    def get_num_curves(self, control_points, order):
        num_control_points = self.get_num_control_points(control_points)
        num_curves = (num_control_points-1)/order
        return int(num_curves)

    def check_valid_order(self, order, control_points):
        num_control_points = self.get_num_control_points(control_points)
        if (num_control_points-1)%order == 0:
            return True
        else:
            return False

    def create_curve_list(self, control_points, order, start_time, scale_factor):
        curve_list = []
        curve_start_time = start_time
        for i in range(self._num_curves):
            curve_control_points = control_points[:,i*order:(i+1)*order+1]
            bezier_curve = BezierCurve(curve_control_points,curve_start_time,scale_factor)
            curve_list.append(bezier_curve)
            curve_start_time += scale_factor
        return curve_list

    def evaluate_curve_at_time(self,t):
        curve_number = int((t - self._start_time)/self._scale_factor)
        if t == self._end_time:
            curve_number -= 1 
        result = self._curve_list[curve_number].evaluate_curve_at_time(t)
        return result

    def evaluate_derivative_at_time(self,t,derivative_order):
        curve_number = int((t - self._start_time)/self._scale_factor)
        if t == self._end_time:
            curve_number -= 1 
        result = self._curve_list[curve_number].evaluate_derivative_at_time(t,derivative_order)
        return result

    def evaluate_curvature_at_time(self,t):
        curve_number = int((t - self._start_time)/self._scale_factor)
        if t == self._end_time:
            curve_number -= 1 
        result = self._curve_list[curve_number].evaluate_curvature_at_time(t)
        return result

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