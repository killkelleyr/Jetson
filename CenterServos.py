import time
from Adafruit_I2C import Adafruit_I2C
import Adafruit_PWM_Servo_Driver

pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x44, busnum=0)

VERTservo_mid = 450 #Middle

pwm.setPWMFreq(60)


pwm.setPWM(0,0,330)
pwm.setPWM(1,0,410)
