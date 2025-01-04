
"""
================================================================================================

                             Selective Interrogation Assessment Task
                                      Template Python Code

================================================================================================
                                                                
  Script Author: Amelia Reynolds
  Created: 08-10-2024 
  Edited: 04-01-2025
	  
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
    
    Please ensure all files are saved in the same location.   
  
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
    author, Amelia Reynolds, via email: arreynolds.research@gmail.com
"""

# Import Packages-------------------------------------

import os
import pygame
import csv
import random
from datetime import datetime

pygame.init()

# Global Variables------------------------------------

error = False

win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
winWidth, winHeight = win.get_size()

black = (0,0,0)
blue = (30,144,255)
green = (30,215,79)
red = (220,20,60)
white = (255,255,255)

taskInfo = {
    # id info
    'date':datetime.now().strftime("%Y-%m-%d"), 
    'time':datetime.now().strftime("%H:%M:%S"), 
    'subject':None, 
    # stimuli
    'activeGrid': None, 
    'activeCategory': None, 
    'activeLabel': None, 
    'activeContent': None, 
    # latencies
    'latencyLabel': 0,
    'latencyContent': 0
}

# Basic Functions-------------------------------------

def loadText(path):
    global promptText, error, errorText
    promptText = {}
    try:
        with open(path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                promptText[row['Key']] = row['Text']
        return promptText
    except FileNotFoundError:
        print(f"Error: File {path} not found.")
        error = True
        errorText = (f"Error: {path} file not found, unable to load task prompts. Please ensure the {path} file is saved in the same location as Python script.")
   
def drawButton(text, x, y, size, color, bold, buttoncolor):
        global win, winWidth, winHeight
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
        return button

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
    
# Event Handling-------------------------------------

def handleEvent():
    global running, clickPos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left mouse button
                clickPos = pygame.mouse.get_pos()
                return True
    return False

def updateInfo(key,value):
    global taskInfo, stimList, gridCount, startTime, clickTime
    taskInfo[key] = value
    if key == 'activeLabel':
         for row in stimList:
             if row[1] == value:
                taskInfo['activeGrid'] = gridCount
                taskInfo['activeCategory'] = row[0]
                taskInfo['activeContent'] = row[2]
                taskInfo['latencyLabel'] = int((clickTime.timestamp()-startTime.timestamp())*1000)
                break

def updateCount():
    global subsetIndex, subsetTotal, clickCount, gridCount
    subsetIndex += subsetTotal
    clickCount = 0
    gridCount += 1

# Task Stimuli----------------------------------------

def createStim(path):
    global stimList, stimTotal, subsetTotal, categoryDict, categoryCount, categoryTotal, labelList, error, errorText
    # initialise global variables
    stimList = []
    stimTotal = 0
    categoryDict = {}
    categoryCount = {} 
    subsetTotal = 16
    try: # read in stimuli from csv
        with open(path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                category = int(row[1])
                if category not in categoryDict:
                    categoryDict[category] = []
                stimulus = (category,row[2],row[3])
                categoryDict[category].append(stimulus)
        for category, stimuli in categoryDict.items():
            random.shuffle(stimuli)
            categoryCount[category] = len(stimuli)
        categoryTotal = len(categoryDict)
        subsetCount = subsetTotal // categoryTotal
        for i in range(0, min(len(stimuli) for stimuli in categoryDict.values()), subsetCount):
            batch = [] 
            for category, stimuli in categoryDict.items():
                batch.extend(stimuli[i:i+subsetCount])
                random.shuffle(batch)
                stimList.extend(batch)
        labelList = [stimulus[1] for stimulus in stimList] 
        stimTotal = len(labelList)
    except FileNotFoundError: 
        print(f"Error: File {path} not found.")
        error = True
        errorText = (f"Error: {path} file not found, unable to load task stimuli. Please ensure the {path} file is saved in the same location as Python script.")

def subsetStim():
    global subsetTotal, subsetIndex, labelList, gridList, gridCount, clickCount, running
    
    if subsetIndex >= len(labelList):
        runAlert(promptText['End_Alert'],2500)
        running = False

    else:
        runAlert(promptText['Grid_Alert'],2500)
        gridStim = labelList[subsetIndex:(subsetIndex+subsetTotal)]
        gridPos = []
        xPos = [int(winWidth*0.2), int(winWidth*0.4), int(winWidth*0.6), int(winWidth*0.8)]
        yPos = [int(winHeight*0.25), int(winHeight*0.45), int(winHeight*0.65), int(winHeight*0.85)]
        for y in yPos:
            for x in xPos:
                gridPos.append((x,y))
                gridList = []
                for pos, label in zip(gridPos, gridStim):
                    font = pygame.font.SysFont('Calibri', int(winHeight*0.025), False)
                    labelText = font.render(label, True, (0, 0, 0)) 
                    labelTextbox = labelText.get_rect(center=(pos))
                    gridList.append((label, labelText, labelTextbox))
        updateCount()
        
# Task Loops------------------------------------------

def runIntro(path):
    global promptText, button
    win.fill(white)
    drawText(promptText['Instructions_Title'],0.5,0.15,0.04,black,True)
    wrapText(promptText['Instructions_Body'],0.5,0.25,0.03,black,False,0.75)
    button = drawButton('Start Task',0.5,0.8,0.03,white,True,green)
    pygame.display.update()

def runAlert(text, duration):
    win.fill(white) 
    drawText(text,0.5,0.5,0.03,black,True)
    pygame.display.update() 
    pygame.time.delay(duration)

def runGrid():
    global clickCount, promptText, gridList, button
    button = []
    # create display
    win.fill(white)
    vLines = [int(winWidth*0.3), int(winWidth*0.5), int(winWidth*0.7)]  
    hLines = [int(winHeight*0.35), int(winHeight*0.55), int(winHeight*0.75)] 
    for x in vLines:
        pygame.draw.line(win,black,(x, int(winHeight*0.15)), (x, int(winHeight*0.95)),1)
    for y in hLines:
        pygame.draw.line(win,black,(int(winWidth*0.1), y), (int(winWidth*0.9), y),1)
    for label, labelText, labelTextbox in gridList:
            win.blit(labelText, labelTextbox)
    drawText(promptText['Grid_Prompt'],0.5,0.08,0.025,black,True)
    # update display
    pygame.display.update()

def runContent():
    global taskInfo, promptText, button
    win.fill(white)
    drawText(taskInfo['activeContent'],0.5,0.45,0.03,black,False)
    button = drawButton(promptText['Continue_Button'],0.5,0.8,0.025,white,True,blue)
    pygame.display.update()

def runError():
    global errorText, button
    win.fill(white) 
    drawText('( "• ᴖ •) Uh oh!',0.5,0.4,0.04,black,True)
    wrapText(errorText,0.5,0.45,0.028,black,False,0.45)
    button = drawButton('Exit Task',0.5,0.8,0.03,white,True,red)
    pygame.display.update() 

# Data Output---------------------------------------

def createID(path):
    usedid = set()
    try:
        with open(path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) > 2 and row[2].strip().isdigit():
                    usedid.add(int(row[2]))
    except FileNotFoundError:
        pass  
    
    while True:
        newid = random.randint(100000, 999999)
        if newid not in usedid:
            updateInfo('subject', newid)
            return newid

def dataRaw(path):
    global taskInfo
    head = [
        "startDate",
        "startTime",
        "subject",
        "gridNum",
        "categoryNum", 
        "labelStim",
        "labelLatency", 
        "contentStim",
        "contentLatency"
        ]
    if not os.path.exists(path):
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(head)
    with open(path, 'a', newline='') as file:
        data = [
            # subject id
            taskInfo['date'],
            taskInfo['time'],
            taskInfo['subject'],
            # item id
            taskInfo['activeGrid'],
            taskInfo['activeCategory'],
            # label stimulus
            taskInfo['activeLabel'],
            taskInfo['latencyLabel'],
            # content stimulus
            taskInfo['activeContent'],
            taskInfo['latencyContent']
            ]
        writer = csv.writer(file)
        writer.writerow(data)

def createDat():
    global stimTotal, subsetTotal, gridTotal, taskInfo, categoryDict, dataDict
    gridTotal = stimTotal // subsetTotal
    dataDict = {}
    dataDict['startDate'] = taskInfo.get('date', '')
    dataDict['startTime'] = taskInfo.get('time', '')
    dataDict['subject'] = taskInfo.get('subject', '')
    for grid in range(1,gridTotal-1):
        for category in categoryDict:
            keySubtotal = f"Grid{grid}_Category{category}_Subtotal"
            dataDict[keySubtotal] = 0
    for category in categoryDict:
        # Create a key for the grand total of each category
        keyTotal = f"Category{category}_Total"
        dataDict[keyTotal] = 0

def updateDat():
    global taskInfo, dataDict
    activeGrid = taskInfo.get('activeGrid')
    activeCategory = taskInfo.get('activeCategory')
    if activeGrid is not None and activeCategory is not None:
        subtotalKey = f"Grid{activeGrid}_Category{activeCategory}_Subtotal"
        totalKey = f"Category{activeCategory}_Total"
    if subtotalKey in dataDict:
        dataDict[subtotalKey] += 1 
    if totalKey in dataDict:
        dataDict[totalKey] = sum(value for key, value in dataDict.items() if key.endswith(f"Category{activeCategory}_Subtotal"))
    return dataDict

def dataDat(path):
    global dataDict
    head = list(dataDict.keys())
    if not os.path.exists(path):
        with open(path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(head)  
    with open(path, 'a', newline='') as file:
        writer = csv.writer(file)
        data = [dataDict[key] for key in head]
        writer.writerow(data)

# Run Task--------------------------------------

# file paths
stimFile = 'SelectIntTask_Stimuli.csv'
txtFile = 'SelectIntTask_Instructions.csv'
rawFile = 'SelectIntTask_RawData.csv'
datFile = 'SelectIntTask_SummaryData.csv'

# task set up
loadText(txtFile)
createStim(stimFile)
createID(datFile)
createDat()

# run conditions
running = True
state = 'intro'

while running:

    if state == 'intro': # intro loop
        if error:
            runError()
            click = handleEvent()
            if click:
                if button.collidepoint(clickPos):
                    running = False
        runIntro(txtFile)
        click = handleEvent()
        if click: 
            if button.collidepoint(clickPos):
                # initialise counters
                gridCount = 0 
                subsetIndex = 0
                clickCount = 8
                # run grid loop
                startTime = datetime.now()
                state = 'grid'
    
    elif state == 'grid': # grid loop
        if clickCount == 8:
            subsetStim()
        runGrid()
        click = handleEvent()
        if click:
            for label, labelText, labelTextbox in gridList:
                if labelTextbox.collidepoint(clickPos):
                            clickTime = datetime.now()
                            updateInfo('activeLabel',label)
                            gridList.remove((label,labelText,labelTextbox))
                            clickCount += 1
                            startTime = datetime.now()
                            state = 'content'
    
    elif state == 'content': # content loop
        runContent()
        click = handleEvent()
        if click: 
            if button.collidepoint(clickPos):
                clickTime = datetime.now()
                updateInfo('latencyContent',int((clickTime.timestamp()-startTime.timestamp())*1000))
                dataRaw(rawFile)
                updateDat()
                state = 'grid'

dataDat(datFile)

pygame.quit()
