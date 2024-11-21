
"""
================================================================================================

                             Selective Interrogation Assessment Task
                                      Template Python Code

================================================================================================
                                                                
  Script Author: Amelia Reynolds
  Created: 08-10-2024 
  Edited: 21-11-2024
	  
  Task Information .............................................................................
		 
    This is an editable code for the Selective Interrogation Assessment Task. This task 
    assesses selective interrogation of information, that is, the information an individual 
    volitionally accesses from a pool of available information. The task permits computation 
    indices representing the relative proportions of categories of information selectively 
    interrogated by each participant.
 
  Requirements ..................................................................................
 
    Software
    (1) Python Programming Language
    (2) The Pygame Library
    
    Files
    (1) SelectiveIntTask_Code.py
    (2) SelectIntTask_Stimuli.csv
    (2) SelectIntTask_Instructions.txt
    
    Please ensure all files are saved in the same location, and file names are not changed.   
  
  Task Citation ..................................................................................
 
    Reynolds, A., MacLeod, C., & Grafton, B. (2024). The role of expectancies and selective
    interrogation of information in trait anxiety-linked affect when approaching potentially
    stressful future events. Behaviour Research and Therapy.
    doi.org/10.1016/j.brat.2024.104568 
  
  MIT License .................................................................................... 
  
    Copyright (c) 2024 Amelia Reynolds
    
    Permission is hereby granted, free of charge, to any person obtaining a copy of this 
    software and associated documentation files (the "Software"), to deal in the Software
    without restriction, including without limitation the rights to use, copy, modify, merge,
    publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons 
    to whom the Software is furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all copies or 
    substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
    INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
    PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE 
    FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
    OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
    DEALINGS IN THE SOFTWARE.

  Contact Details ..............................................................................
		 
    For additional information, error reporting, and coding assistance, please contact the 
    author, Amelia Reynolds, via email: amelia.reynolds@research.uwa.edu.au
"""
#-----------------------------------Import Packages-------------------------------------

# packages
import sys
import os
import csv
from csv import writer # import module to write in csv file
import pygame 
import random  # to generate random numbers
from datetime import datetime, timedelta  # for timestamp

# libraries   
pygame.init()

#-----------------------------------Global Variables-----------------------------------

# file paths
stimFile = 'SelectIntTask_Stimuli.csv'
rawFile = 'SelectIntTask_RawData.csv'
dataFile = 'SelectIntTask_SummaryData.csv'

# experiment info
expInfo = {
    'date':datetime.now().strftime("%Y-%m-%d"), # current date
    'time':datetime.now().strftime("%H:%M:%S"), # current time
    'subject':None, # subject number
    # grid 1 scores
    "grid1Category1":0,
    "grid1Category2":0,
    "grid1BiasIndex":0,
    # grid 2 scores
    "grid2Category1":0,
    "grid2Category2":0,
    "grid2BiasIndex":0,
    # grid 3 scores
    "grid3Category1":0,
    "grid3Category2":0,
    "grid3BiasIndex":0,
    # grid 4 scores
    "grid4Category1":0,
    "grid4Category2":0,
    "grid4BiasIndex":0,
    # total scores
    'totalCategory1': 0,
    'totalCategory2': 0,
    'totalBiasIndex': 0
}

# experiment window
win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # set window size
winWidth, winHeight = win.get_size() # store width and height

# aesthetics
black = (0,0,0)
blue = (30,144,255)
green = (30,215,79)
red = (220,20,60)
white = (255,255,255)

# responses 
button = [] # initialise list to store clickable buttons 

#----------------------------------Define Functions-------------------------------------

def updateGlobal(key, value, path): # update expInfo dictionary and global variables
    global expInfo
    expInfo[key] = value
    globals()[key] = value
    updateSumData(path)  # update CSV file with new values

def createRawData(path): # long format data file (1 row per label selected) 
    if os.path.exists(path):
        pass
    if not os.path.exists(path): # if does not exist, create raw data file
        header = [ 
            "dateStart", # date subject commenced experiment
            "timeStart", # time subject commenced experiment
            "subjectID", # subject id number
            "gridNum",   # grid number
            "selectCategory", # category of selected label
            "selectLabel", # selected label stimulus
            "selectLatency", # latency of label selection
            "viewContent", # corresponding content stimulus
            "viewLatency" # latentcy of content viewing
            ]
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)

