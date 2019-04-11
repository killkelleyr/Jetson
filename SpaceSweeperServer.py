from inputs import get_gamepad
import socket
import time
from multiprocessing import Manager, Process

#Define the server IP and Port to open
HOST='192.168.2.62'
PORT=5002
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr=s.accept()

#set the range of ESC values to send
minESC = 2550.0
maxESC = 2700.0

minESCRev = 2450
maxESCRev = 2420

#set the range of the triggers
#minThrottle = 0.0
#maxThrottle = 1023.0
minT = 0.0
maxT = 1023.0

minThrottle = 9000.0
maxThrottle = 32767.0

sep = ' '

manager = Manager()
escValLeft = manager.Value('i',2554)
escValRight = manager.Value('i',2554)


def gamepad():
	while 1:
		events = get_gamepad()
		for event in events:
			if(event.code == "ABS_Y"): #ABS_Z# Rev
				if (event.state > 9000):
					escValLeft.value = (((maxESCRev-minESCRev)/(maxThrottle-minThrottle))*float(abs(event.state)) + minESCRev+10)

				elif (event.state < -9000): #for
					escValLeft.value = (((maxESC-minESC)/(maxThrottle-minThrottle))*float(abs(event.state)) + minESC)
				else:
					escValLeft.value = minESC

			if(event.code == "ABS_RY"):
				if (event.state > 9000):
					escValRight.value = (((maxESCRev-minESCRev)/(maxThrottle-minThrottle))*float(abs(event.state)) + minESCRev+10)
				elif (event.state < -9000):
					escValRight.value = (((maxESC-minESC)/(maxThrottle-minThrottle))*float(abs(event.state)) + minESC)
				else:
					escValRight.value = minESC
			sendtoclient()

def sendtoclient():
	val = "["+str(int(escValLeft.value))+","+str(int(escValRight.value))+"]"
	print("Sending: " + val)
	conn.send(val)

gamepad()

