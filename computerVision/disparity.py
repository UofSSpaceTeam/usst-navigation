import numpy as np
import cv2
from matplotlib import pyplot as plt
import time


def bm_stereo(imgL, imgR):
    '''coputes a disparity map'''
    stereo = cv2.StereoBM_create(numDisparities=32, blockSize=45)
    disparity = stereo.compute(imgL,imgR)
    return disparity

def sgbm_stereo(imgL, imgR):
    '''coputes a disparity map'''
    window_size = 3
    min_disp = 16
    num_disp = 112-min_disp
    # stereo = cv2.StereoSGBM_create(minDisparity = min_disp,
    #     numDisparities = num_disp,
    #     blockSize = 16,
    #     P1 = 8*3*window_size**2,
    #     P2 = 32*3*window_size**2,
    #     disp12MaxDiff = 1,
    #     uniquenessRatio = 10,
    #     speckleWindowSize = 100,
    #     speckleRange = 32
    # )
    stereo = cv2.StereoSGBM_create(
            numDisparities=16,
            blockSize = 4,
            P1 = 8*3*window_size**2,
            P2 = 32*3*window_size**2,
            # speckleWindowSize = 500,
            # speckleRange = 2
    )

    print('computing disparity...')
    disp = stereo.compute(imgL, imgR)#.astype(np.float32) / 16.0

    return disp

def threshold(img):
    '''Apply threshold to see the forground.'''
    threshold_min = 200
    th, img_thresh = cv2.threshold(img, threshold_min, 255, cv2.THRESH_TOZERO)
    return img_thresh


def bottom_half(disparity):
    '''Example of looking at a particular region of the image'''
    height, width = disparity.shape
    bot = disparity[height//2:height, 0:width]
    return bot


if __name__ == '__main__':
    # read in images
    imgL = cv2.imread('./tsukuba_left.jpg', 0)
    imgR = cv2.imread('./tsukuba_right.jpg', 0)

    # calculate disparity map
    # disp = sgbm_stereo(imgL, imgR)
    disp = bm_stereo(imgL, imgR)

    # Apply a threshold to cut out the back ground
    disp = threshold(disp)

    # focus on the bottom of the image
    disp = bottom_half(disp)

    # Show the image with matplotlib
    plt.imshow(disp,'gray')
    plt.show()
