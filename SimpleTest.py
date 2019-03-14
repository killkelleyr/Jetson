import time
from Adafruit_I2C import Adafruit_I2C
import Adafruit_PWM_Servo_Driver

pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x40, busnum=0)
#pwm = Adafruit_PWM_Servo_Driver.PWM()

servo_min = 390
servo_max = 570

count = servo_min

pwm.setPWMFreq(60)
time.sleep(1)
pwm.setPWM(0,0,400)
#while count < servo_max:	
#	pwm.setPWM(0, 0, count)
#	time.sleep(1)
#	count = count + 25
