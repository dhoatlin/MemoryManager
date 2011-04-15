#!/usr/bin/python

from Tkinter import *
from tkFileDialog import *
import math

#line numbers
currentLine = 1.0
totalLines = 0

#page/frame size
pageSize = 512.0

#colors
available = '#82FF86'
taken = '#FF4F4F'

#physical pages
pageFrames = []

#all paging tables
pagingTables = {}


'''------------------------------------------
Defining function to be used during execution
------------------------------------------'''

'''
Browse function for loading a file, uses tkinter library
'''
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
    
    #disbale writing to textbox enable next button
    inputbox.config(state=DISABLED)
    outputbox.config(state=DISABLED)
    nextButton.config(state=NORMAL)

'''
Function for the next button

Tracks which line the program is on and updates the ouputbox/paging frames
'''
def nextStep():
  global currentLine, totalLines
  
  #enable writing to output box
  outputbox.config(state=NORMAL)
    
  if currentLine <= totalLines:
    #grab next line from input box and write to output box
    inputLine = inputbox.get(currentLine, currentLine+1)
    outputbox.insert(END, '==>' + inputLine)
    
    #parse input line to brief description of what is happening
    output = parseInput(inputLine)
    outputbox.insert(END, output)
    
    #update current line
    currentLine += 1.0
  else:
    outputbox.insert(END, 'End of simulation')
    nextButton.config(state=DISABLED)
    
  #disable output box
  outputbox.config(state=DISABLED)

  '''
  #for debugging: show every process paging table
  keys = pagingTables.keys()
  keys.sort()
  for key in keys:
    for i in range(len(pagingTables[key])):
      print 'pid: ' + key + ' ' + str(pagingTables[key][i])
    print '----------------------'
  print '********************'
  '''
  '''
  #for debugging: show contents of every frame
  for page in pageFrames:
    print page
  print '*****************************'
  '''

'''
Removes a process from it's frames

after removal, it checks to see if there are any waiting processes
'''

def removeProgram(inputs):
  for i in range(len(pageFrames)):
    if pageFrames[i]['pid'] == inputs['pid']:
      pageFrames[i]['avail'] = True
      pageFrames[i]['label'].config(bg=available, text='Free')
      pageFrames[i]['pid'] = 'N/A'
  #sort keys to follow FIFO
  keys = pagingTables.keys()
  keys.sort()
  for key in keys:
    for i in range(len(pagingTables[key])):
      if pagingTables[key][i]['status'] == 'waiting':
        enough = checkAvailSpace(len(pagingTables[key]))
        if enough:
          addPhysicalLocation(key, True)
  
'''
loads a process into it's frames

initializes new process page tables
'''
def loadProgram(inputs):
  total = inputs['codeSize'] + inputs['dataSize']
  enough = checkAvailSpace(total)
  #enough room -> add paging table to program
  if enough:
    initPageTable(inputs['pid'], total, 'running', inputs['codeSize'])
      
    #add physical location
    addPhysicalLocation(inputs['pid'], False)
        
  else:
    initPageTable(inputs['pid'], total, 'waiting', inputs['codeSize'])


'''
builds a new paging table without a physical location yet
'''
def initPageTable(pid, total, status, codeTotal):
  pagingTables[pid] = []
  count = 0
  for i in range(total):
    if count < codeTotal:
      pagingTables[pid].append({'type': 'code', 'logical': str(i), 'status': status})
      count += 1
    else:
      pagingTables[pid].append({'type': 'data', 'logical':str(i), 'status': status})

'''
adds the physical address to the page table
'''
def addPhysicalLocation(pid, restore):
  for page in pagingTables[pid]:
    for i in range(len(pageFrames)):
      if(pageFrames[i]['avail']):
        page['physical'] = str(i)
        if restore:
          page['status'] = 'running'
        labelText = page['type'] + '-' + page['logical'] + ' of P' + pid
        pageFrames[i]['label'].config(bg=taken, text=labelText)
        pageFrames[i]['avail'] = False
        pageFrames[i]['pid'] = pid
        break

'''
checks if there is enough frames for a new process

returns true if space is available
'''
def checkAvailSpace(total):
  found = 0
  enough = False
  for i in range(len(pageFrames)):
    if pageFrames[i]['avail']:
      found += 1
    if found == total:
      enough = True
      break
  return enough  

'''
parses a line from the inputbox

loads and removes programs where needed
prints to output box some information about a new program
'''
def parseInput(inputLine):
  global pageSize
  splitInput = inputLine.split()
  pid = splitInput[0]
  if splitInput[1] == '-1':
    output = 'End of program ' + pid + '\n'
    removeProgram({'pid': pid})
  else:
    code = splitInput[1]
    codePages = int(math.ceil(int(code) / pageSize))
    data = splitInput[2]
    dataPages = int(math.ceil(int(data) / pageSize))
    output = 'Loading program ' + pid + ' into RAM: code=' + code + '(' + str(codePages) + ' page(s))' + ', data=' + data + '(' + str(dataPages) + ' page(s))' + '\n'
    loadProgram({'pid': pid, 'codeSize': codePages, 'dataSize': dataPages})
  return output

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
for i in range(8):
  newLabel = Label(memFrame, text='Free', height=3, width=20, bg=available, relief=SUNKEN)
  newLabel.grid(row=i)
  pageFrames.append({'label': newLabel, 'avail': True, 'pid': 'N/A'})

#create output frame
outputFrame = Frame(root)
outputbox = Text(outputFrame, height = 20, width=70, state=DISABLED)
outScrollbar = Scrollbar(outputFrame)
outScrollbar.pack(side=RIGHT, fill=Y)
outputbox.pack()
outScrollbar.config(command=outputbox.yview)
outputbox.config(yscrollcommand=outScrollbar.set)

#create next button for stepping through
nextButton = Button(root, text='next', command=nextStep, state=DISABLED)

#place frames in grid layout
inputFrame.grid(row=0, column=0, sticky=N)
nextButton.grid(row=1, column=0)
memFrame.grid(row=0, column=1, rowspan=2)
outputFrame.grid(row=0, column=2, sticky=N)


'''------------------------------
Start tkinter's event driven loop
------------------------------'''
mainloop()