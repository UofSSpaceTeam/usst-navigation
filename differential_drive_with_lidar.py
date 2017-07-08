from matplotlib import pyplot as plt
import numpy as np
import random
import math
from lidarlib.lidarmap import gen_map, center, max_range
from lidarlib.lidarimage import rand_open_point, plot_with_image, gen_map_from_image,\
        plot_result
from differential_drive import *

max_range = 600 # What is considered "infinity"
N = 15 # number of objects to add
max_variance = 15 # How rough can surface of terrain be
width = 1.5

def polarToCartesian(r,theta):
    x = r * cos(theta)
    y = r * sin(theta)
    return x, y

def CartesianToPolar(x,y):
    r = sqrt(x*x+y*y)
    if x == 0:
        if y > 0:
            theta = pi / 2
        else:
            theta = 3 * pi / 2
    else:
        theta = atan(y/x)
    if x < 0:
        theta = theta + pi
    return r, theta

def inverse_kinematics(x_dst, y_dst, l = 1, speed = 10, x = 0, y = 0, theta = 0):
	
	ratio,reverse = inverse_kinematics_drive(x,y,x_dst,y_dst,theta,l)
	if reverse:
		speed = -1
	trace_x = []
	trace_y = []
	x_tmp = x
	y_tmp = y
	theta_tmp = theta
	for i in range(100):
		[x_tmp,y_tmp,theta_tmp] = diff_drive_fk(x_tmp,y_tmp, l,theta_tmp, speed, ratio * speed, 1)
		trace_x.append(x_tmp)
		trace_y.append(y_tmp)
	return trace_x, trace_y  

def main():
    target = (random.randrange(0,360),
                    random.randrange(max_range/2,max_range))

    m = gen_map()
    waypoints = [(0,0)]

    # First check if we can see the position
    if target[1] < m.distance(m.angle_snap(target[0])):
        x, y = polarToCartesian(target[1],math.radians(target[0]))
        trace_x, trace_y = inverse_kinematics(x, y)
        trace = []
        for i in range(len(trace_x)):
            r, theta = CartesianToPolar(trace_x[i],trace_y[i])
            trace.append((math.degrees(theta),r)) 
        # target within view exit early
        plot_result(m, trace, target)
    else:
        opening = m.find_opening(target[0])
        if opening is not None:
            waypoints.append(opening)
            plot_result(m, waypoints, target)
        else:
            # Assume we are in a corner or cave, and try
            # to get away from the obsticals
            deep_angle = center(*m.find_farthest_region())
            waypoints.append((deep_angle, max_range))
            plot_result(m, waypoints, target)

if __name__ == '__main__':
    main()