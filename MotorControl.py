import time
from Adafruit_I2C import Adafruit_I2C
import Adafruit_PWM_Servo_Driver

pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x40, busnum=0)
#pwm = Adafruit_PWM_Servo_Driver.PWM()

servo_min = 320

servo_max = 570

count = servo_min

pwm.setPWMFreq(60)
time.sleep(1)
pwm.setPWM(0,0,320)
pwm.setPWM(1,0,320)
print("initializing")
time.sleep(2)
print("spining")
pwm.setPWM(0,0,330)
pwm.setPWM(1,0,330)
time.sleep(5)
print("Stop")
pwm.setPWM(0,0,320)
pwm.setPWM(1,0,320)

#while count < servo_max:	
#	pwm.setPWM(0, 0, count)
#	time.sleep(1)
#	count = count + 25
