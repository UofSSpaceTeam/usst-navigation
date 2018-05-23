# Automatic RGB565 Color Tracking Example
#
# This example shows off single color automatic RGB565 color tracking using the OpenMV Cam.

# TODO: make the square in  the center bigger!!!

import sensor, image, time
print("Letting auto algorithms run. Don't put anything in front of the camera!")


### Sensor initialization ###
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.YUV422)
#sensor.set_framesize(sensor.QVGA) #Alternate sensor. Lower res, wider FOV
sensor.skip_frames(time = 50)
#sensor.set_special_effect(sensor.NEGATIVE)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
sensor.set_auto_exposure(False)
sensor.set_brightness(-3)
sensor.set_contrast(0)
sensor.set_saturation(3)
sensor.set_gainceiling(2)
clock = time.clock()

# Capture the color thresholds for whatever was in the center of the image.
#    Adjust 'size of box' to manage the x&y dimensions of the colour capture
sizeOfBox= (12,12)
r = [(320//2)-(50//2), (240//2)-(50//2), sizeOfBox[0], sizeOfBox[1]] # 50x50 center of QVGA.

#remove print statements after debugging
print("***Auto algorithms done*** \n\nHold the object you want to track in front of the camera in the box.")
print("MAKE SURE THE COLOR OF THE OBJECT YOU WANT TO TRACK IS FULLY ENCLOSED BY THE BOX!")


n = 2000 # miliseconds of wait time before camera starts recording thresholds
while clock.avg() < n: # wait time to set up ball in front of camera
    img = sensor.snapshot()
    img.draw_rectangle(r)


    #Write to file#
f = open('thresholds.txt','w') # Create file to write thresholds values into

print("Learning thresholds...") # Remove line after debugging
threshold = [50, 50, 0, 0, 0, 0] # Middle L, A, B values.
for i in range(100):
    img = sensor.snapshot()
    hist = img.get_histogram(roi = r)
    lo = hist.get_percentile(0.20) # Get the CDF of the histogram at the 1% range (ADJUST AS NECESSARY)!
    hi = hist.get_percentile(0.80) # Get the CDF of the histogram at the 99% range (ADJUST AS NECESSARY)!
    # Average in percentile values.
    threshold[0] = (threshold[0] + lo.l_value()) // 2
    threshold[1] = (threshold[1] + hi.l_value()) // 2
    threshold[2] = (threshold[2] + lo.a_value()) // 2
    threshold[3] = (threshold[3] + hi.a_value()) // 2
    threshold[4] = (threshold[4] + lo.b_value()) // 2
    threshold[5] = (threshold[5] + hi.b_value()) // 2
    # If you want to print out the result to console, uncomment line below
    print('0:',threshold[0],' |1:',threshold[1],' |2:',threshold[2],' |3:',threshold[3],' |4:',threshold[4],' |5:',threshold[5],sep='') #Remove after debugging
    f.write(','.join([str(x) for x in threshold] + ["\n"])) # Write detected values to file
    for blob in img.find_blobs([threshold], pixels_threshold=40, area_threshold=45, merge=True, margin=2):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        img.draw_rectangle(r)
    sensor.skip_frames(time = 1) # Delay between frames (ms). Reduces clutter of output. Feel free to comment out this line or reduce the value.

f.close()
print("Colour threshold initializaiton complete")



"""#Spare code
lo = hist.get_percentile(0.01) # Get the CDF of the histogram at the 1% range (ADJUST AS NECESSARY)!
hi = hist.get_percentile(0.99) # Get the CDF of the histogram at the 99% range (ADJUST AS NECESSARY)!

"""
