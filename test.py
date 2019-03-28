from Adafruit_I2C import Adafruit_I2C
import Adafruit_PWM_Servo_Driver
from inputs import get_gamepad
import time

pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x40, busnum=0)

pwmPosL = 1
minESC = 2554
maxESC = 4554
pwm.setPWMFreq(500)
pwm.setPWM(pwmPosL, 0, minESC)
time.sleep(2)


minThrottle = 0
maxThrottle = 255


while 1:
	events = get_gamepad()
	for event in events:
        #Triggers Max: 255 Min: 0
		if(event.code == "ABS_Z"):
			percentage = (event.state/255)
			escValue = (((maxESC-minESC)/(maxThrottle-minThrottle))*event.state + minESC)
			pwm.setPWM(pwmPosL,0,escValue)
            		print("Left Trigger: "+str(int(percentage*100))+"%")
			
        	if(event.code == "ABS_RZ"):
            		percentage = (event.state/255)
            		escValue = (((maxESC-minESC)/(maxThrottle-minThrottle))*event.state + minESC)
            		print("Right Trigger: "+str(int(percentage*100))+"%")
        	print("Val to send to esc: "+str(int(escValue)))
