import os
import Tkinter as tkinter
import time
from PIL import Image
from PIL import ImageTk
from Adafruit_I2C import Adafruit_I2C
import Adafruit_PWM_Servo_Driver
import serial
    
pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x40, busnum=0)
ser = serial.Serial('/dev/ttyACM0', baudrate = 500000)


pwmPos = 2

minESC = 320
pwm.setPWM(pwmPos,0,minESC)
maxESC = 350
brakeESC = 320
UPDATE_RATE = 5000
    
    
connect = False
escVal = minESC
    
#def updater(self):
#    self.after(UPDATE_RATE, self.updater)
    
def up_action():
    global escVal
    if(escVal < maxESC):
        escVal = escVal+1
        pwm.setPWM(pwmPos, 0, escVal)
    print_ESC()
    
def down_action():
    global escVal
    if(escVal > minESC):
        escVal = escVal-1
        pwm.setPWM(pwmPos, 0, escVal)
    print_ESC()
    
def brake_action():
    global escVal
    escVal = brakeESC
    pwm.setPWM(pwmPos, 0, escVal)
    print_ESC()
    
def print_ESC():
    print("Current ESC Value:",escVal)
	
def serial_connect():
	if ser.isOpen():
		print("open: " + ser.portstr)
		ser.write(b'S')
	else:
		print("connection failed")



root = tkinter.Tk()
root.title("Command Center")
root.geometry("500x500")
    
up = tkinter.PhotoImage(file="upArrow.png")
down = tkinter.PhotoImage(file="downArrow.png")
stopL = Image.open("stop.png")
stopL = stopL.resize((100,100),Image.ANTIALIAS)
stop =  ImageTk.PhotoImage(stopL)
    
upBtn = tkinter.Button(root,  text="up", bg='green', image=up, command=up_action).grid(row=0,column=0)
downBtn = tkinter.Button(root,  text="down", bg='green',  image=down, command=down_action).grid(row=2,column=0)
brakeBtn = tkinter.Button(root, text="reset", bg='red', width = 100, height = 100, image=stop, command=brake_action).grid(row=1, column=4, rowspan=2)
connectBtn = tkinter.Button(root, text="connect", width = 100, height = 100, command=serial_connect).grid(row=0, column=4)

  
root.mainloop()
