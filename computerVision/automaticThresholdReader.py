# This program reads a .txt file of threshold numbers generated from automaticThresholdInitializer.py

# define average function (can be replaced later)
def average(allThresholds):
    lMin = []
    lMax = []
    aMin = []
    aMax = []
    bMin = []
    bMax = []
    for a,b,c,d,e in allThresholds:
        lMin.append(a)
        lMax.append(b)
        aMin.append(c)
        aMax.append(d)
        bMin.append(e)
        bMax.append(f)

    finalThresholdAvg = [lMin,lMax,aMin,aMax,bMin,bMax]
    for index in range(len(finalThresholdAvg)):
        finalThresholdAvg[index] = sum(finalThresholdAvg[index]) / len(finalThresholdAvg[index])

    return finalThresholdAvg



#read text file
allThresholds = []
file = open("thresholds.txt",'r')
for line in file:
    allThresholds += [int(x) for x in line.rstrip().split(",")]

#create averages
threshold = average(allThresholds)


# run colour tracker
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
