import socket
import threading
import time
import random
import pickle

server=None
host="127.0.0.1"
port=8004
client=""
clients=[]
client_names=[]
threads=[]

def connect():

	d= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	d.connect((host,port))
	receive(d)

def receive(d):
	while(True):
		var =d.recv(1024)
		
		try:
			key=pickle.loads(var)
			print(key)
		except:
			print (var.decode())
			
			inp=input()
			d.send(inp.encode())


	

connect()

