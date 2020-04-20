# -*- coding: utf-8 -*-
import re, struct, random, time

__author__ = "Derek"
__date__ = "$7/06/2017 13:10:00$"

class Utility:
    def __init__(this, client, server):
        this.client = client
        this.isCommand = False
        this.lastObjID = 0
        this.canExplosion = False
        this.isFireworks = False
        this.conjX = 0
        this.conjY = 0

    def spawnObj(this, objID, posX, posY, angle):
        itemID = random.randint(100, 999)
        objID = int(objID)
        posX = int(posX)
        posY = int(posY)
        data = struct.pack("!ihhhhhbb", itemID, objID, posX, posY, angle, 0, 1, 0)        
        this.client.room.sendAll([5, 20], data)
        this.lastObjID = struct.unpack("!i", data[:4])[0]        

    def removeObj(this):
        this.client.sendPacket([4, 8], struct.pack("!i?", this.lastObjID, True))

    def playerWin(this):
        timeTaken = int((time.time() - (this.client.playerStartTimeMillis if this.client.room.autoRespawn else this.client.room.gameStartTimeMillis)) * 100)
        place = this.client.room.numCompleted
        if place == 0:
            place = place + 1
        this.client.sendPlayerWin(place, timeTaken)

    def buildConj(this):
        if this.isFireworks == True:
            this.client.sendPacket([4, 14], [int(this.conjX), int(this.conjY)])    

    def removeConj(this):
        if this.isFireworks == True:
            this.client.sendPacket([4, 15], [int(this.conjX), int(this.conjY)])

    def newCoordsConj(this):
        this.conjX = random.randint(0, 79)
        this.conjY = random.randint(2, 39)

    def explosionPlayer(this, posX, posY):
        data = struct.pack("!h", int(posX))
        data += "\x00\x842"
        data += struct.pack("!h?", int(posY), True)
        this.client.sendPacket([5, 17], data)
    
    def moreSettings(this, setting):
        if setting == "giveAdmin":
            if not this.client.playerName in this.client.room.adminsRoom:
                this.client.room.adminsRoom.append(this.client.playerName)

        elif setting == "join":
            this.sendMessage("<J>Welcome to #utility!")
            this.consoleChat(1, "", ""+str(this.client.playerName)+" joined the room.")
            this.client.sendPacket([29, 20], "\x00\x00\x1c\x16\x00t<font color=\'#000000\'><p align=\'center\'><b><font size=\'128\' face=\'Soopafresh,Verdana\'>#utility</font></b></p></font>\x00_\x00d\x02X\x00\xc8\x002FP\x00\x00\x00\x00\x00\x01")
            this.client.sendPacket([29, 20], "\x00\x00\x1c{\x00t<font color=\'#000000\'><p align=\'center\'><b><font size=\'128\' face=\'Soopafresh,Verdana\'>#utility</font></b></p></font>\x00i\x00d\x02X\x00\xc8\x002FP\x00\x00\x00\x00\x00\x01")
            this.client.sendPacket([29, 20], "\x00\x00\x1c\xe0\x00t<font color=\'#000000\'><p align=\'center\'><b><font size=\'128\' face=\'Soopafresh,Verdana\'>#utility</font></b></p></font>\x00d\x00_\x02X\x00\xc8\x002FP\x00\x00\x00\x00\x00\x01")
            this.client.sendPacket([29, 20], "\x00\x00\x1dE\x00t<font color=\'#000000\'><p align=\'center\'><b><font size=\'128\' face=\'Soopafresh,Verdana\'>#utility</font></b></p></font>\x00d\x00i\x02X\x00\xc8\x002FP\x00\x00\x00\x00\x00\x01")
            this.client.sendPacket([29, 20], "\xff\xff\xff\xed\x00W<p align=\'center\'><b><font size=\'128\' face=\'Soopafresh,Verdana\'>#utility</font></b></p>\x00d\x00d\x02X\x00\xc8\x002FP\x00\x00\x00\x00\x00\x01")
            this.client.sendPacket([29, 20], "\xff\xff\xff\xf0\x00\x80<p align=\'center\'><a href=\'event:info' target='_blank'><b>?</b></a></p>\x00\x05\x00\x1c\x00\x10\x00\x10\x002FP\x002FPd\x00")
            this.client.sendPacket([29, 20], "\xff\xff\xff\xef\x00><p align=\'center\'><a href=\'event:info\'><b><i>i</i></b></a></p>\x00!\x00\x1c\x00\x10\x00\x10\x002FP\x002FPd\x00")            
    
        elif setting == "removePopups":        
            popupID = [7190, 7291, 7392, 7493, -19]
            for id in popupID:
                this.removePopups(id)        

    def removePopups(this, popupID):
        this.client.sendPacket([29, 22], struct.pack("!i", popupID))
            
    def consoleChat(this, type, username, message):
        for client in this.client.room.clients.values():
            if client.playerName in this.client.room.adminsRoom:                
                if type == 1:
                    prefix = "<font color='#AAAAAA'>Ξ [Utility] "
                elif type == 2:
                    prefix = "<font color='#AAAAAA'>Ξ ["+str(username)+"] "

                message = prefix + message 
                
                client.sendPacket([6, 9], struct.pack("!h", len(message)) + message)

    def sendMessage(this, message):
        this.client.sendPacket([6, 9], struct.pack("!h", len(message)) + message)

    def staffChat(this, username, message):
        for client in this.client.room.clients.values():
            if client.playerName in this.client.room.adminsRoom:
                prefix = "<font color='#00FFFF'>Ξ ["+str(username)+"] "
                client.Utility.sendMessage(prefix + message + "</font>")
    
    def sentCommand(this, command):
        command = command[1:]
        if command == "admins":
            this.consoleChat(2, this.client.playerName, "!" + command)
            admins = ', '.join(this.client.room.adminsRoom)
            this.sendMessage("The current room admins are: "+str(admins)+".")            
            this.isCommand = True

        elif command.startswith("admin "):
            playerName = command.split(" ")[1]
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                if playerName in this.client.room.adminsRoom:
                    this.sendMessage(""+str(playerName)+" is already an admin.")
                else:
                    this.client.room.adminsRoom.append(playerName)
                    for client in this.client.room.clients.values():
                        client.Utility.sendMessage(""+str(playerName)+" is now an admin.")
            this.isCommand = True

        elif command.startswith("me "):
            message = command.split(" ")[1]
            if not this.client.playerName in this.client.room.playersBan:
                for client in this.client.room.clients.values():
                    client.Utility.sendMessage("<V>*"+str(this.client.playerName)+" <N>"+str(message)+"")
            this.isCommand = True

        elif command.startswith("c "):
            message = command.split(" ")[1]
            this.staffChat(this.client.playerName, message)
            this.isCommand = True

        elif command.startswith("spawn "):
            if this.client.playerName in this.client.room.adminsRoom:
                this.consoleChat(2, this.client.playerName, "!" + command)
                try:
                    objID = command.split(" ")[1]
                except:
                    objID = 0
                try:
                    posX = command.split(" ")[2]
                except:
                    posX = 140
                try:
                    posY = command.split(" ")[3]
                except:
                    posY = 320
                this.spawnObj(objID, posX, posY, 0)
            this.isCommand = True

        elif command == "snow":
            if this.client.playerName in this.client.room.adminsRoom:
                this.consoleChat(2, this.client.playerName, "!" + command)
                this.client.room.sendAll([5, 23], struct.pack("!?h", True, 10))
            this.isCommand = True

        elif command.startswith("snow "):            
            event = command.split(" ")[1]
            if this.client.playerName in this.client.room.adminsRoom:
                this.consoleChat(2, this.client.playerName, "!" + command)
                if event == "on":
                    this.client.room.sendAll([5, 23], struct.pack("!?h", True, 10))
                elif event == "off":
                    this.client.room.sendAll([5, 23], struct.pack("!?h", False, 10))
            this.isCommand = True

        elif command.startswith("time "):
            time = command.split(" ")[1]
            if this.client.playerName in this.client.room.adminsRoom:
                this.consoleChat(2, this.client.playerName, "!" + command)
                try:
                    if time > 32767:
                        time = 32767
                    this.client.room.sendAll([5, 22], struct.pack("!H", int(time)))
                except:
                    time = 32767
                    this.client.room.sendAll([5, 22], struct.pack("!H", int(time)))
            this.isCommand = True

        elif command.startswith("ban "):
            playerName = command.split(" ")[1]
            if this.client.playerName in this.client.room.adminsRoom:
                this.consoleChat(2, this.client.playerName, "!" + command)
                if not playerName in this.client.room.playersBan:
                    if playerName in this.client.room.adminsRoom:
                        this.sendMessage(""+str(playerName)+" is an admin and can't be banned.")
                    else:
                        this.client.room.playersBan.append(playerName)
                        for client in this.client.room.clients.values():
                            client.Utility.sendMessage("<R>"+str(playerName)+" has been banned.")            
                else:
                    this.sendMessage(""+str(playerName)+" is already banned.")
            this.isCommand = True

        elif command.startswith("unban "):
            playerName = command.split(" ")[1]
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                if playerName in this.client.room.playersBan:
                    num = None
                    for i, x in enumerate(this.client.room.playersBan):
                        if x == playerName:
                            num = i
                    del this.client.room.playersBan[num]
                    for client in this.client.room.clients.values():
                        client.Utility.sendMessage(""+str(playerName)+" has been unbanned.")
            this.isCommand = True

        elif command == "banlist":
            if this.client.playerName in this.client.room.adminsRoom:
                this.consoleChat(2, this.client.playerName, "!" + command)
                banList = ' '.join(this.client.room.playersBan)
                this.sendMessage(str(banList))
            this.isCommand = True

        elif command == "vampire":
            if this.client.playerName in this.client.room.adminsRoom:
                this.consoleChat(2, this.client.playerName, "!" + command)
                this.client.room.sendAll([8, 66], struct.pack("!i", this.client.playerCode))
            this.isCommand = True

        elif command.startswith("vampire "):
            event = command.split(" ")[1]
            if this.client.playerName in this.client.room.adminsRoom:
                this.consoleChat(2, this.client.playerName, "!" + command)
                if not event in ["me", "all"]:
                    for client in this.client.room.clients.values():
                        if event == client.playerName:
                            client.room.sendAll([8, 66], struct.pack("!i", client.playerCode))
                elif event == "me":
                    this.client.room.sendAll([8, 66], struct.pack("!i", this.client.playerCode))
                elif event == "all":
                    for client in this.client.room.clients.values():
                        client.room.sendAll([8, 66], struct.pack("!i", client.playerCode))
            this.isCommand = True

        elif command == "name":
            if this.client.playerName in this.client.room.adminsRoom:
                this.consoleChat(2, this.client.playerName, "!" + command)
                color = "000000"
                data = struct.pack("!i", this.client.playerCode)
                data += struct.pack("!i", int(color, 16))
                this.client.room.sendAll([29, 4], data)
            this.isCommand = True
                
        elif command.startswith("name "):
            event = command.split(" ")[1]
            try:
                color = command.split(" ")[2]
            except:
                color = "000000"                
            if this.client.playerName in this.client.room.adminsRoom:
                this.consoleChat(2, this.client.playerName, "!" + command)
                if not event in ["me", "all"]:
                    for client in this.client.room.clients.values():
                        if event == client.playerName:
                            data = struct.pack("!i", client.playerCode)
                            data += struct.pack("!i", int(color, 16))
                            client.room.sendAll([29, 4], data)                                                        
                elif event == "me":
                    data = struct.pack("!i", this.client.playerCode)
                    data += struct.pack("!i", int(color, 16))
                    this.client.room.sendAll([29, 4], data)
                elif event == "all":
                    for client in this.client.room.clients.values():
                        data = struct.pack("!i", client.playerCode)
                        data += struct.pack("!i", int(color, 16))
                        client.room.sendAll([29, 4], data)                    
            this.isCommand = True

        elif command.startswith("tp "):
            if this.client.playerName in this.client.room.adminsRoom:
                this.consoleChat(2, this.client.playerName, "!" + command)
                try:
                    posX = command.split(" ")[1]
                    posY = command.split(" ")[2]
                    if posX == "all":
                        try:
                            posX = command.split(" ")[2]
                            posY = command.split(" ")[3]
                            for client in this.client.room.clients.values():
                                client.room.sendAll([8, 3], struct.pack("!hhih", int(posX), int(posY), 0, 0))
                        except:
                            pass
                    elif not posX.isdigit():
                        try:
                            playerName = command.split(" ")[1]
                            posX = command.split(" ")[2]
                            posY = command.split(" ")[3]
                            for client in this.client.room.clients.values():
                                if playerName == client.playerName:
                                    client.room.sendAll([8, 3], struct.pack("!hhih", int(posX), int(posY), 0, 0))                                    
                        except:
                            pass
                    elif posX and posY.isdigit():
                        this.client.room.sendAll([8, 3], struct.pack("!hhih", int(posX), int(posY), 0, 0))
                except:
                    pass
            this.isCommand = True

        elif command == "meep":
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                this.client.sendPacket([8, 39], "\x01")
            this.isCommand = True

        elif command.startswith("meep "):
            event = command.split(" ")[1]
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                if event == "me":
                    this.client.sendPacket([8, 39], "\x01")
                elif event == "all":
                    for client in this.client.room.clients.values():
                        client.sendPacket([8, 39], "\x01")
                elif not event in ["me", "all"]:
                    for client in this.client.room.clients.values():
                        if event == client.playerName:
                            client.sendPacket([8, 39], "\x01")
            this.isCommand = True

        elif command == "disco":
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                if this.client.room.discoRoom == False:
                    this.client.room.discoRoom = True
                    for client in this.client.room.clients.values():
                        client.reactorDisco()
                elif this.client.room.discoRoom == True:
                    this.client.room.discoRoom = False
            this.isCommand = True

        elif command == "fly":
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                this.client.isFly = True
                this.client.room.bindKeyBoard(this.client.playerName, 32, False, this.client.isFly)
            this.isCommand = True
            
        elif command.startswith("fly "):
            event = command.split(" ")[1]
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                if event == "me":
                    this.client.isFly = True
                    this.client.room.bindKeyBoard(this.client.playerName, 32, False, this.client.isFly)
                elif event == "on":
                    for client in this.client.room.clients.values():
                        client.isFly = True
                        client.room.bindKeyBoard(client.playerName, 32, False, client.isFly)
                elif event == "off":
                    for client in this.client.room.clients.values():
                        client.isFly = False                        
                if not event in ["me", "on", "off"]:
                    for client in this.client.room.clients.values():
                        if event == client.playerName:
                            client.isFly = True
                            client.room.bindKeyBoard(client.playerName, 32, False, client.isFly)                
            this.isCommand = True

        elif command == "ffa":
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                this.client.isFFA = True
                this.client.room.bindKeyBoard(this.client.playerName, 40, False, this.client.isFFA)
            this.isCommand = True

        elif command.startswith("ffa "):
            event = command.split(" ")[1]
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                if event == "me":
                    this.client.isFFA = True
                    this.client.room.bindKeyBoard(this.client.playerName, 40, False, this.client.isFFA)
                elif event == "on":
                    for client in this.client.room.clients.values():
                        client.isFFA = True
                        client.room.bindKeyBoard(client.playerName, 40, False, client.isFFA)
                elif event == "off":
                    for client in this.client.room.clients.values():
                        client.isFFA = False
                if not event in ["me", "on", "off"]:
                    for client in this.client.room.clients.values():
                        if event == client.playerName:
                            client.isFFA = True
                            client.room.bindKeyBoard(client.playerName, 40, False, client.isFFA)
            this.isCommand = True

        elif command == "shaman":
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                this.client.sendShamanCode(this.client.playerCode, 0)
            this.isCommand = True

        elif command.startswith("shaman "):
            event = command.split(" ")[1]
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                if event == "me":
                    this.client.sendShamanCode(this.client.playerCode, 0)
                elif event == "all":
                    for client in this.client.room.clients.values():
                        client.sendShamanCode(client.playerCode, 0)
                if not event in ["me", "all"]:
                    for client in this.client.room.clients.values():
                        if event == client.playerName:
                            client.sendShamanCode(client.playerCode, 0)
            this.isCommand = True

        elif command in ["np", "map"]:
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                this.client.room.mapChange()
            this.isCommand = True

        elif command.startswith("np ") or command.startswith("map "):
            mapCode = command.split(" ")[1]
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                try:
                    this.client.room.forceNextMap = mapCode
                    this.client.room.mapChange()
                except:
                    pass
            this.isCommand = True

        elif command in ["kill", "mort"]:
            this.consoleChat(2, this.client.playerName, "!" + command)
            if not this.client.isDead:
                this.client.isDead = True
                if not this.client.room.noAutoScore: this.client.playerScore += 1
                this.client.sendPlayerDied()
            this.isCommand = True

        elif command.startswith("kill ") or command.startswith("mort "):
            event = command.split(" ")[1]
            this.consoleChat(2, this.client.playerName, "!" + command)
            if event == "me":
                if not this.client.isDead:
                    this.client.isDead = True
                    if not this.client.room.noAutoScore: this.client.playerScore += 1
                    this.client.sendPlayerDied()
            elif event == "all":
                if this.client.playerName in this.client.room.adminsRoom:
                    for client in this.client.room.clients.values():
                        if not client.isDead:
                            client.isDead = True
                            if not client.room.noAutoScore: client.playerScore += 1
                            client.sendPlayerDied()
            if not event in ["me", "all"]:
                if this.client.playerName in this.client.room.adminsRoom:
                    for client in this.client.room.clients.values():
                        if event == client.playerName:
                            if not client.isDead:
                                client.isDead = True
                                if not client.room.noAutoScore: client.playerScore += 1
                                client.sendPlayerDied()
            this.isCommand = True

        elif command == "cheese":
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                this.client.room.sendAll([5, 19], [this.client.playerCode])
            this.isCommand = True

        elif command.startswith("cheese "):
            event = command.split(" ")[1]
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                if event == "me":
                    this.client.room.sendAll([5, 19], [this.client.playerCode])
                elif event == "all":
                    for client in this.client.room.clients.values():
                        client.room.sendAll([5, 19], [client.playerCode])
                if not event in ["me", "all"]:
                    for client in this.client.room.clients.values():
                        if event == client.playerName:
                            client.room.sendAll([5, 19], [client.playerCode])
            this.isCommand = True

        elif command == "explosion":
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                if this.canExplosion == False:
                    this.client.isExplosion = True
                    this.client.room.bindMouse(this.client.playerName, this.client.isExplosion)
                    this.canExplosion = True
                elif this.canExplosion == True:
                    this.client.isExplosion = False
                    this.client.room.bindMouse(this.client.playerName, this.client.isExplosion)
                    this.canExplosion = False
            this.isCommand = True

        elif command.startswith("explosion "):
            event = command.split(" ")[1]
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                if event == "me":
                    if this.canExplosion == False:
                        this.client.isExplosion = True
                        this.client.room.bindMouse(this.client.playerName, this.client.isExplosion)
                        this.canExplosion = True
                    elif this.canExplosion == True:
                        this.client.isExplosion = False
                        this.client.room.bindMouse(this.client.playerName, this.client.isExplosion)
                        this.canExplosion = False
                elif event in ["all", "on"]:
                    for client in this.client.room.clients.values():
                        if client.Utility.canExplosion == False:
                            client.isExplosion = True
                            client.room.bindMouse(client.playerName, client.isExplosion)
                            client.Utility.canExplosion = True
                        elif client.Utility.canExplosion == True:
                            client.isExplosion = False
                            client.room.bindMouse(client.playerName, client.isExplosion)
                            client.Utility.canExplosion = False
                elif event == "off":
                    for client in this.client.room.clients.values():
                        client.isExplosion = False
                        client.room.bindMouse(client.playerName, client.isExplosion)
                        client.Utility.canExplosion = False
                if not event in ["me", "all", "on", "off"]:
                    for client in this.client.room.clients.values():
                        if event == client.playerName:
                            if client.Utility.canExplosion == False:
                                client.isExplosion = True
                                client.room.bindMouse(client.playerName, client.isExplosion)
                                client.Utility.canExplosion = True
                            elif client.Utility.canExplosion == True:
                                client.isExplosion = False
                                client.room.bindMouse(client.playerName, client.isExplosion)
                                client.Utility.canExplosion = False
            this.isCommand = True
            
        elif command == "pw":
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                this.client.room.roomPassword = ""
                for client in this.client.room.clients.values():
                    client.Utility.sendMessage("The room's password has been removed.")
            this.isCommand = True

        elif command.startswith("pw "):
            password = command.split(" ")[1]
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                this.client.room.roomPassword = str(password)                
                for client in this.client.room.clients.values():
                    client.Utility.sendMessage(""+str(this.client.playerName)+" has set a room password.")
                this.sendMessage("The room's password has been set to: "+str(password)+"")
            this.isCommand = True

        elif command == "win":
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                this.playerWin()
                this.client.isDead = True
            this.isCommand = True

        elif command.startswith("win "):
            event = command.split(" ")[1]
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                if event == "me":
                    this.playerWin()
                    this.client.isDead = True
                elif event == "all":
                    for client in this.client.room.clients.values():
                        client.Utility.playerWin()
                        client.isDead = True
                if not event in ["me", "all"]:
                    for client in this.client.room.clients.values():
                        if event == client.playerName:
                            client.Utility.playerWin()
                            client.isDead = True
            this.isCommand = True

        elif command == "fireworks":
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:            
                for client in this.client.room.clients.values():
                    client.Utility.isFireworks = True
                    client.fireworksUtility()
            this.isCommand = True

        elif command.startswith("fireworks "):
            event = command.split(" ")[1]
            this.consoleChat(2, this.client.playerName, "!" + command)
            if this.client.playerName in this.client.room.adminsRoom:
                if event == "off":
                    for client in this.client.room.clients.values():
                        client.Utility.isFireworks = False
                elif event != "off":
                    for client in this.client.room.clients.values():
                        client.Utility.isFireworks = True
                        client.fireworksUtility()
            this.isCommand = True
