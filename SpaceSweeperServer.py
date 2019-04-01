from inputs import get_gamepad
import socket
import time
from multiprocessing import Manager, Process

#Define the server IP and Port to open
HOST='192.168.1.198'
PORT=5002
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2)
conn, addr=s.accept()

#set the range of ESC values to send
minESC = 2550.0
maxESC = 2800.0

minESCRev = 2450
maxESCRev = 2420

#set the range of the triggers
#minThrottle = 0.0
#maxThrottle = 1023.0

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
			if(event.code == "ABS_Y"): #ABS_Z
				if (event.state > 9000):
					percentage = float(float(event.state)/maxThrottle)
					escValLeft.value = (((maxESC-minESC)/(maxThrottle-minThrottle))*float(event.state) + minESC)
				elif (event.state < -9000):
					escValLeft.value = (((maxESCRev-minESCRev)/(maxThrottle-minThrottle))*float(abs(event.state)) + minESCRev+10)
				else:
					escValLeft.value = minESC

			if(event.code == "ABS_RZ"):
				percentage = float(event.state/maxThrottle)
				escValRight.value = (((maxESC-minESC)/(maxThrottle-minThrottle))*float(event.state) + minESC)


def sendtoclient():
	while True:
		val = str(int(escValLeft.value))+","+str(int(escValRight.value))+sep
		print("Sending: " + val)
		conn.send(val)

p1 = Process(target=gamepad)
p1.start()
p2 = Process(target=sendtoclient)
p2.start()

p1.join()
p2.join()
