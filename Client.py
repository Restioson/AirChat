import socket
import tkinter.simpledialog
from tkinter import *
import _thread as thread
import sys, os, time
import tkinter.messagebox

s = socket.socket()
master = Tk()
master.withdraw()
while True:
	try:
		ip = tkinter.simpledialog.askstring('ChatServer','Enter the ChatServer IP:')
		s.connect((ip,65000))
		break
	except:
		tkinter.messagebox.showerror("ConnectError","Can't connect!")
		ss = tkinter.messagebox.askyesno("Runtime Error","Would you like to exit?")
		if ss == True:
			sys.exit(0)


master.update()
master.deiconify()
p=print
p("Setting title...")
master.wm_title("AirChat 1.2")
def key(event):
	print("pressed", repr(event.char))

def listen(bytes,ARG):

	while True:
		p("listening...")
		try:
			DAT = str(s.recv(bytes))
			DAT = DAT.replace("'","").replace("b","",2).replace('"',"")
			DAT = DAT.replace('"',"")
			text.config(state=NORMAL)
			text.insert(END,DAT)
			text.insert(END,"\n")
			text.config(state=DISABLED)
			print(DAT)

		except socket.error:
			tkinter.messagebox.showerror("Disconnected","The server has crashed or been shut down")
			quitclient = tkinter.messagebox.askyesno("Runtime Error","Would you like to exit?")
			if quitclient == False:
				try:
					os.system('python Client.py')
					sys.exit(0)
				except:
					tkinter.messagebox.showerror("Operation Failed","Could not restart client")
					time.sleep(10)
					sys.exit(0)

			if quitclient == True:
				sys.exit(0)

		#Do something with the data

def callback():
	s.send(E1.get().encode('utf-8'))
	E1.delete(0, END)

b = Button(master, text="Send Message to Chat Room", command=callback,bd =4)
b.pack(fill=X)

E1 = Entry(master, bd =5)
E1.pack(side = BOTTOM,fill=X)

text=Text(master,bd = 5)
text.config(state=DISABLED)
text.pack(side=LEFT,fill=BOTH)

scrl = Scrollbar(master, command=text.yview,orient=VERTICAL,bd = 3)
scrl.pack(side=RIGHT,fill=BOTH)

text.config(yscrollcommand=scrl.set)
print("connect!")

Name = tkinter.simpledialog.askstring('Username','Enter your username here:')
s.send(("~"+Name).encode('utf-8'))
print("Done...")
p(s.getpeername())

thread.start_new_thread(listen, (1024, ''))

mainloop()