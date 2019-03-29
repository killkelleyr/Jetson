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
import socket

pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x40, busnum=1)
HOST = '192.168.1.198'
PORT = 5002
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
sep = ' '
pwmPosL = 1

minESC = 2550
pwm.setPWMFreq(500)

time.sleep(1)
pwm.setPWM(pwmPosL, 0, minESC)
time.sleep(2)
#pwm.setPWM(pwmPosL,0,328)


maxESC = 10000                                                                                                                 
#setRPM = 100

manager = Manager()
valLeft = manager.Value('i', 0)
rpmLeft = manager.Value('i', 0)
setRPM = manager.Value('i',0)
#setRPM.Value = 0
ser = None


def get_controller():
	while True:
		buf = ''
		while sep not in buf:
			buf += s.recv(8)
		try:
			data = int(buf)
		except:
			data = data
		setRPM.value = data
		print("RPM Value: "+str(setRPM.value))

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

		time.sleep(0.125)
		newValLeft=int(valLeft.value)

		rpmLeft.value=(((float(newValLeft)-float(oldValLeft))/1024)*480)
		

def adjust_motor():
	global minESC, setRPM
	print("Adjust Motor")
	esc = minESC
	while True:
		print("Left"+str(int(rpmLeft.value)))
		rpm = int(rpmLeft.value)

		if(int(setRPM.value) <= rpm <= int(setRPM.value)):
			print("setpt: "+str(setRPM.value))
			print("stay")

		elif(rpm < int(setRPM.value)):
			if(esc<maxESC):
	                	esc += 1
				print("setpt: "+str(setRPM.value))
				print("increase: "+str(esc))
				set_esc(pwmPosL,esc)
		elif(rpm > int(setRPM.value)):
			if(esc>minESC):
				esc -= 1
				print("setpt: "+str(setRPM.value))
				print("decrease: "+str(esc))
				set_esc(pwmPosL,esc)
		time.sleep(0.01)

def set_esc(pos,escVal):
	pwm.setPWM(pos,0,escVal)
		


p1 = Process(target=read_encoder)
p1.start()
p2 = Process(target=calculate_rpm)
p2.start()
p3 = Process(target=adjust_motor)
p3.start()
p4 = Process(target=get_controller)
p4.start()

p1.join()
p2.join()
p3.join()
p4.join()
