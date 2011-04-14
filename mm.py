#!/usr/bin/python

from Tkinter import *
from tkFileDialog import *

#line numbers
currentLine = 1.0
totalLines = 0

#colors
available = '#82FF86'
taken = '#FF4F4F'

'''------------------------------------------
Defining function to be used during execution
------------------------------------------'''

#browse function for loading a file
def browse():
  global currentLine, totalLines
  file = askopenfile(parent=root, mode='rb',title='Choose a file')
  if file != None:
    #enable writing to textbox
    inputbox.config(state=NORMAL)
    outputbox.config(state=NORMAL)
    #delete old data from textboxes
    inputbox.delete(1.0, END)
    outputbox.delete(1.0, END)
    
    #write file to textbox
    totalLines = 0
    currentLine = 1.0
    for line in file:
      inputbox.insert(END, line)
      totalLines += 1
    file.close()
    
    #disbale writing to textbox
    inputbox.config(state=DISABLED)
    outputbox.config(state=DISABLED)
    
def nextStep():
  global currentLine, totalLines
  if currentLine <= totalLines:
    outputbox.config(state=NORMAL)
    inputLine = '==>' + inputbox.get(currentLine, currentLine+1)
    outputbox.insert(END, inputLine)
    outputbox.config(state=DISABLED)
    currentLine += 1.0
    process()
    
def process():
  outputbox.config(state=NORMAL)
  outputbox.insert(END, 'processing\n')
  outputbox.config(state=DISABLED)

'''---------------------------
Creating the GUI using tkinter
---------------------------'''



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
inputbox = Text(inputFrame, height=20, width=30, state=DISABLED)
scrollbar = Scrollbar(inputFrame)
scrollbar.pack(side=RIGHT, fill=Y)
inputbox.pack()
scrollbar.config(command=inputbox.yview)
inputbox.config(yscrollcommand=scrollbar.set)

#create memory frame
memFrame = Frame(root)
pageFrames = []
for i in range(8):
  newLabel = Label(memFrame, text='Free', height=3, width=20, bg=available, relief=SUNKEN)
  newLabel.grid(row=i)
  pageFrames.append(newLabel)

#create output frame
outputFrame = Frame(root)
outputbox = Text(outputFrame, height = 20, width=60, state=DISABLED)
outScrollbar = Scrollbar(outputFrame)
outScrollbar.pack(side=RIGHT, fill=Y)
outputbox.pack()
outScrollbar.config(command=outputbox.yview)
outputbox.config(yscrollcommand=outScrollbar.set)

#create next button for stepping through
nextButton = Button(root, text='next', command=nextStep)

#place frames in grid layout
inputFrame.grid(row=0, column=0, sticky=N)
nextButton.grid(row=1, column=0)
memFrame.grid(row=0, column=1, rowspan=2)
outputFrame.grid(row=0, column=2, sticky=N)


'''------------------------------
Start tkinter's event driven loop
------------------------------'''
mainloop()