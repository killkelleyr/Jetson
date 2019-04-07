import time
from Adafruit_I2C import Adafruit_I2C
import Adafruit_PWM_Servo_Driver
import freenect
import cv2
import numpy as np

pwmPosL = 0
pwmPosR = 1

pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x40,busnum=1)
speed=2635
escBrake = 2550
timeDist=2.5

threshold = 100
current_depth = 600

#threshold = 50
#current_depth = 450

print("Initializing Motors")
pwm.setPWMFreq(500)
time.sleep(1)
pwm.setPWM(0,0,escBrake)
pwm.setPWM(1,0,escBrake)
time.sleep(2)

def show_depth():
	global threshold
	global current_depth
	
	depth,timestamp = freenect.sync_get_depth()
	depth = 255 * np.logical_and(depth >= current_depth - threshold, depth <= current_depth + threshold)
	depth = depth.astype(np.uint8)
	#cv2.imshow('Depth', depth)
	count = cv2.countNonZero(depth)
	print("White Pixels: ",count)

	if (count>8000):
		stop_Motors()
	else:
		move_Forward()

def move_Forward():
	#print("Driving Forward")
	pwm.setPWM(pwmPosL,0,speed)
	pwm.setPWM(pwmPosR,0,speed)
	
def initiate_Rev():
	pwm.setPWM(pwmPosL,0,2450)
	pwm.setPWM(pwmPosR,0,2450)
	time.sleep(0.05)
	stop_Motors()
	time.sleep(0.05)
	
def move_Reverse():
	#print("Driving Backwards")
	initiate_Rev()
	pwm.setPWM(pwmPosL,0,2470)
	pwm.setPWM(pwmPosR,0,2470)

def turn_Left():
	#print("Turning Left")
	initiate_Rev()
	pwm.setPWM(pwmPosL,0,2475)
	pwm.setPWM(pwmPosR,0,2665)

def turn_Right():
	initiate_Rev()
	pwm.setPWM(pwmPosR,0,2470)
	pwm.setPWM(pwmPosL,0,2685)
	
def stop_Motors():
	#print("Stopping Motors")
	pwm.setPWM(pwmPosL,0,minESC)
	pwm.setPWM(pwmPosR,0,minESC)

#cv2.namedWindow('Depth')

while 1:
	show_depth()
	if cv2.waitKey(10) == 27:
		pwm.setPWM(0,0,escBrake)
		pwm.setPWM(1,0,escBrake)
		break
