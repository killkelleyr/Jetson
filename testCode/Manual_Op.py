import time
from Adafruit_I2C import Adafruit_I2C
import Adafruit_PWM_Servo_Driver
from multiprocessing import Process, Manager, Value
import socket
data = 2554
pwmD = Adafruit_PWM_Servo_Driver.PWM(address=0x40, busnum=1)
pwmC = Adafruit_PWM_Servo_Driver.PWM(address=0x44, busnum=0)
HOST = '192.168.2.62'
PORT = 5002
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

pwmD.setPWMFreq(500)
pwmC.setPWMFreq(60)

sep = ' '
pwmPosL = 0
pwmPosR = 1

pwmPosT = 0
pwmPosP = 1

minESC = 2550

VERTservo_min = 190
VERTservo_mid = 330 #Middle
VERTservo_max = 450

servo_min = 260
servo_max = 590

print("Initialize")
time.sleep(1)
pwmD.setPWM(pwmPosL, 0, minESC)
pwmD.setPWM(pwmPosR, 0, minESC)

maxESC=10000                                                                                                                 
dataL = minESC
dataR = minESC
ser = None

def get_controller():
	global dataL
	global dataR
	
	while True:
		buf = ''
		hold = ''
		while len(buf) < 17:
			hold = s.recv(1)
			#print (hold)
			if hold == '[':
				pass
			elif hold == ']':
				pass
			else:
				buf += hold
		leftESC,rightESC,pan,tilt = buf.split(',')
		dataL = int(leftESC)
		dataR = int(rightESC)
		dataP = int(pan)
		dataT = int(tilt)
		set_esc(pwmPosL,dataL)
		set_esc(pwmPosR,dataR)
		set_PT(pwmPosT,dataT)
		set_PT(pwmPosP,dataP)
		
def set_esc(pwmPos, data):
	pwmD.setPWM(pwmPos,0,data)

def set_PT(pwmPos, data):
	pwmC.setPWM(pwmPos,0,data)

get_controller()
	

