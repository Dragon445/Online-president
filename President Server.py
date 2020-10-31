#code by Ethan Brammah for an online card game of president.uses only baisic libraries. i cant spell btw
from _thread import*
import socket
import random
import time
import string
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
def id_generator(size=6, chars=string.digits):#room id genorator
            return ''.join(random.choice(chars) for x in range(size))
s.bind(("192.168.0.17",5555))#creates server
s.listen(100)
import pickle
global rooms#room storage veriable, rooms are stored as classes under keys of their ids
# game function
def playGame(roomid):
        
    while rooms[roomid].playable == False:
       try:
            
                
            if rooms[roomid].players == 1:
                broadcast("displayMessage:game over.",rooms[roomid].roomid)
                break
            if rooms[roomid].turn in rooms[roomid].canPlay:
                
            
                if rooms[roomid].playable == False:
                    playedcard = 0
                    playedmove = []
                    if rooms[roomid].starter == rooms[roomid].turn:
                        rooms[roomid].canPlayConn[rooms[roomid].turn].send(str.encode("setRoundSize:0"))
                        rooms[roomid].roundSize = rooms[roomid].canPlayConn[rooms[roomid].turn].recv(2048).decode()
                        rooms[roomid].starter = -1
                        broadcast("displayMessage:"+ rooms[roomid].playerNames[rooms[roomid].turn] + " has set the round size to " + str(rooms[roomid].roundSize),rooms[roomid].roomid)
                        
                    if len(rooms[roomid].playersHands[rooms[roomid].turn]) != 0:         
                        rooms[roomid].canPlayConn[rooms[roomid].turn].send(str.encode("playTurn:" + str(rooms[roomid].lastCardPlayed) + ":" + str(rooms[roomid].roundSize)))
                        move = rooms[roomid].canPlayConn[rooms[roomid].turn].recv(2048).decode()
                        splitmove = move.split(":")
                        if splitmove[0] == "playedTurn":
                            playedmove = pickle.loads(rooms[roomid].canPlayConn[rooms[roomid].turn].recv(2048))
                            
                            playedcard = pickle.loads(rooms[roomid].canPlayConn[rooms[roomid].turn].recv(2048))
                            if playedmove == "out":
                                rooms[roomid].canPlay.remove(rooms[roomid].turn)
                                
                                broadcast("displayMessage:" + rooms[roomid].playerNames[rooms[roomid].turn] +" is out",rooms[roomid].roomid)
                            
                            rooms[roomid].playersHands[rooms[roomid].turn] = playedmove
                            rooms[roomid].lastCardPlayed = playedcard
                            if len(playedmove) == 0:
                                rooms[roomid].players -= 1
                                rooms[roomid].canPlay = []
                                rooms[roomid].canPlayConn[rooms[roomid].turn].send(str.encode("goneOut:" + str(rooms[roomid].winners)))
                                
                                
                                broadcast("displayMessage:" + rooms[roomid].playerNames[rooms[roomid].turn] + " has got rid of all their cards. they are #" + str(rooms[roomid].winners) + ". they have" + str(len(playedmove)) + " cards left",rooms[roomid].roomid)
                                rooms[roomid].goneOut.append(rooms[roomid].turn)
                                del rooms[roomid].canPlayConn[rooms[roomid].turn]
                                del rooms[roomid].playerNames[rooms[roomid].turn]
                                del rooms[roomid].playersHands[rooms[roomid].turn]#stops this player from playing again. inelgennt and horrible but it works
                               
                                rooms[roomid].winners += 1
                                rooms[roomid].lastCardPlayed = 0
                                rooms[roomid].roundSize = 0
                                rooms[roomid].starter = rooms[roomid].turn
                                rooms[roomid].winners += 1
                                for i in range(rooms[roomid].players):
                                    
                                    rooms[roomid].canPlay.append(i)
                                if rooms[roomid].turn == rooms[roomid]. players:
                                    turn = 0
                                continue
                                
                            if playedmove != "out":
                                broadcast("displayMessage:" + rooms[roomid].playerNames[rooms[roomid].turn] + " has played a " + str(playedcard) + ". they have" + str(len(playedmove)) + " cards left",rooms[roomid].roomid)
                
                            if rooms[roomid].lastCardPlayed != 14 and len(rooms[roomid].canPlay) != 1 or len(playedmove) == 0:
                                rooms[roomid].turn += 1
                            if rooms[roomid].lastCardPlayed == 14:
                                 rooms[roomid].canPlay = []
                                 rooms[roomid].starter = rooms[roomid].turn
                                 for i in range(rooms[roomid].players):
                                    
                                    rooms[roomid].canPlay.append(i)
                                 broadcast("displayMessage:" + rooms[roomid].playerNames[rooms[roomid].turn] +" won this round. they now start",rooms[roomid].roomid)
                                 
                                 rooms[roomid].lastCardPlayed = 0
                            if len(rooms[roomid].canPlay) == 1:
                                rooms[roomid].turn = rooms[roomid].canPlay[-1]
                                broadcast("displayMessage:" + rooms[roomid].playerNames[rooms[roomid].turn] +" won this round. they now start",rooms[roomid].roomid)
                                rooms[roomid].starter = rooms[roomid].turn
                                rooms[roomid].canPlay = []
                                rooms[roomid].lastCardPlayed = 0
                                for i in range(rooms[roomid].players):
                                    
                                    rooms[roomid].canPlay.append(i)
                            if rooms[roomid].turn == rooms[roomid].players:
                                rooms[roomid].turn = 0
            else:
                if rooms[roomid].turn != len(rooms[roomid].canPlay):
                    rooms[roomid].turn += 1#if player has gone out make it the next players turn
                if rooms[roomid].turn == len(rooms[roomid].canPlay):
                    rooms[roomid].turn = 0
        except:
            del rooms[roomid].connList[rooms[roomid].turn]
            broadcast("displayMessage:someone has left this game or an error has occured. this room is being terminated",roomid)
            del rooms[roomid]#if there is an error or someone leaves this room is deleted
            break
