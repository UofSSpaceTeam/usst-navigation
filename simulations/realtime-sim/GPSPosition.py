import math
from math import *

class GPSPosition:
    # Earth's radius in metres
    RADIUS = 6371008.8

    def __init__(self, lat, lon, mode=0):
        # lat an lon are assumed to be in radians
        self.lat = lat
        self.lon = lon
        self.mode = mode # 0=SPP, 1=Float RTK, 2=Fixed RTK

    def distance(self, them):
        ''' Returns the distance to another GPSPositions on earth in meters'''
        hav = lambda z: (1 - cos(z)) / 2   # haversine
        ahav = lambda z: 2 * asin(sqrt(z)) # inverse haversine

        d_lat = them.lat - self.lat
        d_lon = them.lon - self.lon

        z = (hav(d_lat) + cos(self.lat) * cos(them.lat) * hav(d_lon))

        return GPSPosition.RADIUS * ahav(z)

    def bearing(self, them):
        ''' Returns the bearing to another GPSPositions on earth in degrees'''
        d_lat = them.lat - self.lat
        d_lon = them.lon - self.lon

        y = sin(d_lon) * cos(them.lat)
        x = (cos(self.lat) * sin(them.lat)
                        - sin(self.lat) * cos(them.lat) * cos(d_lat))

        return math.degrees(atan2(y, x))

    def gpsPosition(self, bearing, distance):
        '''Returns a new GPSPosition relative to this one
            Args:
                bearing: The bearing to the next point in degrees
                distance: The distance to the next point in meters
        '''
        r_lat = math.radians(self.lat)
        r_lon = math.radians(self.lon)
        target_lat = asin(sin(r_lat)*cos(distance/GPSPosition.RADIUS) +cos(r_lat)*sin(distance/GPSPosition.RADIUS)*cos(math.radians(bearing)))

        target_lon = r_lon + atan2(sin(math.radians(bearing))*sin(distance/GPSPosition.RADIUS)*cos(r_lat),cos(distance/GPSPosition.RADIUS)-sin(r_lat)*sin(target_lat))
        return GPSPosition(math.degrees(target_lat), math.degrees(target_lon))

    def __str__(self):
        return 'GPSPosition({}, {})'.format(self.lat, self.lon)

