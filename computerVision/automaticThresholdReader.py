# This program reads a .txt file of threshold numbers generated from automaticThresholdInitializer.py


#read text file
file = open("thresholds.txt",'r')
for line in file:
    line = line.rstrip().split(",")





print("Thresholds learned...")
print("Tracking colors...")

while(True):
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs([threshold], pixels_threshold=10, area_threshold=10, merge=True, margin=2):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        print("blob:",blob)
        sensor.skip_frames(time = 200) # Delay between frames. Reduces clutter of output. Feel free to comment out this line or reduce the value.
    print(clock.fps())
