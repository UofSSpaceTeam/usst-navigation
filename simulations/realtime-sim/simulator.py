import math
import random
import time

from robocluster import Device
from GPSPosition import GPSPosition
from differential_drive import diff_drive_fk

class Rover:

    def __init__(self):
        self.position = GPSPosition(52.132653, -106.628012)
        self.prev_pos = self.position
        self.heading = 0 # degress, north = 0
        self.wheelspeed = [0, 0]
        self.prev_wheelspeed = self.wheelspeed
        self.wheel_radius = 0.26 # meters
        self.wheel_axis = 1
        self.velocity = [0,0]
        self.acceleration = [0,0]


    def update(self, dt):
        delta_wheelspeed = [self.wheelspeed[0]-self.prev_wheelspeed[0],
                            self.wheelspeed[1]-self.prev_wheelspeed[1]]
        next_pose = diff_drive_fk(0, 0,
                self.wheel_axis,
                -math.radians(self.heading)+math.pi/2,
                self.wheelspeed[0],
                self.wheelspeed[1],
                dt)
        bearing = -math.degrees(math.atan2(next_pose[1], next_pose[0]) - math.pi/2)
        distance = math.sqrt(next_pose[0]**2 + next_pose[1]**2)
        n_gps = self.position.gpsPosition(bearing, distance)
        n_velocity = [next_pose[0]*dt, next_pose[1]*dt]
        self.acceleration = [n_velocity[0]-self.velocity[0],
                             n_velocity[1]-self.velocity[1]]

        self.position = n_gps
        self.heading = -math.degrees(next_pose[2] - math.pi/2)

        self.prev_wheelspeed = self.wheelspeed
        self.velocity = n_velocity


def simulate_piksi(gpsPosition):
    stddev_lat = 1.663596084712623e-05
    stddev_lon = 2.1743680968892167e-05
    return [random.gauss(gpsPosition.lat, stddev_lat),
            random.gauss(gpsPosition.lon, stddev_lon)]

def simulate_bno(accel):
    stddev_x = 0.025842126805189967
    stddev_y = 0.03368775942186025
    stddev_z = 0.038244224565556637
    return [random.gauss(accel[0], stddev_x),
            random.gauss(accel[1], stddev_y)]

simDevice = Device('simDevice', 'rover')

# Rover parameters
simDevice.storage.rover = Rover()
simDevice.storage.rover.wheelspeed = [0, 0]
simDevice.storage.rover.heading = 0

DELTA_T = 0.1
@simDevice.every(DELTA_T)
async def update():
    simDevice.storage.rover.update(DELTA_T)
    # simDevice.storage.rover.wheelspeed = [x+0.1 for x in simDevice.storage.rover.wheelspeed]
    print('position', simDevice.storage.rover.position)
    print('wheel speed', simDevice.storage.rover.wheelspeed)
    print('heading', simDevice.storage.rover.heading)
    print('accleration', simDevice.storage.rover.acceleration)

@simDevice.every(DELTA_T)
async def publish_state():
    position = simDevice.storage.rover.position
    pos_list = [position.lat, position.lon]
    noisy_pos = simulate_piksi(position)
    print(noisy_pos)
    await simDevice.publish("singlePointGPS", noisy_pos)
    accel = simDevice.storage.rover.acceleration
    accel = simulate_bno(accel)
    # print(accel)
    await simDevice.publish("Acceleration", accel)

@simDevice.on('*/FilteredGPS')
async def check_accuracy(event, data):
    pres = 1
    dif_lat = abs(data[0] - simDevice.storage.rover.position.lat)
    dif_long = abs(data[1] - simDevice.storage.rover.position.lon)
    if dif_lat < pres:
        print('Accurate Lat : ', dif_lat)
    if dif_long < pres:
        print('Accurate Long : ', dif_long)
    else:
        print('North dif: ', dif_lat, 'East dif: ', dif_long)


@simDevice.on('*/wheelLF')
def update_wheel_l(event, data):
    simDevice.storage.rover.wheelspeed[0] = data

@simDevice.on('*/wheelRF')
def update_wheel_l(event, data):
    simDevice.storage.rover.wheelspeed[1] = data



simDevice.run()
