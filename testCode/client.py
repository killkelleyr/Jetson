import time
import socket

HOST = '192.168.1.198'
PORT = 5002
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

data = ""
def get_controller():
	while True:
		buf = ''
		while len(buf) < 9:
			hold += s.recv(1)
			if hold == "[":
				pass
			elif hold == "]":
				pass
			else
				buf += hold
		left,right = buf.split(',')
		print("L: "+str(left)+" R: "+str(right))
		hold = ''

get_controller()
