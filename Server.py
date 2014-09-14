from socket import *
import _thread as thread
import time

BUFF = 1024
HOST = '0.0.0.0'
PORT = 65000
list=[]
ul = []

def handler(clientsock,addr):
	joinnew = True
	list.append(clientsock)
	USERNAME = "<"+gethostbyaddr(addr[0])[0]+">"
	while 1:
		try:
			data = str(clientsock.recv(BUFF))
		except:
			list.pop(list.index(clientsock))
			if USERNAME != "<"+gethostbyaddr(addr[0])[0]+">":
				ul.pop(ul.index(USERNAME))
			break
		for i in list:
			if joinnew == True:
				i.send((USERNAME+" joined the server.").encode('utf-8'))
				joinnew = False
			repr(list)
			print('data:' + repr(data))
			repr(list)
			if not data:
				break
			if "~" not in data:
				i.send((USERNAME+":"+data).encode('utf-8'))	
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


if __name__=='__main__':
	ADDR = (HOST, PORT)
	serversock = socket(AF_INET, SOCK_STREAM)
	serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	serversock.bind(ADDR)
	serversock.listen(5)
	while 1:
		print('waiting for connection...')
		clientsock, addr = serversock.accept()
		print ('...connected from:', addr)
		thread.start_new_thread(handler, (clientsock, addr))