def createSumData(path): # wide format summary data file (1 row per subject)
    if os.path.exists(path):
        pass
    if not os.path.exists(path): # if does not exist, create summary data file
        header = [ 
            "dateStart", # date subject commenced experiment
            "timeStart", # time subject commenced experiment
            "subjectID", # subject id number
            "grid1Category1",
            "grid1Category2",
            "grid1BiasIndex",
            "grid2Category1",
            "grid2Category2",
            "grid2BiasIndex",
            "grid3Category1",
            "grid3Category2",
            "grid3BiasIndex",
            "grid4Category1",
            "grid4Category2",
            "grid4BiasIndex",
            "totalCategory1",
            "totalCategory2",
            "totalBiasIndex"
            ]
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)

def uniqueSubject():
    usedid = set()
    try:
        with open(rawFile, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            for row in reader:
                # ensure row[2] exists and is not empty 
                if len(row) > 2 and row[2].strip().isdigit():
                    usedid.add(int(row[2]))
    except FileNotFoundError:
        pass  # if file doesn't exist,generate new ID

    while True:
        newid = random.randint(100000, 999999)
        if newid not in usedid:
            updateGlobal('subject', newid, dataFile)
            return newid

def updateRawData(path,subject,value):
    if not os.path.exists(path):
        createSumData(path)  # ensure the raw file exists before appending
    # initialise lists 
    rows = []
    # read file and update new row
    with open(path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[2] == str(subject) and row[-1] == "N/A":  
                row[-1] = value  
            rows.append(row)
    # write updated row into raw data file 
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def updateSumData(path):
    
    # check summary data file exists 
    if not os.path.exists(path):
        createSumData(path) # create file, if needed  
    
    # check if subject id has existing data
    subjectid = False
    rows = []
    with open(path, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader) 
        for i, row in enumerate(rows):
            if row[2] == str(expInfo['subject']):  # match subject ID
                updatedRow = [expInfo[key] for key in expInfo]
                rows[i] = updatedRow
                subjectid = True
                break

    # if subject id does not have existing data, append a new row
    if not subjectid:
        newRow = [expInfo[key] for key in expInfo]
        rows.append(newRow)

    # write updated rows back to csv
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def drawText(text, x, y, size, color, bold):
        global win, winWidth, winHeight
        text = str(text)
        font = pygame.font.SysFont('Calibri', int(winHeight*size), bold)
        text = font.render(text, True, color)
        textbox = text.get_rect(center=(int(winWidth*x), int(winHeight*y)))
        win.blit(text, textbox)

def wrapText(text, x, y, size, color, bold, wrapwidth):
    global win, winWidth, winHeight
    text = str(text)
    font = pygame.font.SysFont('Calibri', int(winHeight * size), bold)
    maxWidth = int(winWidth*wrapwidth) # set max width 
    # initialise variables 
    offsetLine = 0.02
    paragraphs = text.split('\n') 
    # loop through each paragraph
    for paragraph in paragraphs:
        words = paragraph.split(' ')
        lines = []
        currentLine = ""
        currentWidth = 0
        # loop over words, wrapping as needed
        for word in words:
            wordText = font.render(word, True, color)
            wordWidth, wordHeight = wordText.get_size()
            # If adding the word would exceed the maximum width, wrap to a new line
            if currentWidth + wordWidth >= maxWidth:
                lines.append(currentLine)  # save current line
                currentLine = word + " "   # start new line 
                currentWidth = wordWidth + font.size(" ")[0]  # reset width
            else:
                currentLine += word + " "  # add word to line
                currentWidth += wordWidth + font.size(" ")[0]  # update width
        # add line to paragraph
        if currentLine:
            lines.append(currentLine)
        # render each line of paragraph
        for line in lines:
            lineText = font.render(line, True, color)
            line_rect = lineText.get_rect(center=(int(winWidth * x), int(winHeight * (y + offsetLine))))
            win.blit(lineText, line_rect)
            offsetLine += size  # move to next line
        # add extra space paragraphs
        offsetLine += size  

def drawButton(text, x, y, size, color, bold, buttoncolor):
        global win, winWidth, winHeight, button
        text = str(text)
        if bold == True:
            font = pygame.font.SysFont('Calibri', int(winHeight * size), True)
        elif bold == False:
            font = pygame.font.SysFont('Calibri', int(winHeight * size), False)
        text = font.render(text, True, color)
        textbox = text.get_rect(center=(int(winWidth*x), int(winHeight*y)))
        padding = 15  # Add some padding around the text
        button = pygame.Rect(
            textbox.left - padding,
            textbox.top - padding,
            textbox.width + 2 * padding,
            textbox.height + 2 * padding
            )
        pygame.draw.rect(win, buttoncolor, button, border_radius = 12)
        win.blit(text, textbox)
        return (button)

#-----------------------------------Generate Stimuli------------------------------------

# initialise global stimuli lists
Stim = []  # stimuli (category, label, content) list
category1Stim = [] # initialise list for category 1 stimuli 
category2Stim = [] # initialise list for category 2 stimuli 

with open(stimFile, mode='r') as file: # read csv
    reader = csv.reader(file)
    next(reader)  # skip header row
    for row in reader:
        category = int(row[1]) # index of category column
        stimulus = (category,row[2],row[3])  # index of label and content columns
        if category == 1: # separate stimuli based on category
            category1Stim.append(stimulus)
        elif category == 2:
            category2Stim.append(stimulus)

random.shuffle(category1Stim) #shuffle stimuli (label, content) in category 1
random.shuffle(category2Stim) #shuffle stimuli (label, content) in category 2

for i in range(0, min(len(category1Stim), len(category2Stim)), 8): #ensure for every 16 there are 8 of each category
    batch = category1Stim[i:i+8] + category2Stim[i:i+8]  # 8 from each category
    random.shuffle(batch)  # Shuffle the batch
    Stim.extend(batch)

labelStim = [stimulus[1] for stimulus in Stim] # extract labels from shuffled list


#------------------Task Instructions------------------

def displayInstruct(): # display instruction page function
    win.fill(white)
    # create instructions heading
    drawText('Task Instructions',0.5,0.15,0.04,black,True)
    # create instructions body 
    with open('SelectIntTask_Instructions.txt', mode='r') as instruct: # read from txt file
         wrapText(instruct.read(),0.5,0.25,0.03,black,False,0.75)
    # create continue button
    drawButton('Start Task',0.5,0.8,0.03,white,True,green)
    # display instruction page
    pygame.display.update() # update display
    return button

def displayAlert(alert, duration):
    win.fill(white)  # background
    drawText(alert,0.5,0.45,0.03,black,True)
    pygame.display.update()  # update display
    pygame.time.delay(duration)

#------------------Task Trials------------------

# initialise counters
gridCount = 0 # initialise grid counter
clickCount = 8 # initialise click counter
subsetCount = 16 # define number of labels on each grid
subsetIndex = 0 # track current index of label subset

# initialise lsits
gridPos = [] # possible grid positions
labelPos = [] # labels and assigned positions 
selectedLabel = []  # selected labels
selectedCategory = []  # selected category
selectedContent = []  # selected content

def subsetStim(gridPos):
    global gridCount, clickCount, subsetCount, subsetIndex, labelStim, labelPos
    if subsetIndex >= len(labelStim):
        displayAlert('This is the end of the task. The program will now end automatically.',3000)
        running = False  # end if no more labels
        pygame.quit()
    else:
        gridStim = labelStim[subsetIndex:(subsetIndex+subsetCount)] # select subset
        labelPos = [] # initialise new list
        for pos, label in zip(gridPos, gridStim):
            font = pygame.font.SysFont('Calibri', int(winHeight*0.025), False)
            labelText = font.render(label, True, (0, 0, 0))  # render label text
            labelTextbox = labelText.get_rect(center=(pos))
            labelPos.append((label, labelText, labelTextbox)) # store (label, position)
        subsetIndex += subsetCount
        clickCount = 0 # reset click counter
        gridCount += 1 # increment grid counter
    return labelPos

# display grid
def displayGrid():
    global clickCount
    if run_Grid == False:
        pass
    else:
        # generate grid partition
        vLines = [int(winWidth*0.3), int(winWidth*0.5), int(winWidth*0.7)]  # x positions for vertical lines
        hLines = [int(winHeight*0.25), int(winHeight*0.45), int(winHeight*0.65)] # y positions for horizontal lines
        xPos = [int(winWidth*0.2), int(winWidth*0.4), int(winWidth*0.6), int(winWidth*0.8)]
        yPos = [int(winHeight*0.15), int(winHeight*0.35), int(winHeight*0.55), int(winHeight*0.75)]
        # assign grid positions 
        for y in yPos:
            for x in xPos:
                gridPos.append((x, y))
        if clickCount >= 8: # check if new label subset required
            subsetStim(gridPos) # run subsetting function
            displayAlert('New information will now be made available.', 2500)
        # draw grid partition
        win.fill(white)
        for x in vLines:
            pygame.draw.line(win,black,(x, int(winHeight*0.05)), (x, int(winHeight*0.85)),1)
        for y in hLines:
            pygame.draw.line(win,black,(int(winWidth*0.1), y), (int(winWidth*0.9), y),1)
        for label, labelText, labelTextbox in labelPos:
            win.blit(labelText, labelTextbox)
        drawText('Please select a label to continue.',0.5,0.92,0.025,black,True)
        # display grid
        pygame.display.update() # update display
    return labelPos

#------------------Run Task------------------


# define run conditions
running = True
run_Instructions = True
run_Grid = False
run_Content = False

# initialise timer
timer = pygame.time.Clock()

# assign subject id
uniqueSubject()

while running:

    # set event listeners
    for event in pygame.event.get():
        
        # keyboard event
        if event.type == pygame.KEYDOWN: # check for key press events
            if event.key == pygame.K_ESCAPE: # esc key
                print("Esc key pressed")
                running = False
                pygame.quit()
        
        # mouse event
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left mouse button
                clickPos = pygame.mouse.get_pos()
                
                # for instructions run
                if run_Instructions:
                     if button.collidepoint(clickPos):
                        run_Instructions = False
                        run_Grid = True
                
                # for grid run
                if run_Grid:
                     for label, labelText, labelTextbox in labelPos:
                        if labelTextbox.collidepoint(clickPos):
                            
                            # record latency
                            clickTime = datetime.now()
                            clickLatency = int((clickTime.timestamp()-startTime.timestamp())*1000) # latency in milliseconds

                            # record response
                            selectedLabel.append(label)  
                            labelPos.remove((label,labelText,labelTextbox))
                            clickCount += 1
                            
                            # record data
                            for row in Stim:
                                if row[1] == label:

                                    # define relevant values   
                                    category = int(row[0])
                                    content = row[2]
                                    keyCategory1 = f'grid{gridCount}Category1'
                                    keyCategory2 = f'grid{gridCount}Category2'
                                    keyBiasIndex = f'grid{gridCount}BiasIndex' 
                                    
                                    # increment summary data selection counts
                                    if category == 1: 
                                        updateGlobal('totalCategory1',int(expInfo['totalCategory1'])+1,dataFile)
                                        updateGlobal(keyCategory1, int(expInfo[keyCategory1]) + 1, dataFile)
                                    if category == 2:
                                        updateGlobal('totalCategory2',int(expInfo['totalCategory2'])+1,dataFile) 
                                        updateGlobal(keyCategory2, int(expInfo[keyCategory2]) + 1, dataFile)
                                    
                                    # update summary data bias index scores
                                    updateGlobal('totalBiasIndex',(int(expInfo['totalCategory1'])/(int(expInfo['totalCategory1'])+int(expInfo['totalCategory2']))),dataFile)
                                    updateGlobal(keyBiasIndex, expInfo[keyCategory1]/(expInfo[keyCategory1]+expInfo[keyCategory2]), dataFile)

                                    # update raw data
                                    with open(rawFile, 'a', newline='') as file: 
                                        rawdata = [
                                            expInfo['date'],
                                            expInfo['time'],
                                            expInfo['subject'],
                                            gridCount,
                                            category,
                                            label,
                                            clickLatency,
                                            content,
                                            "N/A"] # raw data
                                        writer = csv.writer(file)
                                        writer.writerow(rawdata)   
                                    break
                                else:
                                    content = 'Error: No matching content found.'
                            
                            # view content
                            run_Grid = False
                            run_Content = True
                            startTime = datetime.now()
                            win.fill(white)
                            wrapText(content,0.5,0.4,0.03,black,False,0.75)
                            drawButton('Continue',0.5,0.8,0.025,white,True,blue)
                            pygame.display.update() 

                
                # for content run
                if run_Content:
                    if button.collidepoint(clickPos):
                        # latency tracking
                        viewTime = datetime.now()
                        viewLatency = int((viewTime.timestamp()-startTime.timestamp())*1000)
                        updateRawData(rawFile,expInfo['subject'],viewLatency)
                        #view grid
                        run_Content = False
                        run_Grid = True
    
    # during instructions run
    if run_Instructions:
         button = displayInstruct()  # display instructions
    
    # during instructions run
    if run_Grid:
        startTime = datetime.now()
        labelPos = displayGrid()  # display grid  
