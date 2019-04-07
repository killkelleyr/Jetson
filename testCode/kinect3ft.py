import freenect
import cv2
import numpy as np

threshold = 100
current_depth = 600


def show_depth():
	global threshold
	global current_depth
	
	depth,timestamp = freenect.sync_get_depth()
	depth = 255 * np.logical_and(depth >= current_depth - threshold, depth <= current_depth + threshold)
	depth = depth.astype(np.uint8)
	cv2.imshow('Depth', depth)
	count = cv2.countNonZero(depth)
	if (count>100000):
		print("Too Close Stop Motors")
	else:
		print("No objects in path continue on")
	#187721
cv2.namedWindow('Depth')

while 1:
	show_depth()
	if cv2.waitKey(10) == 27:
		break
