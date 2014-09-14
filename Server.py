#Server for Airchat

#Imports
from socket import *
import _thread as thread
import time

#Set the buffersize, hostname and port
BUFF = 1024
HOST = 'localhost'
PORT = 65000

#Create a username list and socket list
list=[]
ul = []

#Handler for sockets
def handler(clientsock,addr):
	joinnew = True
	#Add them to the list of sockets
	list.append(clientsock)
	#Set their default username (hostname)
	USERNAME = "<"+gethostbyaddr(addr[0])[0]+">"
	while 1:
		#If they disconnect, remove thier username from the list and also thier socket
		try:
			data = str(clientsock.recv(BUFF))
		except:
			list.pop(list.index(clientsock))
			if USERNAME == gethostbyaddr(addr[0]):
				pass
			else:
				ul.pop(ul.index(USERNAME))
			break
		
		#Send the other clients the current socket's messages
		for i in list:
			#If the client is new:
			if joinnew == True:
				i.send((USERNAME+" joined the server.").encode('utf-8')) #Say they just joined
				joinnew = False
			repr(list)
			print('data:' + repr(data))
			repr(list)
			if not data:
				break
			if "~" not in data:
				i.send((USERNAME+":"+data).encode('utf-8'))	
			#Change thier name if there is a '~' in front
			if "~" in data:
				try:
					USERNAME = ("<"+data.replace("b'",'',1).replace("'",'').replace('~','',1)+">".replace(' ','',1))
					if USERNAME in ul:
						USERNAME = "<"+gethostbyaddr(addr[0])[0]+">"
						clientsock.send("<Alert> Username Taken. Reseting username to hostname...".encode("utf-8"))
					else:
						ul.append(USERNAME)
						i.send(("<"+gethostbyaddr(addr[0])[0]+">"+" has changed thier username to "+USERNAME).encode('utf-8'))
				except:
					clientsock.send("<Alert> Error.".encode("utf-8"))

#Run server

if __name__=='__main__':
	ADDR = (HOST, PORT)
	serversock = socket(AF_INET, SOCK_STREAM)
	serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	serversock.bind(ADDR)
	serversock.listen(5)
	while 1:
		#Mainloop
		print('waiting for connection...')
		clientsock, addr = serversock.accept()
		print ('...connected from:', addr)
		thread.start_new_thread(handler, (clientsock, addr))