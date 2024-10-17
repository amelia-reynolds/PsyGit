
"""
================================================================================================

                             Selective Interrogation Assessment Task
                                      Template Python Code

================================================================================================
                                                                
  Script Author: Amelia Reynolds (amelia.reynolds@research.uwa.edu.au)
  Created: 08-10-2024 
  Edited: 17-10-2024
	  
Task Information .............................................................................
		 
This is a beta version of an editable code for the Selective Interrogation Assessment
Task developed by Reynolds et al. (2024). This task assesses selective interrogation 
of information, that is, the information an individual volitionally accesses from a pool 
of available information. The task permits computation indices representing the relative 
proportions of categories of information selectively interrogated by each participant.

Please be aware, this version does not currently produce a data file. 
  
Citation .....................................................................................
 
Reynolds, A., MacLeod, C., & Grafton, B. (2024). The role of expectancies and selective
interrogation of information in trait anxiety-linked affect when approaching potentially
stressful future events. Behaviour Research and Therapy.
doi.org/10.1016/j.brat.2024.104568 

Contact Details ..............................................................................
		 
For additional information, error reported, or assistance, please contact the author, 
Amelia Reynolds @ amelia.reynolds@research.uwa.edu.au
"""
#-----------------------------------Import Packages-----------------------------------

# import packages
import sys
import os
import pygame
import random  # import the random module for generating random numbers
from datetime import datetime  # import datetime for timestamp
import csv

# initialize pygame
pygame.init()

#-----------------------------------Global Variables-----------------------------------

# window
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

# experiment info
expInfo = {
    'subject': f"{random.randint(0, 999999):06.0f}",  # random subject number
    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

#----------------------------------Basic Functions-------------------------------------

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

with open('SelectIntTask_Stimuli.csv', mode='r') as file: # read csv
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
selectedStim = []  # selected labels

def subsetStim(gridPos):
    global gridCount, clickCount, subsetCount, subsetIndex, labelStim, labelPos
    subsetIndex += subsetCount
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
            displayAlert('New information will now be made available', 2500)
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

# before experiment
# # insert datafile generation function here

# set run conditions
running = True
run_Instructions = True
run_Grid = False
run_Content = False

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
                            
                            selectedStim.append(label)  # store selected label
                            print(f"Selected:{label}")
                            labelPos.remove((label,labelText,labelTextbox))
                            clickCount += 1
                            
                            # assign corresponding content
                            for row in Stim:
                                if row[1] == label:  # check if the label matches
                                    content = row[2]  # get the string from the third column
                                    print(f"Selected:{content}")
                                    break
                                else:
                                    content = 'Error: No matching content found.'
                            
                            run_Grid = False
                            run_Content = True
                            # draw content screen
                            win.fill(white)
                            wrapText(content,0.5,0.4,0.03,black,False,0.75)
                            drawButton('Continue',0.5,0.8,0.025,white,True,blue)
                            pygame.display.update() # update display

                
                # for content run
                if run_Content:
                    if button.collidepoint(clickPos):
                        run_Content = False
                        run_Grid = True
    
    # during instructions run
    if run_Instructions:
         button = displayInstruct()  # display instructions
    
    # during instructions run
    if run_Grid:
         labelPos = displayGrid()  # display instructions  
