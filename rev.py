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
#pwm.setPWM(pwmPosR, 0, minESC)
time.sleep(1)

count = 2500
print("starting rev")
while count > 2450:
	pwm.setPWM(pwmPosL, 0, count)
	print("val: "+str(count))
	time.sleep(0.05)
	count -= 1
print("stop")
pwm.setPWM(pwmPosL, 0, minESC)
time.sleep(2)
print("going forward")
pwm.setPWM(pwmPosL, 0, 2610)
time.sleep(2)
print("stop")
pwm.setPWM(pwmPosL, 0, minESC)
