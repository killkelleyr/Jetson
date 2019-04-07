from Adafruit_I2C import Adafruit_I2C
import Adafruit_PWM_Servo_Driver
import time

pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x40, busnum=1)

pwmPosL = 0
pwmPosR = 1

minESC = 2550
pwm.setPWMFreq(500)

print("Initialize")
time.sleep(1)
pwm.setPWM(pwmPosL, 0, minESC)
pwm.setPWM(pwmPosR, 0, minESC)
time.sleep(1)


def turn_Left():
	print("Turning Left")
	pwm.setPWM(pwmPosL,0,2475)
	pwm.setPWM(pwmPosR,0,2665)
	#time.sleep(0.5)

def turn_Right():
	print("Turning Right")
	pwm.setPWM(pwmPosR,0,2470)
	pwm.setPWM(pwmPosL,0,2685)
	#time.sleep(0.5)

def stop_Motors():
	print("Stopping Motors")
	pwm.setPWM(pwmPosL,0,minESC)
	pwm.setPWM(pwmPosR,0,minESC)

def reverse():
	pwm.setPWM(pwmPosL,0,2470)
	pwm.setPWM(pwmPosR,0,2470)

def forward():
	pwm.setPWM(pwmPosL,0,2645)
	pwm.setPWM(pwmPosR,0,2645)

def initiate():
	pwm.setPWM(pwmPosL,0,2450)
	pwm.setPWM(pwmPosR,0,2450)

#turn_Right()
#time.sleep(0.5)
#stop_Motors()
#time.sleep(2)
#turn_Left()
#forward()
#time.sleep(1)
#stop_Motors()
#time.sleep(0.5)

forward()
time.sleep(2)
stop_Motors()
time.sleep(0.5)
initiate()
time.sleep(0.05)
stop_Motors()
time.sleep(0.05)
reverse()
time.sleep(1)
stop_Motors()



#print("stop")
#pwm.setPWM(pwmPosL, 0, minESC)
#pwm.setPWM(pwmPosR, 0, minESC)
