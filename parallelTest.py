from multiprocessing import Process, Manager, Value
import serial
import time

manager = Manager()
val = manager.Value('i',0)

ser = serial.Serial('/dev/ttyACM1', baudrate = 115200)
if ser.isOpen():
	print "Open: " + ser.portstr
	ser.write(b'S')



def func1(val, name=''):
	#global val
	while True:
		X = ser.readline()
		val.value += 1
		#print("In",val)

def func2():
	#global val
	while True:
		oldVal=int(val.value)
		#print("o",oldVal)
		time.sleep(1)
		newVal=int(val.value)
		#print("i",val.value)
		rpm=((float(newVal)-float(oldVal))/1024)*60
		print("rpm: {0}".format(rpm))


if __name__ == '__main__':
	p1 = Process(target=func1, args=(val,'val'))
	p1.start()
	p2 = Process(target=func2)
	p2.start()
	p1.join()
 	p2.join()
