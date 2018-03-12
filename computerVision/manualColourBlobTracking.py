# Single color RGB565 tracking using the OpenMV Cam.
# L or lightness is black and white
# A is cyan/magenta
# B is blue to yellow
import sensor, image, time

threshold_index = 0 # Do not change this value. 0 for red, 1 for green, 2 for blue.

# Initial values
#(30, 100, 15, 127, 15, 127)
#(30, 100, -64, -8, -32, 32)
#(0, 30, 0, 64, -128, 0)

# Color Tracking Thresholds -> (L Min, L Max, A Min, A Max, B Min, B Max)
# Lime Green = L:100, A:-128, B:128
# The below thresholds track in general red/green/blue things. You may wish to tune them...

thresholds =  [(40  , 88, -35, -10, 10, 70)]

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.YUV422) # 352x288. Deprecated, but higher-res, sensor. Zoomed image too.
#sensor.set_framesize(sensor.QVGA) # 320x240. Actively supported sensor but lower res
sensor.skip_frames(time = 50) # buffer after camera initilization. Don't remove completely.
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock() #create clock object


# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. "merge=True" merges all overlapping blobs in the image.

sensorRecord = []
while(True):
    last_rectangle = []
    clock.tick()
    img = sensor.snapshot()
    sensor.skip_frames(time = 200) # Delay between frames. Reduces clutter of output. Feel free to comment out this line or reduce the value.
    for blob in img.find_blobs([thresholds[threshold_index]], pixels_threshold= 175, margin = 5, merge=True):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        print("blob:",blob)
    print(clock.fps()) # print FPS
    print("\n")




################################ Delete nothing below this line ####################################

"""
0: 56
1: 86
2: -23
3: -3
4: 20
5: 58
"""
# we want: 0 -80 L
#--128 to -30
#+- 20 b

"""
thresholds =  [(20, 80, -128, 0, -30, 60), #OBSELETE VALUES
              (0, 100, -30, 100, 15, 16),
              (0, 60, 0, 64, -50, 60)
              ]
"""
""" Original Blob Tracking Example Below:

# Single Color RGB565 Blob Tracking Example
#
# This example shows off single color RGB565 tracking using the OpenMV Cam.

import sensor, image, time

threshold_index = 0 # 0 for red, 1 for green, 2 for blue

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# The below thresholds track in general red/green/blue things. You may wish to tune them...
thresholds = [(30, 100, 15, 127, 15, 127), # generic_red_thresholds
              (30, 100, -64, -8, -32, 32), # generic_green_thresholds
              (0, 30, 0, 64, -128, 0)] # generic_blue_thresholds

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. "merge=True" merges all overlapping blobs in the image.

while(True):
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs([thresholds[threshold_index]], pixels_threshold=200, area_threshold=200, merge=True):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
    print(clock.fps())
"""
