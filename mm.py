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

#making sure window isnt created under any system menu bars like OS X
root.geometry('+50+50')


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
memFrame = Frame(root, height=400, width=150, bg='#525252')

pageFrames = []
for i in range(8):
  #newFrame = Frame(memFrame, height=40, width=120, bg='#8C80FF')
  newLabel = Label(memFrame, text='Free', height=3, width=20, bg='#8C80FF')
  newLabel.grid(row=i)
  #newFrame.grid(row=i, column=0)
  #pageFrames.append([newFrame, newLabel])
  pageFrames.append(newLabel)


#create output frame
outputFrame = Frame(root)
outputbox = Text(outputFrame, height = 20, width=60, state=DISABLED)
outScrollbar = Scrollbar(outputFrame)
outScrollbar.pack(side=RIGHT, fill=Y)
outputbox.pack()
outScrollbar.config(command=outputbox.yview)
outputbox.config(yscrollcommand=outScrollbar.set)

#place frames in grid layout
inputFrame.grid(row=0, column=0, sticky=N)
memFrame.grid(row=0, column=1)
outputFrame.grid(row=0, column=2, sticky=N)

mainloop()