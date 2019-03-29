import os
import Tkinter as tkinter
import time
from PIL import Image
from PIL import ImageTk
import Adafruit_PWM_Servo_Driver
import socket
import serial
from multiprocessing import Process, Manager, Value
import math

    
pwm = Adafruit_PWM_Servo_Driver.PWM(address=0x40, busnum=0)



pwmPosR = 0
pwmPosL = 1

minESC = 320
pwm.setPWMFreq(60)
time.sleep(1)
pwm.setPWM(pwmPosR,0,minESC)
pwm.setPWM(pwmPosL,0,minESC)
print("Initializing Motors")
time.sleep(2)
maxESC = 355
brakeESC = 320
UPDATE_RATE = 5000

rpmRight=0    
rpmLeft=0


manager = Manager()
valLeft = manager.Value('i',0)
valRight = manager.Value('i',0)
rpmRight = manager.Value('i',0)
rpmLeft = manager.Value('i',0)

connect = False
escVal = minESC

ser = None

root = tkinter.Tk()
valRight_new=tkinter.StringVar()
valLeft_new=tkinter.StringVar()
valRight_new.set('Right RPM: '+'0')
valLeft_new.set('Left RPM: '+'0')

try:
	ser = serial.Serial('/dev/ttyACM', baudrate = 115200)
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
        pwm.setPWM(pwmPosR, 0, escVal)
	pwm.setPWM(pwmPosL, 0, escVal)
    print_ESC()
    
def down_action():
    global escVal
    if(escVal > minESC):
        escVal = escVal-1
        pwm.setPWM(pwmPosR, 0, escVal)
	pwm.setPWM(pwmPosL, 0, escVal)
    print_ESC()
    
def brake_action():
	global escVal
	escVal = brakeESC
	pwm.setPWM(pwmPosR, 0, escVal)
	pwm.setPWM(pwmPosL, 0, escVal)
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

def read_encoder(valRight, valLeft):
	while True:
		X = ser.readline()

		if(X[:1]=="R"):
			valRight.value += 1
		if(X[:1] == "L"):
			valLeft.value += 1

def display_rpm():
	while True:
		oldValRight=int(valRight.value)
		oldValLeft=int(valLeft.value)

		time.sleep(0.125)
		newValRight=int(valRight.value)
		newValLeft=int(valLeft.value)

		rpmRight.value=(((float(newValRight)-float(oldValRight))/1024)*480)
		rpmLeft.value=(((float(newValLeft)-float(oldValLeft))/1024)*480)

		valRight_new.set(rpmRight.value)
		valLeft_new.set(rpmLeft.value)
		
def adjust_motor():
	global minESC, setRPM
	print("Adjust Motor")
	esc = minESC
	while True:
		print("Left"+str(int(rpmLeft.value)))
		rpm = int(rpmLeft.value)

		if(setRPM*0.75 <= rpm <= setRPM*1.25):
			print("stay")

		elif(rpm < (setRPM)):
			if(esc<maxESC):
	                	esc += 1
				print("increase: "+str(esc))
				set_esc(pwmPosL,esc)
		elif(rpm > setRPM):
			if(esc>minESC):
				esc -= 1
				print("decrease: "+str(esc))
				set_esc(pwmPosL,esc)
		time.sleep(0.25)


def update_btn():
	global rpmRight, rpmLeft, valRight_new, valLeft_new
	valRight_new.set("Right RPM: "+str(int(rpmRight.value)))
	valLeft_new.set("Left Rpm: "+str(int(rpmLeft.value)))

	root.after(500,update_btn)
	

def func3():
	global root
	root.title("Command Center")
	root.geometry("500x550")
    
	up = tkinter.PhotoImage(file="upArrow.png")
	down = tkinter.PhotoImage(file="downArrow.png")
	stopL = Image.open("stop.png")
	stopL = stopL.resize((100,100),Image.ANTIALIAS)
	stop =  ImageTk.PhotoImage(stopL)
    
	upBtn = tkinter.Button(root,  text="up", bg='green', image=up, command=up_action).grid(row=0,column=0)
	downBtn = tkinter.Button(root,  text="down", bg='green',  image=down, command=down_action).grid(row=2,column=0)
	brakeBtn = tkinter.Button(root, text="reset", bg='red', width = 100, height = 100, image=stop, command=brake_action).grid(row=1, column=4, rowspan=2)

	

	speedLblRight = tkinter.Label(root, text="Right RPM: ",textvariable=valRight_new, width = 20, height=5).grid(row=0,column=5)
	speedLblLeft = tkinter.Label(root, text="Left RPM: ",textvariable=valLeft_new, width = 20, height=5).grid(row=1,column=5)

	connectBtn = tkinter.Button(root, text="connect", width = 20, height = 20, command=serial_connect).grid(row=0, column=4)
	
  
	root.after(1,update_btn)
	root.mainloop()
	brake_action()
	p1.terminate()
	p2.terminate()




p1 = Process(target=read_encoder, args=(valRight,valLeft))
p1.start()
p2 = Process(target=display_rpm)
p2.start()
p3 = Process(target=func3)
p3.start()

p1.join()
p2.join()
p3.join()
