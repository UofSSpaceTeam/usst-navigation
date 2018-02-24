import numpy as np
import cv2
import time
from matplotlib import pyplot as plt


left = cv2.VideoCapture(1)
right = cv2.VideoCapture(2)

while(True):
    # Capture frame-by-frame, this is a dumb
    # way to do it, get a stereo camera ;)
    ret, l_frame = right.read()
    cv2.imshow('left',l_frame)
    print("GO->")
    time.sleep(1)
    ret, r_frame = right.read()

    # Our operations on the frame come here
    l_gray = cv2.cvtColor(l_frame,cv2.COLOR_BGR2GRAY)
    r_gray = cv2.cvtColor(r_frame,cv2.COLOR_BGR2GRAY)
    stereo = cv2.StereoBM_create(numDisparities=32, blockSize=45)
    disparity = stereo.compute(l_gray, r_gray)

    # Display the resulting frame
    cv2.imshow('right',r_frame)
    # cv2.imshow('disp',disparity)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    plt.imshow(disparity,'gray')
    plt.show()

# When everything done, release the capture
left.release()
right.release()
cv2.destroyAllWindows()

