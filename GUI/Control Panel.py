import os
import Tkinter as tkinter
import time
from PIL import Image
from PIL import ImageTk
from Adafruit_I2C import Adafruit_I2C
import Adafruit_PWM_Servo_Driver
import serial
from multiprocessing import Process, Manager, Value
import math
from functools import partial

    
pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x40, busnum=0)



pwmPos = 2

minESC = 320
time.sleep(1)
pwm.setPWM(pwmPos,0,minESC)
time.sleep(2)
maxESC = 500
brakeESC = 320
UPDATE_RATE = 5000

rpm=0    



manager = Manager()
val = manager.Value('i',0)
rpm = manager.Value('i',0)

connect = False
escVal = minESC

ser = None

root = tkinter.Tk()
val_new=tkinter.StringVar()
val_new.set('RPM: '+'0')

try:
	ser = serial.Serial('/dev/ttyACM1', baudrate = 115200)
	if ser.isOpen():
		print("open: " + ser.portstr)
		ser.write(b'S')
		connect = True
				
	else:
		print("connection failed")	
except:
	print("ttyACM0 not found")

    
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
	global connect
	global ser
	if(connect == False):
		try:
			ser = serial.Serial('/dev/ttyACM0', baudrate = 115200)
			if ser.isOpen():
				print("open: " + ser.portstr)
				ser.write(b'S')
				connect = True
				
			else:
				print("connection failed")	
		except:
			print("ttyACM0 not found")

	else:
		print("Already Connected")
		ser.close()
		connect = False

def read_encoder(val, name=''):
	while True:
		X = ser.readline()
		val.value += 1

def display_rpm():
	while True:
		oldVal=int(val.value)
		time.sleep(1)
		newVal=int(val.value)
		rpm.value=(((float(newVal)-float(oldVal))/1024)*60)
		#val_new.set(rpm.value)		
		#partial(update_btn, rpm)
		

def update_btn():
	global rpm, val_new
	val_new.set("RPM: "+str(int(rpm.value)))
	#speedLbl.text(rpm)
	print("rpm: {0}".format(int(rpm.value)))
	root.after(500,update_btn)
	

def func3():
	#root = tkinter.Tk()
	global root
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

	

	speedLbl = tkinter.Label(root, text="RPM: ",textvariable=val_new, width = 10, height=10).grid(row=0,column=5)

	connectBtn = tkinter.Button(root, text="connect", width = 20, height = 20, command=serial_connect).grid(row=0, column=4)
	
	#update_btn()
  
	root.after(1,update_btn)
	root.mainloop()
	brake_action()
	p1.terminate()
	p2.terminate()




p1 = Process(target=read_encoder, args=(val,'val'))
p1.start()
p2 = Process(target=display_rpm)
p2.start()
p3 = Process(target=func3)
p3.start()

p1.join()
p2.join()
p3.join()
