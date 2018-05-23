# This program reads a .txt file of threshold numbers generated from automaticThresholdInitializer.py

# TODO: check initializer and make sure we get enough data to get good thresholds.
# TODO: add in historical data too in Initializer or Reader to also manage environment/situ


import sensor, image, time, ujson, pyb

USB = pyb.USB_VCP()
USB.setinterrupt(-1)

LED = pyb.LED(1)

def Publish(d):
pkt = ujson.dumps(d)
USB.write(bytes([len(pkt)]))
USB.write(pkt.encode())

def HandleInput():
if USB.any():
    LED.toggle()
    b = USB.read(1)
    # if b == b'0x02' or b == b'0x03':
    USB.read(6)
    d = {"name":"OpenMV"}
    Publish(d)
    LED.toggle()

if __name__ == "__main__":

######## Sensor setup ########
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.YUV422)
#sensor.set_framesize(sensor.QVGA) #Alternate sensor. Lower res, wider FOV
sensor.skip_frames(time = 50)
#sensor.set_special_effect(sensor.NEGATIVE)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
sensor.set_auto_exposure(False)
sensor.set_brightness(0)# -3
sensor.set_contrast(0)
sensor.set_saturation(0)# 3
sensor.set_gainceiling(2)
clock = time.clock()

#print("\nResolution is: " + str(sensor.width()) + "x"+ str(sensor.height()))


####### Functions ########
def averageThreshold(allThresholds):

    '''
    This function takes in a list of LAB min/max values (generated from the thresholds .txt file)
    and it returns a list of an average of all those respective entries according to index
    Preconditions: allThresholds: one list of sets of 6 values. must satisfy: len(param)%6==0
    return: List of length 6 - Format: (L MIN, LMAX, A MIN, A MAX, B MIN, B MAX)
    '''
    a=[]
    b=[]
    c=[]
    d=[]
    e=[]
    f=[]
    counter = 0
    while counter < len(allThresholds):
        a.append(allThresholds[counter])
        b.append(allThresholds[counter + 1])
        c.append(allThresholds[counter + 2])
        d.append(allThresholds[counter + 3])
        e.append(allThresholds[counter + 4])
        f.append(allThresholds[counter + 5])
        counter += 6
    final = []
    all = [a,b,c,d,e,f]
    for item in all:
        final.append(int( sum(item) / len(item) ))
    return final

def averageCoord(listA):
    """"""
    return sum(listA)/len(listA)


########### Threshold determination ###########

#read text file
allThreshold = []
#file = open("thresholds.txt",'r')
#for line in file:
    #line = line.rstrip().rstrip(",").split(",")
    #allThreshold += [int(x) for x in line]
#file.close()

##create averages from file readings
#fileThreshold = averageThreshold(allThreshold)

#print("fileThresholds are:",fileThreshold)

#mixedThreshold = []
fileThreshold = [33, 35, 5, 10, 40, 42]
thresholdIdeal1 = (65, 88, -10, 20, 22, 49) # Ideal in sunlight on gray background. Filter on.
thresholdIdeal2 = (32, 53, -10, 8, 32, 49 )# Ideal in sunlight ,back of school, dark gray cement background. Filter on.
thresholdIdeal3 = fileThreshold.copy()

mixed = fileThreshold.copy()
#print('Static thresholds used:', thresholdIdeal3)
mixed.extend(thresholdIdeal3)

threshold = averageThreshold(mixed)
#print("Final thresholds used:",threshold)

######## Data #########
# 0.5 m=~ 2150px // 1 m=~340 px // 2m=~110px // 3 m=~49 px
# 4m =~ 30 5m =~ ??TBD??

dataToConsole = {"sensorWidth":sensor.width(),
                 "sensorHeight":sensor.height(),
                 }

xCoords = []
yCoords = []
sizes = []
blobSizeThreshold = [2150,340,110, 49, 30]
######### Main detection #########
while True:
    HandleInput()
    for PX in blobSizeThreshold:
        #print("Check px size:",PX)
        clock.tick()
        img = sensor.snapshot()
        for blob in img.find_blobs([threshold], pixels_threshold = PX, area_threshold = PX//2, merge=True, margin = PX//12):
            img.draw_rectangle(blob.rect())
            img.draw_cross(blob.cx(), blob.cy())
            #print("blob:",blob)
            xCoords.append(blob[5])
            yCoords.append(blob[6])
            sizes.append(blob[4])


    #while (True): #This is a test loop. remove when done testing.
        #clock.tick()
        #img = sensor.snapshot()
        #blobs = []
        #for blob in img.find_blobs([threshold], pixels_threshold= 10, area_threshold = 10, merge=True, margin = 3):
            ##blobs.append(blob)
            #if blob[4] > 100:
                #pass
            #else:
                #img.draw_rectangle(blob.rect())
                #img.draw_cross(blob.cx(), blob.cy())
                #print(blob)
                #sensor.skip_frames(time = 200)
                ##print("X:",blob[0])
                ##print("y:",blob[1])
                ##print('4:',blob[4])
            #xCoords.append(blob[0])
            #yCoords.append(blob[1])
            #print(clock.fps())
        #sensor.skip_frames(time = 10) # Delay between frames. Reduces clutter of output. Feel free to comment out this entire line or reduce the value.


    if len(xCoords)== 0:
        dataToConsole["x"] = -1
        dataToConsole["y"] = -1
        dataToConsole["size"] = -1

    else:
        dataToConsole["x"] = averageCoord(xCoords)
        dataToConsole["y"] = averageCoord(yCoords)
        dataToConsole["size"] = averageCoord(sizes)

    Publish(dataToConsole)



    """ ######### spare code below / not meant for implementation ##############
    for blob in img.find_blobs([threshold], pixels_threshold=50, area_threshold=50, merge=True, margin=10):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        img.draw_rectangle(r)

    """
