import cv2
import numpy as np
from matplotlib import pyplot as plt

#distance in inches
def computeDistance(radius, focal):
	return focal / radius

#segmentation based on color
def segmentation(img, lowerBound, upperBound, kernel):
	blurred = cv2.GaussianBlur(img, (11, 11), 0)
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, lowerBound, upperBound)
	mask = cv2.erode(mask, kernel, iterations=2)
	mask = cv2.dilate(mask, kernel, iterations=2)
	mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
	mask = cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
	return mask

	
#find the contour that is most likely to be a tennis ball
#currently returns the biggest contour
#TO DO: add more filter to improve the accuracy
def findBall(mask):
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
	
	if len(cnts) > 0:
		
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		return (x,y,radius,center)
	return None


def drawBall(img,x,y,radius,center):
	cv2.circle(img, (int(x), int(y)), int(radius),
		(0, 255, 255), 2)
	cv2.circle(img, center, 5, (0, 0, 255), -1)
	return img


	
#test current ball detection algorithm
def ballDetectionFromPictures(greenLower,greenUpper,kernel):
	#img=cv2.imread('desert4.jpg')
	for i in range(0,20):
		img = cv2.imread('left_'+str(i)+'.png')
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		mask = segmentation(img,greenLower,greenUpper,kernel)
		ball = findBall(mask)
		if ball is not None:
			img = drawBall(img,ball[0],ball[1],ball[2],ball[3])
		plt.figure(0)
		plt.imshow(hsv,cmap = 'gray')
		plt.title('hsv'), plt.xticks([]), plt.yticks([])
		plt.figure(1)
		plt.subplot(121),plt.imshow(img,cmap = 'gray')
		plt.title('detection'), plt.xticks([]), plt.yticks([])
		#plt.figure(2)
		plt.subplot(122),plt.imshow(mask,cmap = 'gray')
		plt.title('segmentation'), plt.xticks([]), plt.yticks([])
		plt.show()

def ballDetectionFromCamera(greenLower, greenUpper, kernel, camNum, focal):
	cam = cv2.VideoCapture(camNum)
	
	while True:
		ret, frame = cam.read()
		mask = segmentation(frame, greenLower, greenUpper, kernel)
		ball = findBall(mask)
		if ball is not None:
			frame = drawBall(frame, ball[0],ball[1],ball[2],ball[3])
			dist = computeDistance(ball[2],focal)
			cv2.putText(frame,str(dist),ball[3],cv2.FONT_HERSHEY_SIMPLEX,0.5,255)
		
		cv2.imshow('frame',frame)
	
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	

def main():	
	greenLower = (27, 55, 100)
	greenUpper = (45, 150, 255)
	kernel = np.ones((5,5),np.uint8)
	focal = 24*122*0.39
	#ballDetectionFromPictures(greenLower,greenUpper,kernel)
	ballDetectionFromCamera(greenLower,greenUpper,kernel, 1, focal)
	

if __name__ == "__main__":
	main()	
	