#Client for Airchat


#Imports
import socket, ssl
import tkinter.simpledialog
from tkinter import *
import _thread as thread
import sys, os, time
import tkinter.messagebox

#Credit to Bryan Oakley@http://stackoverflow.com/questions/3781670/tkinter-text-highlighting-in-python for the CustomText class

class CustomText(Text):
	'''A text widget with a new method, HighlightPattern 

	example:

	text = CustomText()
	text.tag_configure("red",foreground="#ff0000")
	text.HighlightPattern("this should be red", "red")

	The highlight_pattern method is a simplified python 
	version of the tcl code at http://wiki.tcl.tk/3246
	'''
	def __init__(self, *args, **kwargs):
		Text.__init__(self, *args, **kwargs)

	def highlight_pattern(self, pattern, tag, start="1.0", end="end", regexp=False):
		'''Apply the given tag to all text that matches the given pattern

		If 'regexp' is set to True, pattern will be treated as a regular expression
		'''

		start = self.index(start)
		end = self.index(end)
		self.mark_set("matchStart",start)
		self.mark_set("matchEnd",start)
		self.mark_set("searchLimit", end)

		count = IntVar()
		while True:
			index = self.search(pattern, "matchEnd","searchLimit",count=count, regexp=regexp)
			if index == "": 
				break
			self.mark_set("matchStart", index)
			self.mark_set("matchEnd", "%s+%sc" % (index,count.get()))
			self.tag_add(tag, "matchStart","matchEnd")

#Create a socket
s = socket.socket()
s = ssl.wrap_socket(s)

#Create (and hide) a TK window
master = Tk()
master.withdraw()


#Set the title of the TK window
print("Setting title...")
master.wm_title("AirChat 1.2")


#Define the handler
def listen(bytes,ARG):
	p('listening for data...')
	while True:
		DAT = str(s.recv(bytes))
		DAT = DAT.replace("'","").replace("b","",2).replace('"',"").replace("""\\\\""","""\"""")
		DAT = DAT.replace('"',"")
		if DAT == "<Alert> Username Taken. Reseting username to hostname...":
			pass
		text.config(state=NORMAL)
		text.insert(END,DAT)
		text.insert(END,"\n")
		text.highlight_pattern("(<.*?>)", "usrname",regexp=True)
		text.highlight_pattern("(<Alert>)","alert",regexp=True)
		text.config(state=DISABLED)

#Define the "send" button's function
def callback(event):
	s.send(event.widget.get().encode('utf-8'))
	text.config(state=NORMAL)
	text.insert(END, "<You> "+event.widget.get())
	text.insert(END,'\n')
	text.highlight_pattern("<You> "+event.widget.get(),"owntext")
	text.config(state=DISABLED)
	E1.delete(0, END)

#Define the function to connect to the server
def Connect():
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

def GetUser():
	Name = tkinter.simpledialog.askstring('Username','Enter your username here:')

	#Send it to the server
	s.send(("~"+Name).encode('utf-8'))
	print("Done...")

def PackWidgets(textW, scrlW, EntryW):
	textW.pack(side=LEFT, fill=BOTH)
	scrlW.pack(side=Right, fill=BOTH)
	EntryW.pack(side=Bottom, fill=X)
	
def RunApp(root, textWidget, scrlWidget, entryWidget):
	Connect() #Connect to server
	GetUser() #Get username
	PackWidgets(textWidget, scrlWidget, entryWidget) #Pack the widgets
	#Show the window and run the app!
	root.update()
	root.deiconify()
	thread.start_new_thread(listen, (1024, ''))
	root.mainloop()

#Create an entry widget to enter the chat text into
E1 = Entry(master, bd =5)
#Press enter to send text
E1.bind('<Return>', callback)

#Create the panel of text where the chat will be shown
text= CustomText(master,bd = 5, font="Calibri")
text.config(state=DISABLED)

#Create a scrollbar for the text window
scrl = Scrollbar(master, command=text.yview,orient=VERTICAL,bd = 3)
text.config(yscrollcommand=scrl.set)

print("connect!")

#Define some colours
text.tag_configure("usrname", foreground = "#00CC00")
text.tag_configure("alert", foreground = "#B80000")
text.tag_configure("owntext", foreground = "#363636")

RunApp(master, text, scrl, E1)

