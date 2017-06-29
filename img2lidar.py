from PIL import Image
import matplotlib.pyplot as plt
import random
import math
import numpy as np
from lidar_sim import LidarMap
import lidar_sim

WHITE = (255,255,255)
BLACK = (0,0,0)

def bresenhamLine(x0, y0, x1, y1):
    ''' Draw line from p0 to p1.
        Taken from: https://www.codeproject.com/Articles/15604/Ray-casting-in-a-2D-tile-based-environment
    '''
    result = []
    steep = abs(y1-y0) > abs(x1-x0)
    if steep:
        #swap
        x0, y0 = y0, x0
        x1, y1 = y1, x1
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    d_x = x1-x0
    d_y = abs(y1-y0)
    error = 0
    y = y0
    if y0 < y1:
        ystep = 1
    else:
        ystep = -1
    for x in range(x0, x1+1):
        if steep:
            result.append((y,x))
        else:
            result.append((x,y))
        error += d_y
        if 2*error >= d_x:
            y += ystep
            error -= d_x
    return result


def rayCast(position, angle, length, pixmap, max_x, max_y):
    ''' Casts a ray of :length: at :angle: from :position: and
        returns the point where it collides with terrain.
    '''
    ray = bresenhamLine(position[0], position[1],
            position[0]+int(length*math.cos(angle)),
            position[1]+int(length*math.sin(angle)))
    if ray[0] != position:
        ray.reverse()
    for i,p in enumerate(ray):
        if 0 < p[0] < max_x and 0 < p[1] < max_y:
            if pixmap[p[0],p[1]] == BLACK:
                return p
    return None


def unzip_points(l):
    ''' takes a list of couples [(x0,y0),(x1,y1)...]
        and returns two lists: one containing all the
        x values, and the other containing all the y values.
    '''
    return list(zip(*l))[0], list(zip(*l))[1],


def main():
    im = Image.open('map_test.png')
    width = im.size[0]
    height = im.size[1]
    pixels = im.load()
    # load pixels in as 2d list, not used yet
    # data = []
    # for y in range(0, height):
    #     data.append([pix[x,y] for x in range(0,width)])

    waypoints = []

    target_pos = (random.randrange(0,width), random.randrange(0,height))
    rover_pos = (random.randrange(0,width), random.randrange(0,height))
    while pixels[target_pos[0], target_pos[1]] == BLACK:
        target_pos = (random.randrange(0,width), random.randrange(0,height))
    while pixels[rover_pos[0], rover_pos[1]] == BLACK:
        rover_pos = (random.randrange(0,width), random.randrange(0,height))
    waypoints.append(rover_pos)
    waypoints.append(target_pos)

    distances = []
    angles = []
    for a in np.linspace(0,2*math.pi, 200):
        p = rayCast(rover_pos, a, 300, pixels, width-1, height-1)
        if p is not None:
            d = math.sqrt((rover_pos[0]-p[0])**2 + (rover_pos[1]-p[1])**2)
            distances.append(d)
            angles.append(a)
    m = LidarMap(angles, distances)
    cart_map = lidar_sim.map_to_cartesian(m, rover_pos)


    implot = plt.imshow(im)
    plt.plot(target_pos[0], target_pos[1], 'ro',
             rover_pos[0], rover_pos[1], 'co',
             *unzip_points(waypoints),
             *unzip_points(cart_map), 'r.'
             )
    plt.show()

if __name__ == '__main__':
    main()
