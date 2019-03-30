import socket
import time
HOST='192.168.1.198'
PORT=5002
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

sep = ' '

while True:
    buf = ''
    while sep not in buf:
        buf += s.recv(8)
    try:
        data = int(buf)
    except:
        data = data
    #data=s.recv(8096)
    print("Received: "+str(data))

