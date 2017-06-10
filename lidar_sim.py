from matplotlib import pyplot as plt
import numpy as np
import random

max_range = 1000
N = 15
max_variance = 15
distances = [max_range]*360

# add up to N objects (at leas 1)
for i in range(0,random.randrange(1,N)):
    a = random.randrange(0,360)
    b = random.randrange(0,360)
    start = min(a,b)
    end = max(a,b)

    # Object is located aproximately here
    obj_dist = random.randrange(max_variance,max_range)

    # how much to vary the object surface by
    roughness = random.randrange(1,max_variance)

    # Add object while varying the surface
    for j in range(start,end):
        distances[j] = obj_dist+random.randrange(-roughness,roughness)
print(distances)

target_angle = random.randrange(0,360)
target_distance = random.randrange(100,max_range)


waypoints = [(0,0)]
ledges = []
for x in range(0,359):
    # Find edges
    a = distances[x]
    b = distances[x+1]
    if(abs(b-a) > 2*max_variance):
        ledges.append(x)
    if x == target_angle and target_distance < distances[x]:
        waypoints.append((target_angle, target_distance))

falling_edge = []
rising_edge = []
for l in ledges:
    if distances[l] < distances[l+1]:
        falling_edge.append(l)
    else:
        rising_edge.append(l)
print("Rising: {}".format(rising_edge))
print("Falling: {}".format(falling_edge))
# in falling_edge, l is the closer point
# in rising_edge, l is the farther point

# Find region that farthest away from us.
# The idea is that this will move us out
# of a 'corner' and into open space so we
# eventually can just point to the target
max_dist_start = 0
deep_angle_start = 0
for a in falling_edge:
    if distances[a+1] > max_dist_start:
        max_dist_start = distances[a+1]
        deep_angle_start = a

max_dist_end = 0
deep_angle_end = 0
for a in rising_edge:
    if distances[a] >= max_dist_end:
        max_dist_end = distances[a]
        deep_angle_end = a
print("Deepest segment is from {}-{}".format(deep_angle_start, deep_angle_end))

# calculate the angle we should drive in
# to reach the farthest point (hopefully more open space)
if deep_angle_start > deep_angle_end:
    deep_angle = (deep_angle_end+360+deep_angle_start)//2
    if deep_angle >= 360:
        deep_angle -= 360
else:
    deep_angle = (deep_angle_end+deep_angle_start)//2

if len(waypoints) == 1:
    waypoints.append((deep_angle, max_dist_start))

angles = np.linspace(0,np.pi*2, 360)
way_angles = [angles[a] for a in list(zip(*waypoints))[0]]
way_dists = list(zip(*waypoints))[1]

plt.polar(angles, distances, # terrain
          way_angles, way_dists,'g', #path
          angles[target_angle], target_distance, 'bo')
plt.show()
