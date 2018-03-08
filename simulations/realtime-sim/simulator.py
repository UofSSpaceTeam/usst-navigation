import math
import random

from robocluster import Device
from GPSPosition import GPSPosition
from differential_drive import diff_drive_fk

class Rover:

    def __init__(self):
        self.position = GPSPosition(52.132653, -106.628012)
        self.heading = 0
        self.wheelspeed = [0, 0]
        self.wheel_radius = 0.5
        self.wheel_axis = 1


    def update(self, dt):
        next_pose = diff_drive_fk(0, 0,
                self.wheel_axis,
                -math.radians(self.heading)+math.pi/2,
                self.wheelspeed[0],
                self.wheelspeed[1],
                dt)
        bearing = -math.degrees(math.atan2(next_pose[1], next_pose[0]) - math.pi/2)
        print(bearing)
        distance = math.sqrt(next_pose[0]**2 + next_pose[1]**2)
        n_gps = self.position.gpsPosition(bearing, distance)
        self.position = n_gps
        self.heading = -math.degrees(next_pose[2] - math.pi/2)

def simulate_piksi(gpsPosition):
    stddev_lat = 1.663596084712623e-05
    stddev_lon = 2.1743680968892167e-05
    return [random.gauss(gpsPosition.lat, stddev_lat),
            random.gauss(gpsPosition.lon, stddev_lon)]

simDevice = Device('simDevice', 'rover')

# Rover parameters
simDevice.storage.rover = Rover()
simDevice.storage.rover.wheelspeed = [0, 0]
simDevice.storage.rover.heading = 0

DELTA_T = 0.2
@simDevice.every(DELTA_T)
async def update():
    simDevice.storage.rover.update(DELTA_T)
    print('position', simDevice.storage.rover.position)
    print('wheel speed', simDevice.storage.rover.wheelspeed)
    print('heading', simDevice.storage.rover.heading)

@simDevice.every(DELTA_T)
async def publish_state():
    position = simDevice.storage.rover.position
    noisy_pos = simulate_piksi(position)
    print(noisy_pos)
    await simDevice.publish("GPSPosition", noisy_pos)

@simDevice.on('*/wheelLF')
def update_wheel_l(event, data):
    simDevice.storage.rover.wheelspeed[0] = data

@simDevice.on('*/wheelRF')
def update_wheel_l(event, data):
    simDevice.storage.rover.wheelspeed[1] = data



simDevice.run()
