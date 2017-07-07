from lidarmap import gen_map, center, max_range
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



if __name__ == '__main__':
    # test_lidarmap()
    # test_lidarimage()
    test_image_pathing()

