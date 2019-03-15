import serial

ser = serial.Serial('/dev/ttyACM0', baudrate = 500000)
if ser.isOpen():
	print "Open: " + ser.portstr
	ser.write(b'S')
while 1:
	X=ser.readline()
	print(X)
