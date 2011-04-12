#!/usr/bin/python

from Tkinter import *
from tkFileDialog import *

#browse function for loading a file
def browse():
  file = askopenfile(parent=root, mode='rb',title='Choose a file')
  if file != None:
    #enable writing to textbox
    inputbox.config(state=NORMAL)
    
    #write file to textbox
    for line in file:
      inputbox.insert(END, line)
    file.close()
    
    #disbale writing to textbox
    inputbox.config(state=DISABLED)

#create the main window
root = Tk()
root.title('Memory Manager - Dave Hoatlin')


#setup the menubar
menubar = Menu(root)
fileMenu = Menu(menubar, tearoff=0)
fileMenu.add_command(label='Load', command=browse)
fileMenu.add_separator()
fileMenu.add_command(label='Exit', command=root.quit)
menubar.add_cascade(label='File', menu=fileMenu)
root.config(menu=menubar)

#creating a textbox
inputFrame = Frame(root)
inputbox = Text(inputFrame, height=10, width=30, state=DISABLED)
scrollbar = Scrollbar(inputFrame)
scrollbar.pack(side=RIGHT, fill=Y)
inputbox.pack()
scrollbar.config(command=inputbox.yview)
inputbox.config(yscrollcommand=scrollbar.set)

#create memory frame
memFrame = Frame(root, height=300, width=100)

#create output frame
outputFrame = Frame(root)
outputbox = Text(outputFrame, height = 20, width=80, state=DISABLED)
outputbox.pack()

#place frames in grid layout
inputFrame.grid(row=0, column=0)
memFrame.grid(row=0, column=1)
outputFrame.grid(row=0, column=2)

mainloop()