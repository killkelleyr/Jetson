import time
from inputs import get_gamepad
maxUp = -32768
middle = 0
minDown = 32767

minESC = 2600.0
maxESC = 3000.0



def gamepad():
	while 1:
		events = get_gamepad()
		for event in events:
			if(event.code == "ABS_Y"):
				print ("Left: "+str(event.state))
			if(event.code == "ABS_RY"):
				print ("Right: "+str(event.state))

gamepad()
