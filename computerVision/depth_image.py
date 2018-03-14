

import pyzed.camera as zcam
import pyzed.defines as sl
import pyzed.types as tp
import pyzed.core as core
import math
import numpy as np
import sys
import cv2

def main():
    # Create a PyZEDCamera object
    zed = zcam.PyZEDCamera()

    # Create a PyInitParameters object and set configuration parameters
    init_params = zcam.PyInitParameters()
    init_params.depth_mode = sl.PyDEPTH_MODE.PyDEPTH_MODE_PERFORMANCE  # Use PERFORMANCE depth mode
    init_params.coordinate_units = sl.PyUNIT.PyUNIT_MILLIMETER  # Use milliliter units (for depth measurements)

    # Open the camera
    err = zed.open(init_params)
    if err != tp.PyERROR_CODE.PySUCCESS:
        exit(1)

    # Create and set PyRuntimeParameters after opening the camera
    runtime_parameters = zcam.PyRuntimeParameters()
    runtime_parameters.sensing_mode = sl.PySENSING_MODE.PySENSING_MODE_STANDARD  # Use STANDARD sensing mode

    # Capture 50 images and depth, then stop
    i = 0
    image = core.PyMat()
    depth = core.PyMat()
    point_cloud = core.PyMat()
    depth_display = core.PyMat()

    while i < 500:
        # A new image is available if grab() returns PySUCCESS
        if zed.grab(runtime_parameters) == tp.PyERROR_CODE.PySUCCESS:
            # Retrieve left image
            zed.retrieve_image(image, sl.PyVIEW.PyVIEW_LEFT)
	    #retrieve depth image
            zed.retrieve_image(depth_display, sl.PyVIEW.PyVIEW_DEPTH)
            # Retrieve depth map. Depth is aligned on the left image
            zed.retrieve_measure(depth, sl.PyMEASURE.PyMEASURE_DEPTH)
            # Retrieve colored point cloud. Point cloud is aligned on the left image.
            zed.retrieve_measure(point_cloud, sl.PyMEASURE.PyMEASURE_XYZRGBA)
            points = point_cloud.get_data()
            #get the distance in mm
            distances = np.sqrt(points[:,:,0]*points[:,:,0]+points[:,:,1]*points[:,:,1]+points[:,:,2]*points[:,:,2])
            #find the closest point
            min_index = np.unravel_index(np.nanargmin(distances),distances.shape)
            print("closest object at ({0},{1},{2})mm".format(points[min_index[0],min_index[1],0],points[min_index[0],min_index[1],1],points[min_index[0],min_index[1],2]))
            cv2.imshow("depth map", depth_display.get_data()) 
            key = cv2.waitKey(5)
              
            i = i + 1
            
            sys.stdout.flush()

    # Close the camera
    zed.close()

if __name__ == "__main__":
    main()