def broadcast(message,roomid):
    #send a message to all clients within a secific room
    for o in range(len(rooms.get(roomid).connList)):
        rooms.get(roomid).connList[o].send(str.encode(message + "\n"))
    time.sleep(0.2)
def playTurn(temp,lastcard):#unused function, this is used in the client to play turns
            lastCardPlayed = lastcard
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
                if lastCardPlayed < card:
                    
                    
                    for i in range(len(hand)):
                        if hand[i] == card:
                            del hand[i]
                            
                            canplaycard = True
                            break
                if lastCardPlayed >= card:
                    print("card too small")
            return hand,card
class Client:#room client, stores all the information required to play, along with the dealing algorythms and a function to join this room
    def __init__(self,players,roomid):
        self.lastCardPlayed = 0
        self.roomid = roomid
        self.playerNames = []
        self.playersHands,self.playersList,self.canPlay = self.shuffleDeal(players)
        self.connList = []
        self.roundSize = 1
        self.playable = False
        self.tempPlayerHands = {}
        self.canPlayConn = []
        self.turn = 0
        self.starter = 0
        self.winners = 1
        self.players = players
        self.onlineList = []
        self.goneOut = []
    def shuffleDeal(self,players):
        self.lastCardPlayed = 1
       
        temphand = []
        
        playersHands = []
        playersHands = []
        playersList = []
        canPlay = []
        cards = [
                2,2,2,2,
                3,3,3,3,
                4,4,4,4,
                5,5,5,5,
                6,6,6,6,
                7,7,7,7,
                8,8,8,8,
                9,9,9,9,
                10,10,10,10,
                11,11,11,11,
                12,12,12,12,
                13,13,13,13,
                14,14,14,14]
        cards = [2,2,2,3,3,3,4,4,4,5,5,5,6,6,6]
        cards2 = cards

        for i in range(players):
            playersHands.append([])
            canPlay.append(i)

        person = 0
        for i in range(len(cards2)):

            if person == players:
              person = 0

            if len(cards2) == 0:
              break


            card = random.choice(cards2)
            cards2.remove(card)

            playersHands[person].append(card)
           
            person += 1

        for o in range(players):
            
            temphand = playersHands[o]
            temphand.sort()
            
            
        return playersHands,playersList,canPlay
    def joinRoom(self,conn,name):
        conn.send(str.encode("updateHand:" + str(self.playersHands[len(self.connList)])))
        self.canPlayConn.append(conn)
        self.connList.append(conn)
        self.playerNames.append(name)
        
rooms = {"123456":Client(2,"123456"),"654321":Client(2,"654321")}#couple of pre-defined rooms for testing


while True:
    conn,addr = s.accept()
    instruction = conn.recv(2048).decode()
    instruction = instruction.split(":")
    

    if instruction[0] == "startRoom":#if client requests to create a room, create a custom code and create a room instance in the rooms dictionary under that key
        newroomid = id_generator()
        size = int(instruction[2])
        rooms[newroomid] = Client(size,newroomid)
        conn.send(str.encode("displayMessage:your room code is " + str(newroomid)))
        rooms[newroomid].joinRoom(conn,instruction[1])
        rooms[newroomid].onlineList.append(instruction[1])
        continue
    if instruction[0] in rooms:
        rooms[instruction[0]].joinRoom(conn,instruction[1])#join a room with the id provided
        
        rooms[instruction[0]].onlineList.append(instruction[1])
        broadcast("displayMessage: " + instruction[1] + " joined the game",instruction[0])#alert everyone in that room whos joined
        broadcast("displayMessage:online players; " + str(rooms[instruction[0]].onlineList),instruction[0])
        if len(rooms[instruction[0]].connList) == rooms[instruction[0]].players:
            start_new_thread(playGame, (instruction[0], ))
            
    if instruction[0] not in rooms and instruction[0] != "startRoom":
        conn.send(str.encode("displayMessage:game not found, reload client and try again"))
        conn.close()
