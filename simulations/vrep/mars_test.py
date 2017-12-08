import vrep
import sys
import time




vrep.simxFinish(-1) # just in case, close all opened connections
clientID = vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to V-REP

if clientID == -1:
    print("Could not connect to API server")
    sys.exit(1)
else:
    print("Connected with clientID {}".format(clientID))


# Get object handles
err, wheelLB = vrep.simxGetObjectHandle(clientID, "wheelLB", #wheelLB looks in object list in vrep
                                        vrep.simx_opmode_oneshot_wait)
err, wheelLF = vrep.simxGetObjectHandle(clientID, "wheelLF",
                                        vrep.simx_opmode_oneshot_wait)
err, wheelRB = vrep.simxGetObjectHandle(clientID, "wheelRB",
                                        vrep.simx_opmode_oneshot_wait)
err, wheelRF = vrep.simxGetObjectHandle(clientID, "wheelRF",
                                        vrep.simx_opmode_oneshot_wait)
err, GPS = vrep.simxGetObjectHandle(clientID, "GPS",
                                        vrep.simx_opmode_oneshot_wait)

err, Barnstormer = vrep.simxGetObjectHandle(clientID, "Barnstormer",
                                        vrep.simx_opmode_oneshot_wait)


def drive_forward(speed):
    err = vrep.simxSetJointTargetVelocity(clientID, wheelLB, speed, vrep.simx_opmode_oneshot)
    err = vrep.simxSetJointTargetVelocity(clientID, wheelLF, speed, vrep.simx_opmode_oneshot)
    # for some reason right wheels are backward, not sure how to fix in vrep
    err = vrep.simxSetJointTargetVelocity(clientID, wheelRB, -speed, vrep.simx_opmode_oneshot)
    err = vrep.simxSetJointTargetVelocity(clientID, wheelRF, -speed, vrep.simx_opmode_oneshot)

def stop():
    err = vrep.simxSetJointTargetVelocity(clientID, wheelLB, 0, vrep.simx_opmode_oneshot_wait)
    err = vrep.simxSetJointTargetVelocity(clientID, wheelLF, 0, vrep.simx_opmode_oneshot_wait)
    err = vrep.simxSetJointTargetVelocity(clientID, wheelRB, 0, vrep.simx_opmode_oneshot_wait)
    err = vrep.simxSetJointTargetVelocity(clientID, wheelRF, 0, vrep.simx_opmode_oneshot_wait)

def read_gps():
    err, x = vrep.simxGetFloatSignal(clientID, 'GPS/x', vrep.simx_opmode_oneshot_wait)
    err, y = vrep.simxGetFloatSignal(clientID, 'GPS/y', vrep.simx_opmode_oneshot_wait)
    err, z = vrep.simxGetFloatSignal(clientID, 'GPS/z', vrep.simx_opmode_oneshot_wait)
    return [x, y, z]

def read_accel():
    err, x = vrep.simxGetFloatSignal(clientID, 'Accelerometer/x', vrep.simx_opmode_oneshot_wait)
    err, y = vrep.simxGetFloatSignal(clientID, 'Accelerometer/y', vrep.simx_opmode_oneshot_wait)
    err, z = vrep.simxGetFloatSignal(clientID, 'Accelerometer/z', vrep.simx_opmode_oneshot_wait)
    return [x, y, z]

def read_gyro():
    err, x = vrep.simxGetFloatSignal(clientID, 'Gyro/x', vrep.simx_opmode_oneshot_wait)
    err, y = vrep.simxGetFloatSignal(clientID, 'Gyro/y', vrep.simx_opmode_oneshot_wait)
    err, z = vrep.simxGetFloatSignal(clientID, 'Gyro/z', vrep.simx_opmode_oneshot_wait)
    return [x, y, z]

def set_rover_position(x, y, z):
    err =vrep.simxSetObjectPosition(clientID, Barnstormer, -1, (x,y, z), vrep.simx_opmode_oneshot)

def main():
    set_rover_position(0,0,0.25)
    while True:
        drive_forward(0.1)
        print("GPS: ", read_gps())
        print("Accel: ", read_accel())
        print("Gyro: ", read_gyro())

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        stop()
        vrep.simxFinish(-1)
        sys.exit(0)
