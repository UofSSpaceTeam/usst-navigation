import vrep
import sys
import time

from robocluster import Device


vrep.simxFinish(-1) # just in case, close all opened connections
clientID = vrep.simxStart('127.0.0.1',19997,True,True,5000,5) # Connect to V-REP

if clientID == -1:
    print("Could not connect to API server")
    sys.exit(1)
else:
    print("Connected with clientID {}".format(clientID))


err, GPS = vrep.simxGetObjectHandle(clientID, "GPS",
                                        vrep.simx_opmode_oneshot_wait)

err, Barnstormer = vrep.simxGetObjectHandle(clientID, "Barnstormer",
                                        vrep.simx_opmode_oneshot_wait)

wheel_names = ['wheelLB', 'wheelLF', 'wheelRB', 'wheelRF']
wheels = {}
for name in wheel_names:
    err, wheels[name] = vrep.simxGetObjectHandle(clientID, name,
                                            vrep.simx_opmode_oneshot_wait)

def turn_wheel(wheel, speed):
    if wheel in wheel_names:
        err = vrep.simxSetJointTargetVelocity(clientID, wheels[wheel], speed, vrep.simx_opmode_oneshot)


def stop():
    for wheel in wheel_names:
        turn_wheel(wheel, 0)

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

vrepdevice = Device('vrepdevice', 'rover')
example_device = Device('example', 'rover')

@vrepdevice.on('*/wheel*')
def rpm(event, data):
    e = event.split('/')
    # print(e[1])
    turn_wheel(e[1], data)

@vrepdevice.every('100ms')
async def get_gps():
    rover_pos = read_gps()
    await vrepdevice.publish('GPSPos', rover_pos)

@vrepdevice.every('100ms')
async def get_Accel():
    await vrepdevice.publish('Accel', read_accel())

# @example_device.every('100ms')
async def pub():
    await example_device.publish('wheelRB', -0.5)
    await example_device.publish('wheelRF', -0.5)
    await example_device.publish('wheelLB', 0.5)
    await example_device.publish('wheelLF', 0.5)

# @example_device.on('*/joystick2')
async def translate(event, data):
    await example_device.publish('wheelRB', 4*data[1])
    await example_device.publish('wheelRF', 4*data[1])

# @example_device.on('*/joystick1')
async def translate(event, data):
    await example_device.publish('wheelLB', -4*data[1])
    await example_device.publish('wheelLF', -4*data[1])

def main():
    stop()
    vrepdevice.start()
    example_device.start()
    vrepdevice.wait()
    example_device.wait()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        stop()
        vrepdevice.stop()
        example_device.stop()
        vrep.simxFinish(-1)
        sys.exit(0)
