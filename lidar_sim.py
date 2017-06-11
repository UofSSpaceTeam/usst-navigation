from matplotlib import pyplot as plt
import numpy as np
import random

max_range = 1000
N = 15 # number of objects to add
max_variance = 15

def gen_map():
    ''' Generates a list of distances for 360 degrees.
        'Objects' are placed at random positions, and
        have rough surfaces to simulate rocky terrain
    '''
    distances = [max_range]*360
    # add up to N objects (at least 1)
    for i in range(0,random.randrange(1,N)):
        a = random.randrange(0,360)
        b = random.randrange(0,360)
        start = min(a,b)
        end = max(a,b)

        # Object is located approximately here
        obj_dist = random.randrange(max_variance,max_range)

        # how much to vary the object surface by
        roughness = random.randrange(1,max_variance)

        # Add object while varying the surface
        for j in range(start,end):
            distances[j] = obj_dist+random.randrange(-roughness,roughness)
    return distances

def find_edges(distances):
    ''' Finds points in the map that undergo a
        sharp change in distance, indicating the possibility
        of object boundries.
    '''
    edges = []
    for x in range(0,359):
        # Find edges
        a = distances[x]
        b = distances[x+1]
        if(abs(b-a) > 2*max_variance):
            edges.append(x)
    return edges

def rise_fall_edges(edges, distances):
    ''' Divides edges into rising and falling edges.
        in falling_edge, l is the closer point
        in rising_edge, l is the farther point '''

    falling_edge = []
    rising_edge = []
    for e in edges:
        if distances[e] < distances[e+1]:
            falling_edge.append(e)
        else:
            rising_edge.append(e)
    return rising_edge, falling_edge

def find_farthest_region(distances, rising_edge, falling_edge):
    """Find region that farthest away from us.
        The idea is that this will move us out
        of a 'corner' and into open space so we
        eventually can just point to the target """

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
    # print("Deepest segment is from {}-{}".format(deep_angle_start, deep_angle_end))
    return deep_angle_start, deep_angle_end

def farthest_region_angle(deep_angle_start, deep_angle_end):
    """ Find the center of the farthest region"""
    if deep_angle_start > deep_angle_end:
        deep_angle = (deep_angle_end+360+deep_angle_start)//2
        if deep_angle >= 360:
            deep_angle -= 360
    else:
        deep_angle = (deep_angle_end+deep_angle_start)//2
    return deep_angle



def plot_result(distances, waypoints, target):
    """ Plot the map and waypoints with matplotlib"""
    angles = np.linspace(0,np.pi*2, 360)
    way_angles = [angles[a] for a in list(zip(*waypoints))[0]]
    way_dists = list(zip(*waypoints))[1]

    plt.polar(angles, distances, # terrain
              way_angles, way_dists,'g', #path
              angles[target[0]], target[1], 'bo')
    plt.show()

def main():
    target = (random.randrange(0,360),
                    random.randrange(max_range/2,max_range))
    distances = gen_map()
    waypoints = [(0,0)]

    # First check if we can see the position
    for x in range(0,360):
        if x == target[0] and target[1] < distances[x]:
            waypoints.append(target)
            # target within view exit early
            plot_result(distances, waypoints, target)
            return

    # Find a way out of the obstacles
    rising_edge, falling_edge = rise_fall_edges(
            find_edges(distances), distances)
    deep_angle = farthest_region_angle(
            *find_farthest_region(distances, rising_edge, falling_edge))
    waypoints.append((deep_angle, max_range))

    plot_result(distances, waypoints, target)

if __name__ == '__main__':
    main()
