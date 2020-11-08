import socket,pickle,time,os
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
name = input("what is your name: ")
mode = int(input("what do you want to do? to Join a room: type 1, to start a room,type 2"))
if mode == 1:
    
    
    code = input("code: ")
    s.connect(("ip adress goes here",5555))
    s.send(str.encode(code + ":" + name))
if mode == 2:
    code = "startRoom"
    size = input("how many players?: ")
    
    s.connect(("------------------",5555))
    s.send(str.encode(code + ":" + name + ":" + size))
global myHand,lastCardPlayed,roundSize,cardplaynumber,highestset
lasrtCardPlayed = 0
myHand = []
highestset = 1
def countOccurrences(card,hand):
    count = 0
    for i in range(len(hand)):
        if hand[i] == card:
            count += 1
    return count
def playTurn(temp):
    
    hand = temp
    
    if lastCardPlayed > hand[-1]:
        return "out",lastCardPlayed
    card = 0
    canplaycard = False
    while canplaycard == False:
        
        card = input("which card would you like to play? your hand is " + str(hand))
        
            
        if card == "out":
            return "out",lastCardPlayed
        
        if card != "out":
            card = int(card)
            cardplaynumber = countOccurrences(card,hand)
        if lastCardPlayed < card and cardplaynumber >= roundSize and card in hand:
            
            
            for i in range(roundSize):
                hand.remove(card)
            
            canplaycard = True
            break
        print(cardplaynumber)
        if lastCardPlayed >= card or cardplaynumber < roundSize:

        
            print("card too small")
    
    return hand,card
isNotOut = True
while True:
    message = s.recv(2048).decode()
    instruction1 = message.split(":")
    instruction = instruction1[0]
    contents = instruction1[1]
    if instruction == "updateHand":
        contents = contents.replace("[","")
        contents = contents.replace("]","")
        contents = contents.replace(" ","")
        contents = contents.split(",")
        for i in range(len(contents)):
            myHand.append(int(contents[i]))
        print(myHand)
    if instruction == "setRoundSize":
        
        highestset = 0
        cardplaynumber = 0
        
        setlist = []
        for i in range(15):
            tempsetlistelement = countOccurrences(i,myHand)
            setlist.append(tempsetlistelement)
            setlist.sort()
            highestset = setlist[-1]
        print(highestset)
        
        cansetsize = False
        while cansetsize == False:
            print(myHand)
            temproundsize = int(input("how many cards would you like to play?:"))
            if isinstance(temproundsize,int):
                
                if temproundsize <= highestset and temproundsize < 5:
                    roundSize = temproundsize
                    starter = [-1]
                    cansetsize = True
                    s.send(str.encode(str(roundSize)))
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
        print(contents)
    if instruction == "goneOut":
        print("you have are " + "# " + contents)
