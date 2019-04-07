import time
import socket

HOST = '192.168.2.62'
PORT = 5002
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

data = ""
def get_controller():
	count = 0
	while True:
		buf = ''
		hold = ''
		while len(buf) < 9:
			hold = s.recv(1)
			if hold == '[':
				pass
			elif hold == ']':
				pass
			else:
				buf += hold
		print(buf)
		left,right = buf.split(',')
		print("L: "+str(left)+" R: "+str(right))
		

get_controller()
