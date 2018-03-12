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
		''' Returns the distance to another GPSPositions on earth'''
		hav = lambda z: (1 - cos(z)) / 2   # haversine
		ahav = lambda z: 2 * asin(sqrt(z)) # inverse haversine

		d_lat = them.lat - self.lat
		d_lon = them.lon - self.lon

		z = (hav(d_lat)
				+ cos(self.lat) * cos(them.lat) * hav(d_lon))

		return GPSPosition.RADIUS * ahav(z)

	def bearing(self, them):
		''' Returns the bearing to another GPSPositions on earth'''
		d_lat = them.lat - self.lat
		d_lon = them.lon - self.lon

		y = sin(d_lon) * cos(them.lat)
		x = (cos(self.lat) * sin(them.lat)
				- sin(self.lat) * cos(them.lat) * cos(d_lat))

		return atan2(y, x)