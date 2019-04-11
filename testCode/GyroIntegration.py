import time
from Adafruit_I2C import Adafruit_I2C
import Adafruit_PWM_Servo_Driver
import freenect
import cv2
import numpy as np
import math
import RTIMU
from multiprocessing import Process, Manager, Value
import os.path
import sys, getopt
sys.path.append('.')

SETTINGS_FILE = "RTIMULib"
print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

#IMU variables
s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)
poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)

#IMU Settings
imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

#Variables for ESC
pwmPosL = 0
pwmPosR = 1
pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x40,busnum=1)
speed=2635
escBrake = 2550

#Variables for kinect


# Multiprocessing variables
manager = Manager()
robotAngle = manager.Value('i', 0)
whiteSpace = manager.Value('i', 0)
leftESC = manager.Value('i',2550)
rightESC = manager.Value('i',2550)

def show_depth():
	threshold =90
	current_depth = 600
	
	depth,timestamp = freenect.sync_get_depth()
	depth = 255 * np.logical_and(depth >= current_depth - threshold, depth <= current_depth + threshold)
	depth = depth.astype(np.uint8)
	#cv2.imshow('Depth', depth)
	count = cv2.countNonZero(depth)
	whiteSpace.value = count
	print("White Pixels: ",count)

		
def get_gyro():
	while True:
		if imu.IMURead():
		# x, y, z = imu.getFusionData()
		# print("%f %f %f" % (x,y,z))
			data = imu.getIMUData()
			(data["pressureValid"], data["pressure"], data["pressureTemperatureValid"], data["pressureTemperature"]) = pressure.pressureRead()
			(data["humidityValid"], data["humidity"], data["humidityTemperatureValid"], data["humidityTemperature"]) = humidity.humidityRead()
			fusionPose = data["fusionPose"]
		print("Robot Angle: %f" % (math.degrees(math.degrees(fusionPose[2]))))
		time.sleep(poll_interval*1.0/1000.0)

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
	pwm.setPWM(pwmPosR,0,2475)
	pwm.setPWM(pwmPosL,0,2665)
	#time.sleep(0.25)
	
def stop_Motors():
	#print("Stopping Motors")
	pwm.setPWM(pwmPosL,0,escBrake)
	pwm.setPWM(pwmPosR,0,escBrake)
	
def initialize_Motors():
	print("Initializing Motors")
	pwm.setPWMFreq(500)
	time.sleep(1)
	pwm.setPWM(0,0,escBrake)
	pwm.setPWM(1,0,escBrake)
	time.sleep(2)

def keep_straight():
	if robotAngle.value < -5:
		turn_Right()
	elif robotAngle.value > 5:
		turn_Left()
	else:
		move_Forward()

def drive():
	while True:
		print("Whitness",whiteSpace.value)
		if (whiteSpace.value > 26500):
			print("Too close stopping")
			stop_Motors()
		else:
			print("Keeping Straight")
			#keep_straight()
		if sys.stdin.read(1) == 32:
			print("Stopping")
		
	

p1 = Process(target=drive)
p1.start()
p2 = Process(target=show_depth)
p2.start()

p1.join()
p2.join()