#Server for Airchat

#Imports
from socket import *
import _thread as thread
import time
import ssl

#Set the buffersize, hostname and port
BUFF = 1024
HOST = '0.0.0.0'
PORT = 65000

#Create a username list and socket list
list=[]
ul = []

#Handler for sockets
def handler(clientsock,addr):
	joinnew = True
	userset = False
	#Add them to the list of sockets
	list.append(clientsock)
	#Set their default username (hostname)
	USERNAME = "<"+gethostbyaddr(addr[0])[0]+">"
	while 1:
		#If they disconnect, remove thier username from the list and also thier socket
		try:
			data = str(clientsock.recv(BUFF))
		except:
			data = ""
		if not data:
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
			if not data:
				break
			if "~" not in data:
				if i == clientsock:
					pass
				else:
					i.send((USERNAME+":"+data).encode('utf-8'))	
			#Change their name if there is a '~' in front
			if "~" in data and userset == False:
				try:
					USERNAME = ("<"+data.replace("b'",'',1).replace("'",'').replace('~','',1)+">".replace(' ','',1))
					if USERNAME in ul:
						USERNAME = "<"+gethostbyaddr(addr[0])[0]+">"
						clientsock.send("<Alert> Username Taken. Reseting username to hostname...".encode("utf-8"))
					else:
						ul.append(USERNAME)
						i.send(("<"+gethostbyaddr(addr[0])[0]+">"+" has changed their username to "+USERNAME).encode('utf-8'))
						userset = True
				except:
					clientsock.send("<Alert> Error.".encode("utf-8"))

#Run server

if __name__=='__main__':
	ADDR = (HOST, PORT)
	serversock = socket(AF_INET, SOCK_STREAM)
	serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	serversock = ssl.wrap_socket(serversock, keyfile='cert.pem', certfile='cert.pem',server_side=True)
	serversock.bind(ADDR)
	serversock.listen(5)
	while 1:
		#Mainloop
		print('waiting for connection...')
		clientsock, addr = serversock.accept()
		print ('...connected from:', addr)
		thread.start_new_thread(handler, (clientsock, addr))