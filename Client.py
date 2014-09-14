#Client for Airchat


#Imports
import socket
import tkinter.simpledialog
from tkinter import *
import _thread as thread
import sys, os, time
import tkinter.messagebox

#Create a socket
s = socket.socket()

#Create (and hide) a TK window
master = Tk()
master.withdraw()

#Try to connect to the server
while True:
	try:
		ip = tkinter.simpledialog.askstring('ChatServer','Enter the ChatServer IP:')
		s.connect((ip,65000)) #Connect to the server on port 65000
		break
	except:
		tkinter.messagebox.showerror("ConnectError","Can't connect!") #Cannot connect, reconnect or exit?
		ss = tkinter.messagebox.askyesno("Runtime Error","Would you like to exit?")
		if ss == True:
			sys.exit(0) #Exit
		
		else:
			pass #Reconnect

#Show the TK window
master.update()
master.deiconify()

#Shorten print() to p()
p=print

#Set the title of the TK window
p("Setting title...")
master.wm_title("AirChat 1.2")

#Define the handler
def listen(bytes,ARG):
	while True:
		p("listening...")
		DAT = str(s.recv(bytes))
		DAT = DAT.replace("'","").replace("b","",2).replace('"',"")
		DAT = DAT.replace('"',"")
		text.config(state=NORMAL)
		text.insert(END,DAT)
		text.insert(END,"\n")
		text.config(state=DISABLED)
		print(DAT)

#Define the "send" button's function
def callback(event):
	s.send(event.widget.get().encode('utf-8'))
	E1.delete(0, END)

#Create an entry widget to enter the chat text into
E1 = Entry(master, bd =5)
#Press enter to send text
E1.bind('<Return>', callback)
E1.pack(side = BOTTOM,fill=X)

#Create the panel of text where the chat will be shown
text=Text(master,bd = 5)
text.config(state=DISABLED)
text.pack(side=LEFT,fill=BOTH)

#Create a scrollbar for the text window
scrl = Scrollbar(master, command=text.yview,orient=VERTICAL,bd = 3)
scrl.pack(side=RIGHT,fill=BOTH)

text.config(yscrollcommand=scrl.set)
print("connect!")

#Ask the user for their username
Name = tkinter.simpledialog.askstring('Username','Enter your username here:')

#Send it to the server
s.send(("~"+Name).encode('utf-8'))
print("Done...")

#Get the server's address and details
p(s.getpeername())

#Start listening for chat
thread.start_new_thread(listen, (1024, ''))

#Run the client!
mainloop()