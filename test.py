import time
from Adafruit_I2C import Adafruit_I2C
import Adafruit_PWM_Servo_Driver

pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x40, busnum=0)

pwm.setPWMFreq(1000)
time.sleep(1)
#pwm.setPWM(1,0,320)
#time.sleep(1)

start = 0
inc = 1

time.sleep(1)
print("initial")
pwm.setPWM(0,0,2550)
pwm.setPWM(1,0,2550)
time.sleep(2)


on = start
#off = on + 328 + inc
off = 2600

while True:
	pwm.setPWM(1,on,off)
	pwm.setPWM(0,on,off)
	print("ON: ",on)
	print("off: ",off)
	off += 100
	time.sleep(0.5)
