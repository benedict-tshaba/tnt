#/usr/bin/python

#-----------------------------------------------------------------------------#
# Name:        The Note Taker												  #
# Purpose:  To take regular day to day notes. 								  #
#																			  #
# Author:      Tshaba P.B   benedicttshaba@gmail.com 								  #
#																			  #
# Copyright:   (c) T.P.B 2016												  #
# Licence:     T.P.B Licence												  #
#-----------------------------------------------------------------------------#

import Tkinter as tnt
import tkMessageBox
import pickle
import sched, time

version = "1.2.1"
notes_file = "notes.tnt"

about_text = "Version: "+version+"\nThe Note Taker (TNT) is a simple notetaking program. \nCreated by\
 (c) Tshaba Phomolo Benedict"

usage_text = "How to use the program:\nYou enter your note in the text box on your left, when you are done you simply\
  type enter or click on the button named Enter.\nYour note should now appear in the listbox on your right. Then click the\
  button named Save to save your notes.\nWhen you double click your left mouse button your note is copied to the textbox.\
  when you double click a highlighted note with your right mouse button then you remove the note from the listbox.\nYou can\
  also click the Remove button to accomplish the same action.\nNotes are saved automatically every few minutes.\nThe Menu Bar:\
  \nThe Top left cascade named TNT has an Exit command which saves the notes and closes the program.\
  Next to it there is the edit menu with Remove and Prioritise. Prioritise moves your important notes/reminders to\
  the top of the list of notes. Remove will remove the highlighted note from the listbox. Remember to save afterwards.\
  The Date menu has an Add Date command which will add the current date and time to the textbox.\
  \nLast is the help menu which contains the about command and this Usage.\n"

root = tnt.Tk()
root.geometry("600x400")
root.title("The Note Taker")

def Enter():
	"""
	Takes text from the textbox and inserts it into the end of the listbox list of notes.
	Then is clears the textbox.
	"""
	text_contents = text.get(1.0, tnt.END)
	listbox.insert(tnt.END, text_contents)
	text.delete(1.0,tnt.END)

def Remove():
	"""
	Removes an (highlighted) entry from the list box.
	"""
	listbox.delete(tnt.ANCHOR)

def Save():
	"""
	Reads all the information currenlty on the listbox and saves them to a file.
	"""
	f = file(notes_file, "wb")
	notes = listbox.get(0, tnt.END)
	pickle.dump(notes, f)

def AutoSave():
	"""
	Calls Save() after every 60 seconds.
	"""
	Save()
	root.after(60000 * 1, AutoSave) # time in milliseconds we want to save stuff after 1 minute

def ReturnInsert(event):
	"""
	Event handler for the return key. Calls Enter.
	"""
	Enter()

def DeleteCurrent(event):
	"""
	Event handler for double right mouse click. Calls Remove.
	"""
	Remove()

def CopyToText(event):
	"""
	Event handler for left mouse click. Deletes whatever is currently in the textbox and
	replaces it with the highlighted note from the listbox.
	"""
	text.delete(1.0, tnt.END)
	current_note = listbox.get(tnt.ANCHOR)
	text.insert(1.0, current_note)

# Help menu commands
def about_command():
	label = tkMessageBox.showinfo("About", about_text)

def usage_command():
	label = tkMessageBox.showinfo("Usage", usage_text)

# End Help menu commands
# Edit menu commands 
def add_date_command():
	localtime = time.asctime( time.localtime( time.time() ) )
	strtime = str(localtime)
	text.insert(1.0,strtime)

def clear_command():
	listbox.delete(0,tnt.END)

def priori_command():
	priori_text = listbox.get(tnt.ANCHOR)
	listbox.delete(tnt.ANCHOR)
	listbox.insert(0, priori_text)

# End Edit menu commands

def exit_command():
	"""
	Ask for confirmation, if yes. Saves notes to the note list and quits.
	"""
	if tkMessageBox.askyesno("Quit", "Do you really want to quit?"):
		Save()
		root.destroy()

menubar = tnt.Menu(root)
# create pulldown menus, and add them to the menu bar
filemenu = tnt.Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=exit_command)
menubar.add_cascade(label="TNT ", menu=filemenu)
# edit menus
editmenu = tnt.Menu(menubar, tearoff=0)
editmenu.add_command(label="Clear All", command=clear_command)
editmenu.add_separator()
editmenu.add_command(label="Remove", command=Remove)
editmenu.add_separator()
editmenu.add_command(label="Prioritise", command=priori_command)
menubar.add_cascade(label="Edit", menu=editmenu)

# date menus
timemenu = tnt.Menu(menubar, tearoff=0)
timemenu.add_command(label="Add Date", command=add_date_command)
menubar.add_cascade(label="Date",menu=timemenu)
#help menus
helpmenu = tnt.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=about_command)
helpmenu.add_separator()
helpmenu.add_command(label="Usage", command=usage_command)
menubar.add_cascade(label="Help", menu=helpmenu)

# display the menu
root.config(menu=menubar)

textframe = tnt.Frame(root)
listframe = tnt.Frame(root)

#control buttons or action buttons.
enter_button = tnt.Button(textframe, text="Enter", command = Enter)
remove_button = tnt.Button(textframe, text="Remove", command = Remove)
save_button = tnt.Button(textframe, text="Save", command = Save)

text = tnt.Text(textframe,height=8,width=4)

scrollbar = tnt.Scrollbar(listframe, orient=tnt.VERTICAL)
sndscroll = tnt.Scrollbar(listframe, orient=tnt.HORIZONTAL)
listbox = tnt.Listbox(listframe, yscrollcommand=scrollbar.set, selectmode=tnt.EXTENDED)
listbox = tnt.Listbox(listframe, xscrollcommand=sndscroll.set, selectmode=tnt.EXTENDED)
scrollbar.configure(command=listbox.yview)
sndscroll.configure(command=listbox.xview)

text.bind("<Return>", ReturnInsert)
listbox.bind("<Double-Button-3>", DeleteCurrent)
listbox.bind("<Double-Button-1>", CopyToText)

text.pack(side=tnt.TOP, fill=tnt.BOTH, expand=1)
enter_button.pack(side=tnt.LEFT)
remove_button.pack(side=tnt.LEFT)
save_button.pack(side=tnt.LEFT)
sndscroll.pack(side=tnt.BOTTOM, fill=tnt.X)
listbox.pack(side=tnt.LEFT,fill=tnt.BOTH, expand=1)
scrollbar.pack(side=tnt.RIGHT, fill=tnt.Y)

textframe.pack(fill=tnt.BOTH,side=tnt.LEFT)
listframe.pack(fill=tnt.BOTH, expand=1,side=tnt.RIGHT)

try:
	f = file(notes_file, "rb")
	notes = pickle.load(f)
	for item in notes:
		listbox.insert(tnt.END,item)
	f.close()
except:
	pass

AutoSave()
root.mainloop()
