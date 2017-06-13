from math import sin, cos
import numpy as np

'''
Formulas taken from this paper:
http://www8.cs.umu.se/~thomash/reports/KinematicsEquationsForDifferentialDriveAndArticulatedSteeringUMINF-11.19.pdf
'''

def diff_drive_fk(x, y, l, theta, vl, vr, delta_t):
    """ Calculates forwark kinematics based on starting position,
        starting angle, width between wheels, velocity of wheels,
        and delta time.
        Returns: [x', y', theta']
    """
    if vr == vl:
        x_p = x + vr*cos(theta)*delta_t
        y_p = y + vr*sin(theta)*delta_t
        final = [x_p, y_p, theta]
    elif vr == -vl:
        omega = (vr-vl)/l
        theta_p = omega*delta_t + theta
        final = [x, y, theta_p]
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
        result = (np.matmul(a,b) + c).tolist()
        final = [result[0][0], result[1][0], result[2][0]]
    return final


print("---------------------------")
print("Demoing Forward kinematics:")
print("Starting point {}".format([0,0,np.pi/2]))

print("drive straigt {}".format(
    diff_drive_fk(0,0,4,np.pi/2, np.pi, np.pi, 1)))

print("pivot left on left wheel {}".format(
    diff_drive_fk(0,0,4,np.pi/2, 0, np.pi, 1)))

print("pivot right on right wheel {}".format(
    diff_drive_fk(0,0,4,np.pi/2, np.pi, 0, 1)))

print("Rotate right (clockwise) {}".format(
    diff_drive_fk(0,0,4,np.pi/2, np.pi, -np.pi, 1)))

print("Rotate left (counterclockwise) {}".format(
    diff_drive_fk(0,0,4,np.pi/2, -np.pi, np.pi, 1)))

print("Curve to the left {}".format(
    diff_drive_fk(0,0,4,np.pi/2, np.pi, 1.1*np.pi, 1)))

print("Curve to the right {}".format(
    diff_drive_fk(0,0,4,np.pi/2, 1.1*np.pi, np.pi, 1)))
print("--------------------------")
