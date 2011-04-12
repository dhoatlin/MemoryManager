#!/usr/bin/python

import Tkinter, tkFileDialog
from Tkinter import *

def browse():
  file = tkFileDialog.askopenfile(parent=root, mode='rb',title='Choose a file')
  if file != None:
    data = file.read()
    file.close()
    print "I got %d bytes from this file." % len(data)
    loaded = True
    browseButton.config(state=DISABLED)

root = Tkinter.Tk()
frame = Frame(root, height=500, width=500)
frame.pack_propagate(0)
frame.pack()

#setup the menubar
menubar = Menu(root)
fileMenu = Menu(menubar, tearoff=0)
fileMenu.add_command(label='Load', command=browse)
fileMenu.add_separator()
fileMenu.add_command(label='Exit', command=root.quit)
menubar.add_cascade(label='File', menu=fileMenu)
root.config(menu=menubar)

browseButton = Button(frame, text='load', command=browse)
browseButton.pack()

mainloop()