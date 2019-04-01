import time
from multiprocessing import Process, Manager, Value
import socket

HOST = '192.168.1.198'
PORT = 5002
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
sep = ' '

def get_controller():
	data = 2554
	print("Got to loop")
	while True:
		buf = ''
		while len(buf) < 9:
			buf += s.recv(8)
		
		try:
			left,right=buf.split(",")
			print("Left: "+left,right)
			dataL = int(left)
			dataR = int(right)
			if(len(str(dataL)) > 3):
				set_esc(dataL)
			if(len(str(dataR)) > 3):
				set_esc(dataR)
				#print("ESC Value: "+str(dataL)+","+str(dataR))
		except:
			data = data

def set_esc(val):
	print("Received: "+str(val))

get_controller()
