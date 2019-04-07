import time
from Adafruit_I2C import Adafruit_I2C
import Adafruit_PWM_Servo_Driver
import freenect
import cv2
import numpy as np

pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x40,busnum=1)
speed=2615
escBreak = 2550
timeDist=2.5

threshold = 100
current_depth = 600

def show_depth():
	global threshold
	global current_depth
	
	depth,timestamp = freenect.sync_get_depth()
	depth = 255 * np.logical_and(depth >= current_depth - threshold, depth <= current_depth + threshold)
	depth = depth.astype(np.uint8)
	#cv2.imshow('Depth', depth)
	count = cv2.countNonZero(depth)

	if (count>100000):
		print("Too Close Stop Motors")
		pwm.setPWM(0,0,escBreak)
		pwm.setPWM(1,0,escBreak)
	else:
		print("No objects in path continue on")
		pwm.setPWM(0,0,speed)
		pwm.setPWM(1,0,speed)

#cv2.namedWindow('Depth')

while 1:
	show_depth()
	if cv2.waitKey(10) == 27:
		pwm.setPWM(0,0,escBreak)
		pwm.setPWM(1,0,escBreak)
		break

'''
pwm.setPWMFreq(500)
time.sleep(1)
pwm.setPWM(0,0,2550)
pwm.setPWM(1,0,2550)
print("Motors Initializing")
time.sleep(2)
print("Moving forward for "+str(timeDist)+" secs")
pwm.setPWM(0,0,speed)
pwm.setPWM(1,0,speed)
time.sleep(timeDist)
print("Stopping Motors")
pwm.setPWM(0,0,2550)
pwm.setPWM(1,0,2550)
'''
