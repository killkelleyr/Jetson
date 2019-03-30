import time
from Adafruit_I2C import Adafruit_I2C
import Adafruit_PWM_Servo_Driver
import serial
from multiprocessing import Process, Manager, Value
import socket
data = 2554
pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x40, busnum=1)
HOST = '192.168.1.198'
PORT = 5002
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
sep = ' '
pwmPosL = 1
pwmPosR = 0

minESC = 2550
pwm.setPWMFreq(500)

print("Initialize")
time.sleep(1)
pwm.setPWM(pwmPosL, 0, minESC)
pwm.setPWM(pwmPosR, 0, minESC)
time.sleep(2)


maxESC=10000                                                                                                                 

ser = None

def get_controller():
	data = 2554
	while True:
		buf = ''
		while len(buf) < 9:
			buf += s.recv(8)
		
		try:
			left,right=buf.split(",")
			print("Left: "+left,right)
			dataL = int(left)
			dataR = int(right)
			if(len(str(dataL)) > 3):
				set_esc(pwmPosL,dataL)
			if(len(str(dataR)) > 3):
				set_esc(pwmPosR,dataR)
				print("ESC Value: "+str(dataL)+","+str(dataR))
		except:
			data = data
		

def set_esc(pos,escVal):
	pwm.setPWM(pos,0,escVal)

get_controller()


