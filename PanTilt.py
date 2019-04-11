import time
from Adafruit_I2C import Adafruit_I2C
import Adafruit_PWM_Servo_Driver

pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x44, busnum=0)

pwm.setPWMFreq(60)

VERTservo_min = 190
VERTservo_mid = 330 #Middle
VERTservo_max = 450

servo_min = 260
servo_max = 590

count = servo_max
height = 330



def pan_range(start, end, step):
	while start != end:
		yield start
		start += step

def Low_pan(count, VERTservo_min):
	for count in pan_range(servo_min, servo_max, 1):
		pwm.setPWM(0,0,VERTservo_min)
		pwm.setPWM(1,0,count)
		time.sleep(0.01)
		

def Mid_pan(count, VERTservo_mid):
	for count in pan_range(servo_max, servo_min, -1):
		pwm.setPWM(0,0,VERTservo_mid)
		pwm.setPWM(1,0,count)
		time.sleep(0.01)

def High_pan(count, VERTservo_max):
	for count in pan_range(servo_min, servo_max, 1):
		pwm.setPWM(0,0,VERTservo_max)
		pwm.setPWM(1,0,count)
		time.sleep(0.01)

		
pwm.setPWM(1,0,servo_min)
pwm.setPWM(0,0,VERTservo_mid)
time.sleep(2)


while True:
	while height >= VERTservo_min:
		pwm.setPWM(0,0,height)
		time.sleep(0.01)
		height = height - 1

	Low_pan(count, VERTservo_min)

	while height <= VERTservo_mid:
		pwm.setPWM(0,0,height)
		time.sleep(0.01)
		height = height + 1
	
	Mid_pan(count, VERTservo_mid)

	while height <= VERTservo_max:
		pwm.setPWM(0,0,height)
		time.sleep(0.01)
		height = height + 1

	High_pan(count, VERTservo_max)

	while height >= VERTservo_mid:
		pwm.setPWM(0,0,height)
		time.sleep(0.01)
		height = height - 1

	Mid_pan(count, VERTservo_mid)
	

