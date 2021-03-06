import time
from Adafruit_I2C import Adafruit_I2C
import Adafruit_PWM_Servo_Driver

pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x44, busnum=0)

pwm.setPWMFreq(60)

VERTservo_min = 390
VERTservo_mid = 450 #Middle
VERTservo_max = 560

servo_min = 190
servo_max = 590

count = servo_max
height = 390

def pan_range(start, end, step):
	while start != end:
		yield start
		start += step

def Low_pan(count, VERTservo_min):
	for count in pan_range(servo_min, servo_max, 5):
		pwm.setPWM(0,0,VERTservo_min)
		pwm.setPWM(1,0,count)
		time.sleep(0.1)
		

def Mid_pan(count, VERTservo_mid):
	for count in pan_range(servo_max, servo_min, -5):
		pwm.setPWM(0,0,VERTservo_mid)
		pwm.setPWM(1,0,count)
		time.sleep(0.1)

def High_pan(count, VERTservo_max):
	for count in pan_range(servo_min, servo_max, 5):
		pwm.setPWM(0,0,VERTservo_max)
		pwm.setPWM(1,0,count)
		time.sleep(0.1)

		
pwm.setPWM(1,0,servo_min)
pwm.setPWM(0,0,VERTservo_mid)
time.sleep(2)
Low_pan(count, VERTservo_min)

while height <= VERTservo_mid:
	pwm.setPWM(0,0,height)
	time.sleep(0.1)
	height = height + 5

Mid_pan(count, VERTservo_mid)

while height <= VERTservo_max:
	pwm.setPWM(0,0,height)
	time.sleep(0.1)
	height = height + 5

High_pan(count, VERTservo_max)

while height >= VERTservo_mid:
	pwm.setPWM(0,0,height)
	time.sleep(0.1)
	height = height - 5

Mid_pan(count, VERTservo_mid)
#pwm.setPWM(1,0,servo_min)
#pwm.setPWM(0,0,VERTservo_mid)
	
#count = servo_min
#pwm.setPWMFreq(60)
#while count < VERTservo_mid:	
	#pwm.setPWM(0, 0, count)
	#time.sleep(1)
	#count = count + 25
