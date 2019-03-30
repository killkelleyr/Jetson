from inputs import get_gamepad
import socket
import time
from multiprocessing import Manager, Process

HOST='192.168.1.198'
PORT=5002
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2)
conn, addr=s.accept()

minESC = 2600.0
maxESC = 3000.0

minThrottle = 0.0
maxThrottle = 1023.0
escValue = 0

sep = ' '

manager = Manager()
escValLeft = manager.Value('i',2554)
escValRight = manager.Value('i',2554)


def gamepad():
	while 1:
		events = get_gamepad()
		for event in events:
			if(event.code == "ABS_Z"):
				percentage = float(float(event.state)/maxThrottle)
				escValLeft.value = (((maxESC-minESC)/(maxThrottle-minThrottle))*float(event.state) + minESC)

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
