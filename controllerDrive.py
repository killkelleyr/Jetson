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

minESC = 2550
pwm.setPWMFreq(500)

print("Initialize")
time.sleep(1)
pwm.setPWM(pwmPosL, 0, minESC)
time.sleep(2)
#pwm.setPWM(pwmPosL,0,328)


maxESC=10000                                                                                                                 
#setRPM = 100

ser = None

def get_controller():
	data = 2554
	while True:
		buf = ''
		while sep not in buf:
			buf += s.recv(8)
		try:
			data = int(buf)
			if(len(str(data)) > 3):
				set_esc(pwmPosL,data)
				print("ESC Value: "+str(data))
		except:
			data = data
		

def set_esc(pos,escVal):
	pwm.setPWM(pos,0,escVal)

get_controller()


