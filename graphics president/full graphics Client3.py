import socket,pickle,time,os
import random
import pygame

from _thread import *
pygame.font.init()
global btns,messageToShow,x,y,roundsizebuttons,roundSize,message,myHand,autoUpdate,lastCardPlayed
lastCardPlayed = 0
autoUpdate = True
message = ""
roundsizebuttons = []

x = 0
y = 100
roundSize = 0
messageToShow = ""
btns = []
width = 1070
height = 700
background = pygame.image.load("images/background.jpg")
def getevents(win):
    global message
    while True:
        
        message = s.recv(2048).decode()
def displayMessage(text,x,y):
  font = pygame.font.SysFont("yugothicyugothicuisemiboldyugothicuibold", 40)
  text = font.render(text, 1, (255,255,255))
  pygame.draw.rect(win,(0,0,0),(x,y,100,100))
  pygame.draw.rect(win, (255,0,0), (x, y, text.get_width(), text.get_height()))
  
  win.blit(text,(x,y))
  
class Button:
    def __init__(self, text, x, y, color,value):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100
        self.value = value
    def draw(self, win):
        
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("yugothicyugothicuisemiboldyugothicuibold", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
class cardButton:
    def __init__(self,x, y,value):
        
        self.x = x
        self.y = y
        
        self.width = 69
        self.height = 94
        self.value = value
        self.image = pygame.image.load(r'images/' + str(value) + '-clubs.png') 
    def draw(self, win):
        win.blit(self.image,(self.x,self.y))
        #font = pygame.font.SysFont("comicsans", 40)
        #text = font.render(self.text, 1, (255,255,255))
        #win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
selectbuttons = [Button("Create a game", 450, 200, (255,0,0),"1"),Button("join a game", 450, 350, (255,0,0),"2")]
def joinscreen(win):
    onscreen = True
    code = " "
    while onscreen == True:
        mode = ""
        win.fill((0,0,0))
        displayMessage("code?",0,0)
        displayMessage(code,0,100)
        pygame.display.update()
        if code == "":
            code = " "
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
               
                if event.key != 13:
                    
                    gotchar = str(chr(event.key))
                    code = code + gotchar
                if event.key == pygame.K_BACKSPACE:
                    code = code[:-2]
                if event.key == 13:
                    code = code.replace(" ","")
                    return code
                #if event.key == pygame.K_ENTER:
                  #  return code
def setnamescreen(win):
    onscreen = True
    name = ""
    while onscreen == True:
        mode = ""
        win.fill((0,0,0))
        displayMessage("what is your name?",0,0)
        displayMessage(name,0,100)
        pygame.display.update()
        if name == "":
            name = " "
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                
                if event.key != 13:
                    
                    gotchar = str(chr(event.key))
                    name = name + gotchar
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-2]
                if event.key == 13:
                    name = name.replace(" ","",1)
                    return name
                #if event.key == pygame.K_ENTER:
                  #  return code

def createscreen(win):
    onscreen = True
    code = " "
    while onscreen == True:
        mode = ""
        win.fill((0,0,0))
        displayMessage("how many players?",0,0)
        displayMessage(code,0,100)
        pygame.display.update()
            
        pygame.display.update()
        if code == "":
            code = " "
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                
                if event.key != 13:
                    
                    gotchar = str(chr(event.key))
                    code = code + gotchar
                if event.key == pygame.K_BACKSPACE:
                    code = code[:-2]
                if event.key == 13:
                    code = code.replace(" ","")
                    return code
                #if event.key == pygame.K_ENTER:
                  #  return code


def mainscreen(win):
    win.fill((0,0,0))
    font = pygame.font.SysFont("yugothicyugothicuisemiboldyugothicuibold", 120)
    text = font.render("Online President", 1, (100,100,200))
    win.blit(text, (40,0))

    onscreen = True
    while onscreen == True:
        mode = ""
        
        for btn in selectbuttons:
            btn.draw(win)
            
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in selectbuttons:
                    if btn.click(pos):

                        mode = btn.value
                        if mode == "1":
                            return 1
                        if mode == "2":
                            return 2
           
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#name = input("what is your name: ")
#mode = int(input("what do you want to do? to Join a room: type 1, to start a room,type 2"))

lastCardPlayed = 0
myHand = []
highestset = 1
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
name = setnamescreen(win)
joinmode = mainscreen(win)
if joinmode == 1:
    size = createscreen(win)
    code = "startRoom"
    
    
    
    s.connect(("192.168.0.14",5555))
    s.send(str.encode(code + ":" + name + ":" + size))
if joinmode == 2:
    code = joinscreen(win)
    s.connect(("192.168.0.14",5555))
    
    s.send(str.encode(code + ":" + name))
start_new_thread(getevents,(win, ))
def countOccurrences(card,hand):
    count = 0
    for i in range(len(hand)):
        if hand[i] == card:
            count += 1
    return count
