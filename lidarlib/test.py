from lidarmap import gen_map, center, max_range,PathFinding
from lidarimage import rand_open_point, plot_with_image, gen_map_from_image,\
        plot_result
from PIL import Image
import random
import math


def test_lidarmap():
    ''' Path finding algorithm.'''
    target = (random.randrange(0,360),
                    random.randrange(max_range/2,max_range))
    m = gen_map()
    waypoints = [(0,0)]

    # First check if we can see the position
    if target[1] < m.distance(m.angle_snap(target[0])):
        waypoints.append(target)
        # target within view exit early
        plot_result(m, waypoints, target)
    else:
        opening = m.find_opening(target[0])
        if opening is not None:
            waypoints.append(opening)
            plot_result(m, waypoints, target)
        else:
            # Assume we are in a corner or cave, and try
            # to get away from the obsticals
            deep_angle = center(*m.find_farthest_region())
            waypoints.append((deep_angle, max_range))
            plot_result(m, waypoints, target)

def test_lidarimage():
    im = Image.open('map_test.png')

    waypoints = []
    target_pos = rand_open_point(im)
    rover_pos = rand_open_point(im)
    waypoints.append(rover_pos)
    waypoints.append(target_pos)
    m = gen_map_from_image(im, rover_pos)
    plot_with_image(m, im, rover_pos, target_pos, waypoints)

<<<<<<< HEAD
def test_image_pathing():
    im = Image.open('map_test.png')

    waypoints = []
    target_pos = rand_open_point(im)
    rover_pos = rand_open_point(im)
    waypoints.append(rover_pos)
    # waypoints.append(target_pos)
    m = gen_map_from_image(im, rover_pos)
    print(m.partitions)
    angle_to_target = math.atan2((target_pos[1]-rover_pos[1]),(target_pos[0]-rover_pos[0]))
    if angle_to_target < 0:
        angle_to_target += 360
    print(angle_to_target)
    distance = math.sqrt((target_pos[0]-rover_pos[0])**2 + (target_pos[1]-rover_pos[1])**2)

    # First check if we can see the position
    if distance < m.distance(math.degrees(angle_to_target)):
        waypoints.append(target_pos)
        # target_pos within view exit early
        print("no obstructions")
        print(waypoints)
        plot_with_image(m, im, rover_pos, target_pos, waypoints)
    else:
        opening = m.find_opening(math.degrees(angle_to_target))
        if opening is not None:
            waypoints.append(opening)
            print("Found opening {}", opening)
            print(waypoints)
            plot_with_image(m, im, rover_pos, target_pos, waypoints)
        else:
            # Assume we are in a corner or cave, and try
            # to get away from the obsticals
            deep_angle = center(*m.find_farthest_region())
            waypoints.append((deep_angle, max_range))
            # plot_result(m, waypoints, target_pos)
            print("In corner, farthest distance at {}", deep_angle)
            print(waypoints)
            plot_with_image(m, im, rover_pos, target_pos, waypoints)


=======
def test_associateGPS():
    target_pos = GPSPosition(50+random.randrange(1,1000)/1000, -111+random.randrange(1,1000)/1000)
    rover_pos = GPSPosition(50+random.randrange(1,1000)/1000, -111+random.randrange(1,1000)/1000)
    heading = random.randrange(0,360)
    #target_pos = GPSPosition(51,-112)
    #rover_pos = GPSPosition(51.0001,-112)
    
    angle = math.degrees(rover_pos.bearing(target_pos)) - heading
    if angle < 0:
        angle = angle + 360
    distance = rover_pos.distance(target_pos)
    if distance > max_range:
        distance = max_range
    m = gen_map()
    lidar_target = (m.angle_snap(angle), distance)
    
    waypoints = PathFinding(lidar_target, m)
    plot_result(m, waypoints, lidar_target)
>>>>>>> master

if __name__ == '__main__':
    # test_lidarmap()
    # test_lidarimage()
<<<<<<< HEAD
    test_image_pathing()

=======
    #test_associateGPS()
>>>>>>> master
