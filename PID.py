import os
import Tkinter as tkinter
import time
from PIL import Image
from PIL import ImageTk
from Adafruit_I2C import Adafruit_I2C
import Adafruit_PWM_Servo_Driver
import serial
from multiprocessing import Process, Manager, Value
import math

pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x40, busnum=0)

pwmPosL = 1

minESC = 320
pwm.setPWMFreq(60)

time.sleep(1)
pwm.setPWM(pwmPosL, 0, minESC)
time.sleep(2)
#pwm.setPWM(pwmPosL,0,328)


maxESC = 350
setRPM = 90

manager = Manager()
valLeft = manager.Value('i', 0)
rpmLeft = manager.Value('i', 0)

P = 3.3
I = 0.1
D = 0.0005

integral = 0
previous_error= 0

ser = None


def serial_connect():
	global ser
	try:
		ser = serial.Serial('/dev/ttyACM0', baudrate = 115200)
		if ser.isOpen():
			print("open: " + ser.portstr)
			ser.write(b'S')
			connect = True
				
		else:
			print("connection failed")	
	except:
		print("ttyACM0 not found")


def read_encoder():
	serial_connect()
	print("Read Encoder")
	while True:
		X = ser.readline()

		#if(X[:1]=="R"):
		#	print("Right")
		#if(X[:1] == "L"):
		#	valLeft.value += 1
		valLeft.value += 1

def calculate_rpm():
	print("Calculate RPM")
	while True:
		oldValLeft=int(valLeft.value)

		time.sleep(0.5)
		newValLeft=int(valLeft.value)

		rpmLeft.value=(((float(newValLeft)-float(oldValLeft))/1024)*120)
		

def adjust_motor():
	while True:
		global integral
		global previous_error
		error = setRPM - rpmLeft.value
		integral = integral + (error*.02)
		derivative = (error -previous_error) / .02
		escVal = P*error + I*integral + D*derivative
		print("ESC" ,escVal)
		set_esc(int(escVal))
		time.sleep(0.75)

def set_esc(escVal):
	pwm.setPWM(pwmPosL,0,escVal)
		


p1 = Process(target=read_encoder)
p1.start()
p2 = Process(target=calculate_rpm)
p2.start()
p3 = Process(target=adjust_motor)
p3.start()

p1.join()
p2.join()
p3.join()