def playTurn(temp):
    global roundSize,lastCardPlayed,messageToShow,x,y,btns
    btns = []
    x = 0
    y = 100
    win.fill((0,0,0))
    hand = temp
    highestset = 0
    cardplaynumber = 0
    
    setlist = []
    for i in range(15):
        tempsetlistelement = countOccurrences(i,myHand)
        setlist.append(tempsetlistelement)
        setlist.sort()
        highestset = setlist[-1]
    displayMessage("your Turn",0,0)
    displayMessage(messageToShow,0,300)
    displayMessage("round size: " + str(roundSize),800,0)
    for i in range(len(hand)):
        btns.append(cardButton(x,y,hand[i]))
        
        x+=69
        try:
            if hand[i] != hand[i + 1]:
                x += 20
        except:
            pass
        if x > 1000:
            y += 94
            x = 0
    x = 0
    y = 100
    btns.append(Button("out", 250, 500, (255,0,0),"out"))
    for buttons in btns:
                buttons.draw(win)
    
    pygame.display.update()
    canplaycard = False
    card = 0
    while canplaycard == False:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos):
                        card = btn.value
        if card != "" and card != 0:
            if card == "out":
                return "out",lastCardPlayed
            if hand[-1] <= lastCardPlayed:
                return "out",lastCardPlayed
            if highestset < roundSize:
                return "out",lastCardPlayed
            
            if card != "out":
                card = int(card)
                cardplaynumber = countOccurrences(card,hand)
            if lastCardPlayed < card and cardplaynumber >= roundSize and card in hand:
                
                
                for i in range(roundSize):
                  hand.remove(card)
               
                canplaycard = True
                break
            if lastCardPlayed >= card:
                displayMessage("card too small",0,300)
                card = 0
    btns = []
    x = 0
    y = 100
    win.fill((0,0,0))
    for i in range(len(hand)):
        btns.append(cardButton(x,y,hand[i]))
        
        x+=69
        try:
            if hand[i] != hand[i + 1]:
                x += 20
        except:
            pass
        if x > 1000:
            y += 94
            x = 0
    x = 0
    y = 100
    for btn in btns:
        btn.draw(win)
    pygame.display.update()
    return hand,card
isNotOut = True

while True:
    win.fill((0,0,0))
    for buttons in btns:
        buttons.draw(win)
    displayMessage(messageToShow,0,300)
    displayMessage("round size: " + str(roundSize),800,0)
    pygame.display.update()
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    if message != "":
        
        instruction1 = message.split(":")
        message = ""
        instruction = instruction1[0]
        contents = instruction1[1]
        if instruction == "updateHand":
            myHand = []
            contents = contents.replace("[","")
            contents = contents.replace("]","")
            contents = contents.replace(" ","")
            contents = contents.split(",")
            for i in range(len(contents)):
                myHand.append(int(contents[i]))
            
            hand = myHand
            for i in range(len(hand)):
                btns.append(cardButton(x,y,hand[i]))
                
                x+=69
                try:
                    if hand[i] != hand[i + 1]:
                        x += 20
                except:
                    pass
                if x > 1000:
                    y += 94
                    x = 0
            x = 0
            y = 100
        if instruction == "setRoundSize":
            
            highestset = 0
            cardplaynumber = 0
            
            setlist = []
            for i in range(15):
                tempsetlistelement = countOccurrences(i,myHand)
                setlist.append(tempsetlistelement)
                setlist.sort()
                highestset = setlist[-1]
            
            
            cansetsize = False
            displayMessage("how many cards do u want to play? ",0,350)
            while cansetsize == False:
                
                 for i in range(highestset):
                    roundsizebuttons.append(Button(str(i + 1), x, y + 300, (255,0,0),i + 1))
                    x += 200
                 x = 0
                 for button in roundsizebuttons:
                     button.draw(win)
                 pygame.display.update()
                 temproundsize = 0
                 for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for btn in roundsizebuttons:
                            if btn.click(pos):
                                temproundsize = btn.value
                 if temproundsize <= highestset and temproundsize != 0:
                    roundSize = temproundsize
                    s.send(str.encode(str(roundSize)))
                    cansetsize = True
                    temproundsizebuttons = []
                    message = ""
                    pygame.display.update()
                   
        if instruction == "playTurn":
            
            contents = int(contents)
            roundSize = int(instruction1[2])
            lastCardPlayed = contents            
            playedmove, playedcard = playTurn(myHand)
            if playedmove != "out":
                myHand = playedmove
            s.send(str.encode("playedTurn:0"))
            time.sleep(1)
            s.send(pickle.dumps(playedmove))
            time.sleep(1)
            s.send(pickle.dumps(playedcard))
        if instruction == "displayMessage":
            for buttons in btns:
                    buttons.draw(win)
            messageToShow = contents
            
            
            
        if instruction == "goneOut":
            print("you have are " + "# " + contents)
