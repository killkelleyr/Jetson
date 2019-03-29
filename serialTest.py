import serial
import time
from multiprocessing import Process

dist_meas = 0.00
km_per_hour = 0
rpm = 0
elapse = 0
sensor = 12
pulse = 0
start_timer = time.time()
val = 0


def calculate_speed(r_cm):
	global pulse,elapse,rpm,dist_km,dist_meas,km_per_sec,km_per_hour
	if elapse !=0:							# to avoid DivisionByZero error
		rpm = 1/elapse * 60
		circ_cm = (2*math.pi)*r_cm			# calculate wheel circumference in CM
		dist_km = circ_cm/100000 			# convert cm to km
		km_per_sec = dist_km / elapse		# calculate KM/sec
		km_per_hour = km_per_sec * 3600		# calculate KM/h
		dist_meas = (dist_km*pulse)*1000	# measure distance traverse in meter
		return km_per_hour



ser = serial.Serial('/dev/ttyUSB0', baudrate = 9600)
if ser.isOpen():
	print "Open: " + ser.portstr
	ser.write(b'S')

# 	while True:
		#calculate_speed(20)	# call this function with wheel radius as parameter
  		#print('rpm:{0:.0f}-RPM kmh:{1:.0f}-KMH dist_meas:{2:.2f}m pulse:{3}'.format(rpm,km_per_hour,dist_meas,pulse))
		#time.sleep(0.1)

def read_val():
	global val
	val = ser.readline()

while 1:
	read_val()

	print("val"+val)
	#time.sleep(1)
	#new=ser.readline()
	#print("new",new)
	#rpm = (float(new)-float(initial))*60
	#print("rpm:",rpm)
	#print(X)
