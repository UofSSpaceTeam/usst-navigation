from math import sin, cos
import numpy as np

'''
Formulas taken from this paper:
http://www8.cs.umu.se/~thomash/reports/KinematicsEquationsForDifferentialDriveAndArticulatedSteeringUMINF-11.19.pdf
'''

def diff_drive_fk(x, y, l, theta, vl, vr, delta_t):
    """ resulting matrix is:
        |  x'  |
        |  y'  |
        |theta'|
    """
    if vr == vl:
        R = 0
    else:
        R = l/2*(vl + vr)/(vr-vl)
    omega = (vr-vl)/l
    theta = omega*delta_t + theta
    ICC = (x-R*sin(theta), y+R*cos(theta))
    a = np.matrix([[cos(omega*delta_t), -sin(omega*delta_t), 0],
        [sin(omega*delta_t), cos(omega*delta_t), 0],
        [0, 0, 1]])
    b = np.matrix([[x-ICC[0]], [y-ICC[1]], [theta]])
    c = np.matrix([[ICC[0]], [ICC[1]], [omega*delta_t]])
    final = np.matmul(a,b) + c
    return final

print(diff_drive_fk(0,0,4,np.pi/2, np.pi, np.pi+0.0001, 1))

