import socket
import time
from multiprocessing import Manager, Process

#Define the server IP and Port to open
HOST='192.168.1.198'
PORT=5002
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr=s.accept()

escValLeft = 2554
escValRight = 2556

sep = " "

def sendtoclient():
	while True:
		val = "["+str(int(escValLeft))+","+str(int(escValRight))+"]"
		print("Sending: " + val)
		conn.send(val)

sendtoclient()
