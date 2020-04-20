#coding: utf-8
import re, time as _time, os

# Modules
from Utiles import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers

# Library
from collections import deque

class Tribulle:
    try:
        
        def __init__(this, player, server):
            this.client = player
            this.server = player.server
            this.Cursor = player.Cursor

            this.TRIBE_RANKS = "0|${trad#TG_0}|0;1|${trad#TG_1}|0;2|${trad#TG_2}|0;3|${trad#TG_3}|0;4|${trad#TG_4}|32;5|${trad#TG_5}|160;6|${trad#TG_6}|416;7|${trad#TG_7}|932;8|${trad#TG_8}|2044;9|${trad#TG_9}|2046"
            
        def getTime(this):
            return int(_time.time() / 60)

        def sendPacket(this, code, result):
            this.client.sendPacket([60, 3], ByteArray().writeShort(code).writeBytes(result).toByteArray())
      
        def sendPacketToPlayer(this, playerName, code, result):
            player = this.server.players.get(playerName)
            if player != None:
                player.tribulle.sendPacket(code, result)

        def sendPacketWholeTribe(this, code, result, all=False):
            for player in this.server.players.values():
                if player.playerCode != this.client.playerCode or all:
                    if player.tribeCode == this.client.tribeCode:
                        player.tribulle.sendPacket(code, result)

        def sendPacketWholeChat(this, chatID, code, result, all=False):
            for player in this.server.players.values():
                if player.playerCode != this.client.playerCode or all:
                    if chatID in player.chats:
                        player.tribulle.sendPacket(code, result)

        def updateTribeData(this):
            for player in this.server.players.values():
                if player.tribeCode == this.client.tribeCode:
                    player.tribeHouse = this.client.tribeHouse
                    player.tribeMessage = this.client.tribeMessage
                    player.tribeRanks = this.client.tribeRanks

        def parseTribulleCode(this, code, packet):
            if code == 28:
                this.sendFriendsList(packet)
            elif code == 30:
                this.closeFriendsList(packet)
            elif code == 18:
                this.addFriend(packet)
            elif code == 20:
                this.removeFriend(packet)
            elif code == 46:
                this.sendIgnoredsList(packet)
            elif code == 42:
                this.ignorePlayer(packet)
            elif code == 44:
                this.removeIgnore(packet)
            elif code == 52:
                this.whisperMessage(packet)
            elif code == 60:
                this.disableWhispers(packet)
            elif code == 10:
                this.changeGender(packet)
            elif code == 22:
                this.marriageInvite(packet)
            elif code == 24:
                this.marriageAnswer(packet)
            elif code == 26:
                this.marriageDivorce(packet)
            elif code == 108:
                this.sendTribeInfo(packet)
            elif code == 84:
                this.createTribe(packet)
            elif code == 78:
                this.tribeInvite(packet)
            elif code == 80:
                this.tribeInviteAnswer(packet)
            elif code == 98:
                this.changeTribeMessage(packet)
            elif code == 102:
                this.changeTribeCode(packet)
            elif code == 110:
                this.closeTribe(packet)
            elif code == 118:
                this.createNewTribeRank(packet)
            #Edited By Elnas
            elif code == 120:
                this.deleteTribeRank(packet)
            elif code == 116:
                this.renameTribeRank(packet)
            #Edited By Elnas
            elif code == 122:
                this.changeRankPosition(packet)
            elif code == 114:
                this.setRankPermition(packet)
            elif code == 112:
                this.changeTribePlayerRank(packet)
            elif code == 132:
                this.showTribeHistorique(packet)
            elif code == 82:
                this.leaveTribe(packet)
            elif code == 104:
                this.kickPlayerTribe(packet)
            elif code == 126:
                this.setTribeMaster(packet)
            elif code == 128:
                this.finishTribe(packet)
            elif code == 54:
                this.customChat(packet)
            elif code == 48:
                this.chatMessage(packet)
            elif code == 58:
                this.chatMembersList(packet)
            elif code == 50:
                this.sendTribeChatMessage(packet)
            else:
                if this.server.isDebug:
                    print "[%s] [WARN][%s] Invalid tribulle code -> Code: %s packet: %s" %(_time.strftime("%H:%M:%S"), this.client.playerName, code, repr(packet.toByteArray()))
            
        def sendFriendsList(this, readPacket):
            p = ByteArray().writeShort(3 if readPacket == None else 34)
            if readPacket == None:
                p.writeByte(this.client.gender).writeInt(this.client.playerID)
            if this.client.marriage == "":
                p.writeInt(0).writeUTF("").writeByte(0).writeInt(0).writeByte(0).writeByte(0).writeInt(1).writeUTF("").writeInt(0)
            else:
                try:
                    player = this.server.players.get(this.client.marriage)
                    this.Cursor.execute("select Username, PlayerID, Gender, LastOn from Users where Username = %s", [this.client.marriage])
                    rs = this.Cursor.fetchone()
                    p.writeInt(rs["PlayerID"]).writeUTF(rs["Username"].lower()).writeByte(rs["Gender"]).writeInt(rs["PlayerID"]).writeByte(1).writeBoolean(this.server.checkConnectedAccount(rs["Username"])).writeInt(4).writeUTF(player.roomName if player else "").writeInt(rs["LastOn"])
                except:
                    this.client.marriage = ""
            infos = {}
            this.Cursor.execute("select Username, PlayerID, FriendsList, Marriage, Gender, LastOn from Users where Username in (%s)" %(Utils.joinWithQuotes(this.client.friendsList)))
            for rs in this.Cursor.fetchall():
                infos[rs["Username"]] = [rs["PlayerID"], rs["FriendsList"], rs["Marriage"], rs["Gender"], rs["LastOn"]]

            this.client.openingFriendList = True
            isOnline = []
            friendsOn = []
            friendsOff = []
            isOffline = []
            for playerName in this.client.friendsList:
                if not infos.has_key(playerName):
                    continue
                if not this.client.friendsList == ['']:
                    player = this.server.players.get(playerName)
                    info = infos[playerName]
                    isFriend = this.client.playerName in player.friendsList if player != None else this.client.playerName in info[1].split(",")
                    if this.server.checkConnectedAccount(playerName):
                        if isFriend:
                            friendsOn.append(playerName)
                        else:
                            isOnline.append(playerName)
                    else:
                        if isFriend:
                            friendsOff.append(playerName)
                        else:
                            isOffline.append(playerName)
            playersNames = friendsOn + isOnline + friendsOff + isOffline
            
            p.writeShort(len(playersNames)-1 if playersNames == [''] else len(playersNames))
            for playerName in playersNames:
                if not infos.has_key(playerName):
                    continue
                if not playersNames == ['']:
                    info = infos[playerName]
                    player = this.server.players.get(playerName)
                    isFriend = this.client.playerName in player.friendsList if player != None else this.client.playerName in info[1].split(",")
                    genderID = player.gender if player else int(info[3])
                    isMarriage = this.client.playerName == player.marriage if player else info[2] == this.client.playerName
                    p.writeInt(info[0]).writeUTF(playerName.lower()).writeByte(genderID).writeInt(info[0]).writeByte(1 if isFriend else 0).writeBoolean(this.server.checkConnectedAccount(playerName)).writeInt(4 if isFriend and player != None else 1).writeUTF(player.roomName if isFriend and player != None else "").writeInt(info[4] if isFriend else 0)
            if readPacket == None:
                p.writeShort(len(this.client.ignoredsList)-1 if this.client.ignoredsList == [''] else len(this.client.ignoredsList))

                for playerName in this.client.ignoredsList:
                    if not this.client.ignoredsList == ['']:
                        p.writeUTF(playerName.lower())
                p.writeUTF(this.client.tribeName)
                p.writeInt(this.client.tribeCode)
                p.writeUTF(this.client.tribeMessage)
                p.writeInt(this.client.tribeHouse)
                if not this.client.tribeRanks == "":
                    rankInfo = this.client.tribeRanks.split(";")
                    rankName = rankInfo[this.client.tribeRank].split("|")
                    p.writeUTF(rankName[1])
                    p.writeInt(rankName[2])
                else:
                    p.writeUTF("")
                    p.writeInt(0)
            this.client.sendPacket([60, 3], p.toByteArray())
            if not readPacket == None and not this.client.marriage == "":
                this.sendPacket(15 if readPacket == "0" else 29, ByteArray().writeInt(this.client.tribulleID+1).writeByte(1).toByteArray())

        def closeFriendsList(this, readPacket):
            this.client.openingFriendList = False
            this.sendPacket(31, ByteArray().writeBytes(readPacket.toByteArray()).writeByte(1).toByteArray())

        def addFriend(this, readPacket):
            tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
            id = this.server.getPlayerID(playerName)
            player = this.server.players.get(playerName)
            isFriend = this.checkFriend(playerName, this.client.playerName)
            if not this.server.checkExistingUser(playerName):
                this.sendPacket(19, ByteArray().writeInt(tribulleID).writeByte(12).toByteArray())
            elif len(this.client.friendsList) >= 200:
                this.sendPacket(19, ByteArray().writeInt(tribulleID).writeByte(7).toByteArray())
            elif str(playerName) in this.client.friendsList:
                pass
                # this.sendPacket(19, ByteArray().writeInt(tribulleID).writeByte(12).toByteArray())
            else:
                this.client.friendsList.append(playerName)
                if playerName in this.client.ignoredsList:
                    this.client.ignoredsList.remove(playerName)
                this.Cursor.execute("select Username, PlayerID, Gender, LastOn from Users where Username = %s", [playerName])
                rs = this.Cursor.fetchone()
                this.sendPacket(36, ByteArray().writeInt(rs["PlayerID"]).writeUTF(Utils.parsePlayerName(playerName)).writeByte(rs["Gender"]).writeInt(rs["PlayerID"]).writeShort(this.server.checkConnectedAccount(playerName)).writeInt(4 if isFriend else 0).writeUTF(player.roomName if isFriend and player != None else "").writeInt(rs["LastOn"] if isFriend else 0).toByteArray())
                this.sendPacket(19, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
                if this.client.openingFriendList:
                    this.sendFriendsList("0")
                if player != None:
                    player.tribulle.sendPacket(35, ByteArray().writeInt(this.client.playerID).writeUTF(this.client.playerName.lower()).writeByte(this.client.gender).writeInt(this.client.playerID).writeByte(1).writeByte(this.server.checkConnectedAccount(this.client.playerName)).writeInt(4 if isFriend else 0).writeUTF(this.client.roomName if isFriend else "").writeInt(this.client.lastOn if isFriend else 0).toByteArray())
                    if player.openingFriendList:
                        player.tribulle.sendFriendsList("0")
            
        def removeFriend(this, readPacket):
            tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
            packet = ByteArray()
            id = this.server.getPlayerID(playerName)

            if playerName in this.client.friendsList:
                packet.writeInt(id)
                this.client.friendsList.remove(playerName)
                this.sendPacket(37, packet.toByteArray())
                this.sendPacket(21, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
                if this.client.openingFriendList:
                    this.sendFriendsList("0")

                player = this.server.players.get(playerName)
                if player != None:
                    player.tribulle.sendPacket(35, ByteArray().writeInt(this.client.playerID).writeUTF(this.client.playerName.lower()).writeByte(this.client.gender).writeInt(this.client.playerID).writeShort(1).writeInt(0).writeUTF("").writeInt(0).toByteArray())              
                    if player.openingFriendList:
                        player.tribulle.sendFriendsList("0")

        def sendFriendConnected(this, playerName):
            if playerName in this.client.friendsList:
                id = this.server.getPlayerID(playerName)
                player = this.server.players.get(playerName)
                this.sendPacket(35, ByteArray().writeInt(player.playerID).writeUTF(playerName.lower()).writeByte(player.gender).writeInt(player.playerID).writeByte(1).writeByte(1).writeInt(1).writeUTF("").writeInt(player.lastOn).toByteArray())
                this.sendPacket(Identifiers.tribulle.send.ET_SignaleConnexionAmi, ByteArray().writeUTF(player.playerName.lower()).toByteArray())
                   
        def sendFriendChangedRoom(this, playerName, langueID):
            if playerName in this.client.friendsList:
                player = this.server.players.get(playerName)
                if player != None: this.sendPacket(35, ByteArray().writeInt(player.playerID).writeUTF(playerName.lower()).writeByte(player.gender).writeInt(player.playerID).writeByte(1).writeByte(1).writeInt(4).writeUTF(player.roomName).writeInt(player.lastOn).toByteArray())
                    
        def sendFriendDisconnected(this, playerName):
            if playerName in this.client.friendsList:
                this.Cursor.execute("select Username, PlayerID, Gender, LastOn from Users where Username = %s", [playerName])
                rs = this.Cursor.fetchone()
                this.sendPacket(35, ByteArray().writeInt(rs["PlayerID"]).writeUTF(playerName.lower()).writeByte(rs["Gender"]).writeInt(rs["PlayerID"]).writeByte(1).writeByte(0).writeInt(1).writeUTF("").writeInt(rs["LastOn"]).toByteArray())
                this.sendPacket(Identifiers.tribulle.send.ET_SignaleDeconnexionAmi, ByteArray().writeUTF(playerName.lower()).toByteArray())
                
        def sendIgnoredsList(this, readPacket):
            tribulleID = readPacket.readInt()
            packet = ByteArray().writeInt(tribulleID).writeShort(len(this.client.ignoredsList))
            for playerName in this.client.ignoredsList:
                packet.writeUTF(playerName)
            this.sendPacket(47, packet.toByteArray())
    
        def ignorePlayer(this, readPacket):
            tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
            packet = ByteArray().writeInt(tribulleID)

            if not this.server.checkExistingUser(playerName):
                this.sendPacket(43, packet.writeByte(12).toByteArray())
            else:
                this.client.ignoredsList.append(playerName)

                if playerName in this.client.friendsList:
                    this.client.friendsList.remove(playerName)
                this.sendPacket(43, packet.writeByte(1).toByteArray())

        def removeIgnore(this, readPacket):
            tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
            packet = ByteArray().writeInt(tribulleID)

            this.client.ignoredsList.remove(playerName)
            this.sendPacket(45, packet.writeByte(1).toByteArray())

        def whisperMessage(this, readPacket):
            tribulleID, playerName, message = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF()), readPacket.readUTF().replace("\n", "").replace("&amp;#", "&#").replace("<", "&lt;")
            isCheck = this.client.privLevel < 8 and this.server.checkMessage(message, this.client)

            if this.client.isGuest:
                this.client.sendLangueMessage("", "$Créer_Compte_Parler")
            elif not message == "":
                can = True

                packet = ByteArray().writeInt(tribulleID)
                if playerName.startswith("*") or not this.server.players.has_key(playerName):
                    can = False
                    packet.writeByte(12)
                    packet.writeShort(0)
                    this.sendPacket(53, packet.toByteArray())
                else:
                    if this.client.isMute:
                        if not this.client.isGuest:
                            muteInfo = this.server.getModMuteInfo(this.client.playerName)
                            timeCalc = Utils.getHoursDiff(muteInfo[1])
                            if timeCalc <= 0:
                                this.server.removeModMute(this.client.playerName)
                            else:
                                can = False
                                this.client.sendModMute(this.client.playerName, timeCalc, muteInfo[0], True)

                if can:
                    player = this.server.players.get(playerName)
                    if player != None:
                        if player.silenceType != 0:
                            if (this.client.privLevel >= 5 or (player.silenceType == 1 and this.checkFriend(playerName, this.client.playerName))):
                                pass
                            else:
                                this.sendSilenceMessage(playerName, tribulleID)
                                return

                        if not (this.client.playerName in player.ignoredsList) and not isCheck:
                            player.tribulle.sendPacket(66, ByteArray().writeUTF(this.client.playerName.lower()).writeInt(this.client.langueID+1).writeUTF(player.playerName.lower()).writeUTF(message).toByteArray())
                        this.sendPacket(66, ByteArray().writeUTF(this.client.playerName.lower()).writeInt(player.langueID+1).writeUTF(player.playerName.lower()).writeUTF(message).toByteArray())

                        if isCheck:
                            this.server.sendStaffMessage(7, "<V>%s<BL> está enviando mensagens no cochicho com palavras suspeitas [<R>%s<BL>]." %(this.client.playerName, message))

                        if this.client.privLevel >= 1:
                            this.client.sendLuaMessageAdmin("<font color='#FF8F00'>[SUSURRO: <J>%s</J> => <J>%s</J>] [Susurro: <J>%s</J>]</font>" %(this.client.playerName, playerName, message))
 			    message += '\n[SUSURRO: {i} => {d}] [Susurro: {u}]'.format(i=this.client.playerName, d=playerName, u=message)
 			    if os.path.exists('./CentralmiceES/Logs/Tribulle/Susurros/'+this.client.playerName+'.log'):
 				    oFile = open('./CentralmiceES/Logs/Tribulle/Susurros/'+this.client.playerName+'.log', 'a')
 			    else:
 				    oFile = open('./CentralmiceES/Logs/Tribulle/Susurros/'+this.client.playerName+'.log', 'w')
 			    oFile.write(message)
 			    oFile.close()

                        if not this.server.chatMessages.has_key(this.client.playerName):
                             messages = deque([], 60)
                             messages.append([_time.strftime("%Y/%m/%d %H:%M:%S"), "> [%s] %s" %(player.playerName, message)])
                             this.server.chatMessages[this.client.playerName] = messages
                        else:
                             this.server.chatMessages[this.client.playerName].append([_time.strftime("%Y/%m/%d %H:%M:%S"), "> [%s] %s" %(player.playerName, message)])

        def disableWhispers(this, readPacket):
            tribulleID, type, message = readPacket.readInt(), readPacket.readByte(), readPacket.readUTF()
            this.sendPacket(61, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())

            this.client.silenceType = type
            this.client.silenceMessage = "" if this.server.checkMessage(message, this.client) else message

        def sendSilenceMessage(this, playerName, tribulleID):
            player = this.server.players.get(playerName)
            if player != None:
                this.sendPacket(53, ByteArray().writeInt(tribulleID).writeByte(24).writeUTF(player.silenceMessage).toByteArray())

        def changeGender(this, readPacket):
            tribulleID, gender = readPacket.readInt(), readPacket.readByte()
            this.client.gender = gender
            this.sendPacket(12, ByteArray().writeInt(tribulleID).writeByte(gender).toByteArray())
            this.sendPacket(12, ByteArray().writeByte(gender).toByteArray())
            this.client.sendProfile(this.client.playerName)
            #for player in this.server.players.values():
            #    if this.client.playerName and player.playerName in this.client.friendsList and player.friendsList:
            #        player.tribulle.sendPacket(11, ByteArray().writeInt(tribulleID).writeByte(gender).toByteArray())

        def getTribePermissions(this, tribePerm, tribeHouse = True):
            if(tribePerm > 9 or tribePerm < 0): return False
            if (this.client.tribeName in ["", None, "None"]) or (tribeHouse and not this.client.room.isTribeHouse):
                return False
            rankInfo = this.client.tribeRanks.split(";")
            perms = rankInfo[this.client.tribeRank].split("|")
            perms = str(Utils.binarizar(int(perms[2]))).zfill(11)
            #rankStatus = {0: "adminForum", 1: "loadNP",2: "changeHouse",3: "playMusic",4: "kickPlayer",5: "invitePlayer",6: "changeRank",7: "editRank", 8: "changeMessage", 9: "Leader"}
            try:return int(perms[tribePerm]) == 1
            except: return False

        def marriageInvite(this, readPacket):
            tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
            packet = ByteArray().writeInt(tribulleID)

            player = this.server.players.get(playerName)
            if not this.server.checkConnectedAccount(playerName) or not this.server.checkExistingUser(playerName):
                this.sendPacket(23, packet.writeByte(11).toByteArray())
            elif not player.marriage == "":
                this.sendPacket(23, packet.writeByte(14).toByteArray())
            else:
                if not this.client.playerName in player.ignoredMarriageInvites:
                    player.marriageInvite = [this.client.playerName, tribulleID]
                    player.tribulle.sendPacket(38, ByteArray().writeUTF(this.client.playerName).toByteArray())
                    this.sendPacket(23, packet.writeByte(1).toByteArray())

        def marriageAnswer(this, readPacket):
            tribulleID, playerName, answer = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF()), readPacket.readByte()

            player = this.server.players.get(playerName)
            if player != None:
                if answer == 0:
                    this.sendPacket(25, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
                    player.tribulle.sendPacket(40, ByteArray().writeUTF(this.client.playerName.lower()).toByteArray())

                elif answer == 1:
                    player.marriage = this.client.playerName
                    this.client.marriage = player.playerName

                    if not this.client.playerName in player.friendsList:
                        player.friendsList.append(this.client.playerName)
                        
                    if this.client.playerName in player.ignoredsList:
                        player.ignoredsList.remove(playerName)

                    if not player.playerName in this.client.friendsList:
                        this.client.friendsList.append(player.playerName)
                        
                    if player.playerName in this.client.ignoredsList:
                        this.client.remove(playerName)

                    this.sendPacket(39, ByteArray().writeUTF(player.playerName.lower()).toByteArray())
                    player.tribulle.sendPacket(39, ByteArray().writeUTF(this.client.playerName.lower()).toByteArray())

                    if this.client.openingFriendList:
                        this.sendFriendsList("0")

                    if player.openingFriendList:
                        player.tribulle.sendFriendsList("0")

                    this.sendPacket(37, ByteArray().writeInt(player.playerID).toByteArray())
                    player.tribulle.sendPacket(37, ByteArray().writeInt(this.client.playerID).toByteArray())

                    this.sendPacket(25, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
                
        def marriageDivorce(this, readPacket):
            tribulleID = readPacket.readInt()

            time = Utils.getTime() + 3600

            this.sendPacket(41, ByteArray().writeUTF(this.client.marriage).writeByte(1).toByteArray())
            player = this.server.players.get(this.client.marriage)
            if player != None:
                player.tribulle.sendPacket(41, ByteArray().writeUTF(player.marriage).writeByte(1).toByteArray())
                player.marriage = ""
                player.lastDivorceTimer = time
                if player.openingFriendList:
                    player.tribulle.sendFriendsList("0")
            else:
                this.removeMarriage(this.client.marriage, time)

            this.client.marriage = ""
            this.client.lastDivorceTimer = time
            if this.client.openingFriendList:
                this.sendFriendsList("0")
            
        def sendTribe(this, isNew):
            if this.client.tribeName == "":
                this.sendPacket(Identifiers.tribulle.send.ET_ErreurInformationsTribu, ByteArray().writeInt(0).writeByte(0).toByteArray())
                return

            if not this.client.tribeChat in this.client.chats:
                this.client.chats.append(this.client.tribeChat)

            this.sendPacket(Identifiers.tribulle.send.ET_SignaleRejointCanal, ByteArray().writeInt(this.client.tribeChat).writeUTF("~" + this.client.tribeName.lower()).writeBytes(chr(0) * 5).toByteArray())
            this.sendPacketWholeTribe(Identifiers.tribulle.send.ET_SignaleMembreRejointCanal, ByteArray().writeInt(this.client.tribeChat).writeInt(this.client.playerID).writeUTF(this.client.playerName.lower()).toByteArray())
            this.sendTribeInfo()

        def sendLoginMessageTribe(this):
            packet = ByteArray()
            packet.writeInt(0)
            packet.writeInt(0)
            packet.writeInt(0)
            packet.writeInt(0)
            packet.writeInt(0)
            packet.writeShort(1)
            packet.writeInt(0)
            packet.writeShort(0)

            members = this.getTribeMembers(this.client.tribeCode)
            packet.writeShort(len(members))

            infos = {}
            this.Cursor.execute("select Username, PlayerID, Gender, LastOn, TribeRank, TribeJoined from Users where Username in (%s)" %(Utils.joinWithQuotes(members)))
            for rs in this.Cursor.fetchall():
                infos[rs["Username"]] = [rs["PlayerID"], rs["Gender"], rs["LastOn"], rs["TribeRank"], rs["TribeJoined"]]

            for member in members:
                if not infos.has_key(member):
                    continue

                info = infos[member]
                player = this.server.players.get(member)
                packet.writeInt(info[0])
                packet.writeUTF(member.lower())
                packet.writeByte(info[1])
                packet.writeInt(info[0])
                packet.writeInt(info[2] if not this.server.checkConnectedAccount(member) else 0)
                packet.writeByte(info[3])
                packet.writeInt(4)
                packet.writeUTF(player.roomName if player != None else "")
            

        def sendTribeInfo(this, readPacket=""):
            if not readPacket == "":
                tribulleID, connected = readPacket.readInt(), readPacket.readByte()
            else:
                tribulleID = this.client.tribulleID + 1
                connected = 0
            if this.client.tribeName == "":
                this.sendPacket(109, ByteArray().writeInt(this.client.tribulleID).writeByte(17).toByteArray())
                return
            members = this.getTribeMembers(this.client.tribeCode)
            packet = ByteArray()
            packet.writeInt(this.client.tribeCode)
            packet.writeUTF(this.client.tribeName)
            packet.writeUTF(this.client.tribeMessage)
            packet.writeInt(this.client.tribeHouse)
            
            infos = {}
            this.client.isTribeOpen = True
            this.Cursor.execute("select Username, PlayerID, Gender, LastOn, TribeRank, TribeJoined from Users where Username in (%s)" %(Utils.joinWithQuotes(members)))
            for rs in this.Cursor.fetchall():
                infos[rs["Username"]] = [rs["PlayerID"], rs["Gender"], rs["LastOn"], rs["TribeRank"], rs["TribeJoined"]]

            isOnline = []
            isOffline = []

            for member in members:
                if this.server.checkConnectedAccount(member):
                    isOnline.append(member)
                else:
                    isOffline.append(member)

            if connected == 1:
                playersTribe = isOnline + isOffline
            else:
                playersTribe = isOnline

            packet.writeShort(len(playersTribe))
                
            for member in playersTribe:
                if not infos.has_key(member):
                    continue

                info = infos[member]
                player = this.server.players.get(member)
                packet.writeInt(info[0])
                packet.writeUTF(member.lower())
                packet.writeByte(info[1])
                packet.writeInt(info[0])
                packet.writeInt(info[2] if not this.server.checkConnectedAccount(member) else 0)
                packet.writeByte(info[3])
                packet.writeInt(4)
                packet.writeUTF(player.roomName if player != None else "")

            packet.writeShort(len(this.client.tribeRanks.split(";")))

            for rank in this.client.tribeRanks.split(";"):
                ranks = rank.split("|")
                packet.writeUTF(ranks[1]).writeInt(ranks[2])

            # this.client.server.log(packet.toByteArray())
            this.sendPacket(130, packet.toByteArray())
            
        def closeTribe(this, readPacket):
            tribulleID = readPacket.readInt()
            this.client.isTribeOpen = False
            this.sendPacket(111, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())

        def sendTribeMemberConnected(this):
            this.sendPacketWholeTribe(88, ByteArray().writeUTF(this.client.playerName.lower()).toByteArray(), True)
            this.sendPacketWholeTribe(131, ByteArray().writeInt(this.client.playerID).writeUTF(this.client.playerName.lower()).writeByte(this.client.gender).writeInt(this.client.playerID).writeInt(0).writeByte(this.client.tribeRank).writeInt(1).writeUTF("").toByteArray())

        def sendTribeMemberChangeRoom(this):
            this.sendPacketWholeTribe(131, ByteArray().writeInt(this.client.playerID).writeUTF(this.client.playerName.lower()).writeByte(this.client.gender).writeInt(this.client.playerID).writeInt(0).writeByte(this.client.tribeRank).writeInt(4).writeUTF(this.client.roomName).toByteArray())

        def sendTribeMemberDisconnected(this):
            this.sendPacketWholeTribe(90, ByteArray().writeUTF(this.client.playerName.lower()).toByteArray())
            this.sendPacketWholeTribe(131, ByteArray().writeInt(this.client.playerID).writeUTF(this.client.playerName.lower()).writeByte(this.client.gender).writeInt(this.client.playerID).writeInt(this.client.lastOn).writeByte(this.client.tribeRank).writeInt(1).writeUTF("").toByteArray())
            
        def sendPlayerInfo(this):
            this.sendPacket(Identifiers.tribulle.send.ET_ReponseDemandeInfosJeuUtilisateur, ByteArray().writeInt(0).writeInt(this.client.playerID).writeInt(this.client.playerID).writeInt(this.getInGenderMarriage(this.client.playerName)).writeInt(this.server.getPlayerID(this.client.marriage) if not this.client.marriage == "" else 0).writeUTF(this.client.marriage).toByteArray())

        def createTribe(this, readPacket):
            tribulleID, tribeName = readPacket.readInt(), readPacket.readUTF()
            this.sendPacket(85, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())

            createTime = this.getTime()
            if not this.checkExistingTribe(tribeName) and len(tribeName)<20:
                if this.client.shopCheeses >= 500:
                    this.Cursor.execute("insert into Tribe  values(null, %s, '', '0', %s, '', %s, %s)", [tribeName, this.TRIBE_RANKS, this.client.playerName, this.server.lastChatID])
                    this.client.shopCheeses -= 500
                    this.client.tribeCode = this.Cursor.lastrowid
                    this.client.tribeRank = 9
                    this.client.tribeName = tribeName
                    this.client.tribeJoined = createTime
                    this.client.tribeMessage = "Bienvenido a esta nueva tribu -Comunidad: Centralmice ES ;)"
                    this.client.tribeRanks = this.TRIBE_RANKS

                    this.setTribeHistorique(this.client.tribeCode, 1, createTime, this.client.playerName, tribeName)

                    this.client.updateDatabase()
                    this.client.sendLuaMessageAdmin("[<J>%s</J>] - Player <N>%s creo una nueva tribu: <CH>%s" %(this.client.ipAddress, this.client.playerName, tribeName))

                    this.sendPacket(89, ByteArray().writeUTF(this.client.tribeName).writeInt(this.client.tribeCode).writeUTF(this.client.tribeMessage).writeInt(0).writeUTF(this.client.tribeRanks.split(";")[9].split("|")[1]).writeInt(2049).toByteArray())
                else:
                    this.sendPacket(85, ByteArray().writeInt(this.tribulleID).toByteArray())

        def tribeInvite(this, readPacket):
            tribulleID, playerName = readPacket.readInt(), Utils.parsePlayerName(readPacket.readUTF())
            packet = ByteArray().writeInt(tribulleID)
            player = this.server.players.get(playerName)

            if not this.server.checkConnectedAccount(playerName) or not this.server.checkExistingUser(playerName):
                this.sendPacket(79, packet.writeByte(12).toByteArray())
            elif not player.tribeName == "":
                this.sendPacket(79, packet.writeByte(18).toByteArray())
            else:
                if not this.client.tribeCode in player.ignoredTribeInvites:
                    player.tribeInvite = [tribulleID, this.client]
                    player.tribulle.sendPacket(86, ByteArray().writeUTF(this.client.playerName.lower()).writeUTF(this.client.tribeName).toByteArray())
                    this.sendPacket(79, packet.writeByte(1).toByteArray())

        def tribeInviteAnswer(this, readPacket):
            tribulleID, playerName, answer = readPacket.readInt(), readPacket.readUTF(), readPacket.readByte()
            resultTribulleID = int(this.client.tribeInvite[0])
            player = this.client.tribeInvite[1]
            this.client.tribeInvite = []

            if player != None:

                if answer == 0:
                    this.client.ignoredTribeInvites.append(player.tribeCode)
                    player.tribulle.sendPacket(87, ByteArray().writeUTF(this.client.playerName.lower()).writeByte(0).toByteArray())

                elif answer == 1:
                    members = this.getTribeMembers(player.tribeCode)
                    members.append(this.client.playerName)
                    this.setTribeMembers(player.tribeCode, members)

                    this.client.tribeCode = player.tribeCode
                    this.client.tribeRank = 0
                    this.client.tribeName = player.tribeName
                    this.client.tribeJoined = this.getTime()
                    tribeInfo = this.getTribeInfo(this.client.tribeCode)
                    this.client.tribeName = str(tribeInfo[0])
                    this.client.tribeMessage = str(tribeInfo[1])
                    this.client.tribeHouse = int(tribeInfo[2])
                    this.client.tribeRanks = tribeInfo[3]
                    this.client.tribeChat = int(tribeInfo[4])

                    this.setTribeHistorique(this.client.tribeCode, 2, this.getTime(), player.playerName, this.client.playerName)

                    packet = ByteArray()
                    packet.writeUTF(this.client.tribeName)
                    packet.writeInt(this.client.tribeCode)
                    packet.writeUTF(this.client.tribeMessage)
                    packet.writeInt(this.client.tribeHouse)

                    rankInfo = this.client.tribeRanks.split(";")
                    rankName = rankInfo[this.client.tribeRank].split("|")
                    packet.writeUTF(rankName[1])
                    packet.writeInt(rankName[2])
                    this.sendPacket(89, packet.toByteArray())
                    player.tribulle.sendPacket(87, ByteArray().writeUTF(this.client.playerName).writeByte(1).toByteArray())
                    this.sendPacketWholeTribe(91, ByteArray().writeUTF(this.client.playerName).toByteArray(), True)
                    this.updateTribeInfo()
                    this.sendTribeMemberChangeRoom()

        def changeTribeMessage(this, readPacket):
            tribulleID, message = readPacket.readInt(), readPacket.readUTF()
            this.Cursor.execute("update Tribe set Message = %s where Code = %s", [message, this.client.tribeCode])
            this.client.tribeMessage = message
            this.setTribeHistorique(this.client.tribeCode, 6, this.getTime(), message, this.client.playerName)
            this.updateTribeData()
            this.sendTribeInfo()
            this.sendPacketWholeTribe(125, ByteArray().writeUTF(this.client.playerName.lower()).writeUTF(message).toByteArray(), True)
            
        def changeTribeCode(this, readPacket):
            tribulleID, mapCode = readPacket.readInt(), readPacket.readInt()
            this.Cursor.execute("update Tribe set House = %s where Code = %s", [mapCode, this.client.tribeCode])
            
            mapInfo = this.client.room.getMapInfo(mapCode)
            if mapInfo[0] == None:
                this.client.sendPacket(Identifiers.old.send.Tribe_Result, [16])
            elif mapInfo[4] != 22:
                this.client.sendPacket(Identifiers.old.send.Tribe_Result, [17])

            elif mapInfo[0] != None and mapInfo[4] == 22:
                this.setTribeHistorique(this.client.tribeCode, 8, this.getTime(), this.client.playerName, mapCode)
                    
            room = this.server.rooms.get("*\x03" + this.client.tribeName)
            if room != None:
                room.mapChange()

            this.updateTribeData()
            this.sendTribeInfo()

        def updateTribeInfo(this):
            members = this.getTribeMembers(this.client.tribeCode)
            for member in members:
                player = this.server.players.get(member)
                if player != None:
                    if player.isTribeOpen:
                        player.tribulle.updateTribeRanks()
                        player.tribulle.updateTribeData()
                        player.tribulle.sendTribeInfo()
        def createNewTribeRank(this, readPacket):
            tribulleID, rankName = readPacket.readInt(), readPacket.readUTF()

            ranksID = this.client.tribeRanks.split(";")
            s = ranksID[1]
            f = ranksID[1:]
            f = ";".join(map(str, f))
            s = "%s|%s|%s" % ("0", rankName, "0")
            del ranksID[1:]
            ranksID.append(s)
            ranksID.append(f)
            this.client.tribeRanks = ";".join(map(str, ranksID))
            members = this.getTribeMembers(this.client.tribeCode)
            for playerName in members:
                player = this.server.players.get(playerName)
                tribeRank = this.getPlayerTribeRank(playerName)
                if player != None:
                    if player.tribeRank >= 1:
                        player.tribeRank += 1
                        this.Cursor.execute("update Users set TribeRank = %s where Username = %s", [tribeRank+1, playerName])
                else:
                    if tribeRank >= 1:
                        this.Cursor.execute("update Users set TribeRank = %s where Username = %s", [tribeRank+1, playerName])

            this.updateTribeRanks()
            this.updateTribeData()
            this.sendTribeInfo()
            for member in members:
                player = this.server.players.get(member)
                if player != None:
                    if player.isTribeOpen:
                        player.tribulle.sendTribeInfo()

        def deleteTribeRank(this, readPacket):
            tribulleID, rankID = readPacket.readInt(), readPacket.readByte()

            rankInfo = this.client.tribeRanks.split(";")
            del rankInfo[rankID]
            this.client.tribeRanks = ";".join(map(str, rankInfo))

            this.updateTribeRanks()
            this.updateTribeData()

            members = this.getTribeMembers(this.client.tribeCode)
            for playerName in members:
                player = this.server.players.get(playerName)
                if player != None:
                    if player.tribeRank == rankID:
                        player.tribeRank = 0
                    elif player.tribeRank > rankID:
                        player.tribeRank -= 1
                        this.Cursor.execute("update Users set TribeRank = %s where Username = %s", [player.tribeRank, playerName]) 
                    else:
                        continue
                else:
                    tribeRank = this.getPlayerTribeRank(playerName)
                    if tribeRank == rankID:
                        this.Cursor.execute("update Users set TribeRank = 0 where Username = %s", [playerName])
                    elif tribeRank > rankID:
                        tribeRank -= 1
                        this.Cursor.execute("update Users set TribeRank = %s where Username = %s", [tribeRank, playerName]) 
                    else:
                        continue
            this.sendTribeInfo()
            for member in members:
                player = this.server.players.get(member)
                if player != None:
                    if player.isTribeOpen:
                        player.tribulle.sendTribeInfo()
            
        def renameTribeRank(this, packet):
            tribulleID, rankID, rankName = packet.readInt(), packet.readByte(), packet.readUTF()
            rankInfo = this.client.tribeRanks.split(";")
            rank = rankInfo[rankID].split("|")
            rank[1] = rankName
            rankInfo[rankID] = "|".join(map(str, rank))
            this.client.tribeRanks = ";".join(map(str, rankInfo))
            this.updateTribeRanks()
            this.updateTribeData()
            this.sendTribeInfo()
            members = this.getTribeMembers(this.client.tribeCode)
            for member in members:
                player = this.server.players.get(member)
                if player != None:
                    if player.isTribeOpen:
                        player.tribulle.sendTribeInfo()

        def changeRankPosition(this, packet):
            tribulleID, rankID, rankID2 = packet.readInt(), packet.readByte(), packet.readByte()

            ranks = this.client.tribeRanks.split(";")
            rank = ranks[rankID]
            rank2 = ranks[rankID2]
            ranks[rankID] = rank2
            ranks[rankID2] = rank
            this.client.tribeRanks = ";".join(map(str, ranks))
            this.updateTribeRanks()
            this.updateTribeData()
            members = this.getTribeMembers(this.client.tribeCode)
            for member in members:
                player = this.server.players.get(member)
                if player != None:
                    if player.tribeRank == rankID:
                        player.tribeRank = rankID2
                        this.Cursor.execute("update Users set TribeRank = %s where Username = %s", [rankID2, member])
                    elif player.tribeRank == rankID2:
                        player.tribeRank = rankID
                        this.Cursor.execute("update Users set TribeRank = %s where Username = %s", [rankID, member])
                else:   
                    this.Cursor.execute("select TribeRank from Users where Username = %s", [member])
                    rankPlayer = this.Cursor.fetchone()['TribeRank']

                    if rankPlayer == rankID:
                        this.Cursor.execute("update Users set TribeRank = %s where Username = %s", [rankID2, member])
                    elif rankPlayer == rankID2:
                        this.Cursor.execute("update Users set TribeRank = %s where Username = %s", [rankID, member])
                        

            this.updateTribeRanks()
            this.updateTribeData()
            this.sendTribeInfo()
            for member in members:
                player = this.server.players.get(member)
                if player != None:
                    if player.isTribeOpen:
                        player.tribulle.sendTribeInfo()

        def setRankPermition(this, packet):
            tribulleID, rankID, permID, type = packet.readInt(), packet.readByte(), packet.readInt(), packet.readByte()
            rankInfo = this.client.tribeRanks.split(";")
            perms = rankInfo[rankID].split("|")
            soma = 0
            if type == 0:
                soma = int(perms[2]) + 2**permID
            elif type == 1:
                soma = int(perms[2]) - 2**permID
            perms[2] = str(soma)
            join = "|".join(map(str, perms))
            rankInfo[rankID] = join
            this.client.tribeRanks = ";".join(map(str, rankInfo))
            this.updateTribeRanks()
            this.updateTribeData()
            this.sendTribeInfo()
            members = this.getTribeMembers(this.client.tribeCode)
            for member in members:
                player = this.server.players.get(member)
                if player != None:
                    if player.isTribeOpen:
                        player.tribulle.sendTribeInfo()

        def changeTribePlayerRank(this, packet):
            tribulleID, playerName, rankID = packet.readInt(), packet.readUTF(), packet.readByte()

            rankInfo = this.client.tribeRanks.split(";")
            rankName = rankInfo[rankID].split("|")[1]

            player = this.server.players.get(playerName)
            this.Cursor.execute("select Username, PlayerID, Gender, LastOn from Users where Username = %s", [playerName])
            rs = this.Cursor.fetchone()
            if player != None:
                player.tribeRank = rankID
                this.Cursor.execute("update Users set TribeRank = %s where Username = %s", [rankID, playerName])
            else:
                this.Cursor.execute("update Users set TribeRank = %s where Username = %s", [rankID, playerName])
            this.setTribeHistorique(this.client.tribeCode, 5, this.getTime(), playerName, str(rankID), rankName, this.client.playerName)
            # this.sendPacket(131, ByteArray().writeInt(rs[1]).writeUTF(playerName.lower()).writeByte(rs[2]).writeInt(rs[1]).writeInt(0 if this.server.checkConnectedAccount(playerName) else rs[3]).writeByte(rankID).writeInt(1).writeUTF("" if player == None else player.roomName).toByteArray())
            this.sendPacketWholeTribe(124, ByteArray().writeUTF(this.client.playerName.lower()).writeUTF(playerName.lower()).writeUTF(rankName).toByteArray(), True)
            this.sendPacket(113, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
            members = this.getTribeMembers(this.client.tribeCode)
            for member in members:
                player = this.server.players.get(member)
                if player != None:
                    if player.isTribeOpen:
                        player.tribulle.sendTribeInfo()

        def showTribeHistorique(this, readPacket):
            tribulleID, sla, sla2 = readPacket.readInt(), readPacket.readInt(), readPacket.readInt()
            historique = this.getTribeHistorique(this.client.tribeCode).split("|")

            packet = ByteArray()
            packet.writeInt(tribulleID)
            total = len(historique)
            historique = historique[sla:sla+sla2]
            packet.writeShort(len(historique) - 1 if historique == [''] else len(historique))
            for event in historique:
                event = event.split("/")
                if not historique == [''] and not event[1] == '':
                    packet.writeInt(event[1])
                    packet.writeInt(event[0])
                    if int(event[0]) == 8:
                        packet.writeUTF('{"code":"%s","auteur":"%s"}' % (event[3], event[2]))
                    elif int(event[0]) == 6:
                        packet.writeUTF('{"message":"%s","auteur":"%s"}' % (event[2], event[3]))
                    elif int(event[0]) == 5:
                        packet.writeUTF('{"cible":"%s","ordreRang":"%s","rang":"%s","auteur":"%s"}' % (event[2], event[3], event[4], event[5]))
                    elif int(event[0]) == 4:
                        packet.writeUTF('{"membreParti":"%s","auteur":"%s"}' % (event[2], event[2]))
                    elif int(event[0]) == 3:
                        packet.writeUTF('{"membreExclu":"%s","auteur":"%s"}' % (event[2], event[3]))
                    elif int(event[0]) == 2:
                        packet.writeUTF('{"membreAjoute":"%s","auteur":"%s"}' % (event[3], event[2]))
                    elif int(event[0]) == 1:
                        packet.writeUTF('{"tribu":"%s","auteur":"%s"}' % (event[3], event[2]))

            packet.writeInt(total)

            this.sendPacket(133, packet.toByteArray())

        def leaveTribe(this, packet):
            tribulleID = packet.readInt()
            p = ByteArray().writeInt(tribulleID)

            if this.client.tribeRank == (len(this.client.tribeRanks.split(";"))-1):
                p.writeByte(4)
            else:
                p.writeByte(1)
                
                this.sendPacketWholeTribe(92, ByteArray().writeUTF(this.client.playerName.lower()).toByteArray(), True)

                members = this.getTribeMembers(this.client.tribeCode)
                if this.client.playerName in members:
                    members.remove(this.client.playerName)
                    this.setTribeMembers(this.client.tribeCode, members)

                    this.setTribeHistorique(this.client.tribeCode, 4, this.getTime(), this.client.playerName)
                    
                    this.client.tribeCode = 0
                    this.client.tribeName = ""
                    this.client.tribeRank = 0
                    this.client.tribeJoined = 0
                    this.client.tribeHouse = 0
                    this.client.tribeMessage = ""
                    this.client.tribeRanks = ""
                    this.client.tribeChat = 0
                for member in members:
                    player = this.server.players.get(member)
                    if player != None:
                        if player.isTribeOpen:
                            player.tribulle.sendTribeInfo()
            this.sendPacket(83, p.toByteArray())

        def kickPlayerTribe(this, packet):
            tribulleID, playerName = packet.readInt(), packet.readUTF()
            p = ByteArray().writeInt(tribulleID)
            player = this.server.players.get(playerName)

            tribeCode = player.tribeCode if player != None else this.getPlayerTribeCode(playerName)

            if tribeCode != 0:
                p.writeByte(1)
                members = this.getTribeMembers(this.client.tribeCode)
                if playerName in members:
                    members.remove(playerName)
                    this.setTribeMembers(this.client.tribeCode, members)
                    
                    this.setTribeHistorique(this.client.tribeCode, 3, this.getTime(), playerName, this.client.playerName)
                    this.sendPacketWholeTribe(93, ByteArray().writeUTF(playerName.lower()).writeUTF(this.client.playerName.lower()).toByteArray(), True)

                    if player != None:
                        player.tribeCode = 0
                        player.tribeName = ""
                        player.tribeRank = 0
                        player.tribeJoined = 0
                        player.tribeHouse = 0
                        player.tribeMessage = ""
                        player.tribeRanks = ""
                        player.tribeChat = 0
                    else:
                        this.Cursor.execute("update Users set TribeCode = 0, TribeRank = 0, TribeJoined = 0 where Username = %s", [playerName])
                this.updateTribeInfo()
            this.sendPacket(105, p.toByteArray())

        def setTribeMaster(this, packet):
            tribulleID, playerName = packet.readInt(), packet.readUTF()

            rankInfo = this.client.tribeRanks.split(";")
            this.client.tribeRank = (len(rankInfo)-2)
            this.Cursor.execute("update Users set TribeRank = %s where Username = %s", [len(rankInfo)-2, this.client.playerName])
            player = this.server.players.get(playerName)
            if player != None:
                player.tribeRank = (len(rankInfo)-1)
                this.Cursor.execute("update Users set TribeRank = %s where Username = %s", [len(rankInfo)-1, playerName])
            else:
                this.Cursor.execute("update Users set TribeRank = %s where Username = %s", [len(rankInfo)-1, playerName])
            this.Cursor.execute("select Username, PlayerID, Gender, LastOn from Users where Username = %s", [playerName])
            rs = this.Cursor.fetchone()
            this.sendPacket(131, ByteArray().writeInt(rs[1]).writeUTF(playerName.lower()).writeByte(rs[2]).writeInt(rs[1]).writeInt(0 if this.server.checkConnectedAccount(playerName) else rs[3]).writeByte(len(rankInfo)-1).writeInt(4).writeUTF("" if player == None else player.roomName).toByteArray())
            this.sendPacket(131, ByteArray().writeInt(this.client.playerID).writeUTF(this.client.playerName.lower()).writeByte(this.client.gender).writeInt(this.client.playerID).writeInt(0).writeByte(len(rankInfo)-2).writeInt(4).writeUTF(this.client.roomName).toByteArray())
            this.sendPacket(127, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
            members = this.getTribeMembers(this.client.tribeCode)
            for member in members:
                player = this.server.players.get(member)
                if player != None:
                    if player.isTribeOpen:
                        player.tribulle.sendTribeInfo()

        def finishTribe(this, packet):
            tribulleID = packet.readInt()
            p = ByteArray()
            p.writeInt(tribulleID).writeByte(1)
            members = this.getTribeMembers(this.client.tribeCode)
            this.Cursor.execute("update Users set TribeCode = 0, TribeRank = 0, TribeJoined = 0 where TribeCode = %s", [this.client.tribeCode])
            this.Cursor.execute("delete from Tribe where Code = %s", [this.client.tribeCode])
            for member in members:
                player = this.server.players.get(member)
                if player != None:
                    player.tribulle.sendPacket(93, ByteArray().writeUTF(player.playerName.lower()).writeUTF(this.client.playerName.lower()).toByteArray())
                    player.tribeCode, player.tribeRank, player.tribeJoined, player.tribeHouse, player.tribeChat, player.tribeRankID = 0, 0, 0, 0, 0, 0
                    player.tribeMessage, player.tribeName = "", ""
                    player.tribeRanks = ""
                    player.tribeInvite = []
                    player.tribulle.sendPacket(127, p.toByteArray())
                this.client.sendPacket([6, 9], ByteArray().writeUTF("Kabile dağıtıldı.").toByteArray())

        def customChat(this, packet):
            tribulleID, chatName = packet.readInt(), packet.readUTF()

            if re.match("^(?=^(?:(?!.*_$).)*$)(?=^(?:(?!_{2,}).)*$)[A-Za-z][A-Za-z0-9_]{2,11}$", chatName):
                chatID = this.getChatID(chatName)
                if chatID == -1:
                    this.Cursor.execute("insert into Chats values (null, %s)", [chatName])

                chatID = this.getChatID(chatName)

                this.client.chats.append(chatID)
                this.sendPacket(62, ByteArray().writeUTF(chatName).toByteArray())
                this.sendPacket(55, ByteArray().writeInt(tribulleID).writeByte(1).toByteArray())
            else:
                this.sendPacket(55, ByteArray().writeInt(tribulleID).writeByte(7).toByteArray())
            
        def chatMessage(this, packet):
            tribulleID, chatName, message = packet.readInt(), packet.readUTF(), packet.readUTF()
            isCheck = this.client.privLevel < 8 and this.server.checkMessage(message, this.client)
            if not isCheck:
                chatID = this.getChatID(chatName)
                this.sendPacketWholeChat(chatID, 64, ByteArray().writeUTF(this.client.playerName.lower()).writeInt(4).writeUTF(chatName).writeUTF(message).toByteArray(), True)
                this.sendPacket(49, ByteArray().writeInt(tribulleID).writeByte(0).toByteArray())
                this.client.sendLuaMessageAdmin("[<J>%s</J>] [<J>%s</J>] [<J>CHAT</J>] - %s => %s" %(this.client.ipAddress, chatName, this.client.playerName, message))
            
        def chatMembersList(this, packet):
            tribulleID, chatName = packet.readInt(), packet.readUTF()
            p = ByteArray().writeInt(tribulleID).writeByte(1)
            chatID = this.getChatID(chatName)
            length = 0
            for player in this.server.players.values():
                if chatID in player.chats:
                    length += 1
            p.writeShort(length)

            for player in this.server.players.values():
                if chatID in player.chats:
                    p.writeUTF(player.playerName)
            this.sendPacket(59, p.toByteArray())

        def sendTribeChatMessage(this, readPacket):
            tribulleID, message = readPacket.readInt(), readPacket.readUTF()
            this.sendPacketWholeTribe(65, ByteArray().writeUTF(this.client.playerName.lower()).writeUTF(message).toByteArray(), True)
            this.client.sendLuaMessageAdmin("<font color='#2CFF00'>[TRIBU: <J>%s</J> - Usuario: <J>%s</J> - Mensaje: <J>%s</J>]</font>" %(this.client.tribeName, this.client.playerName, message))

        def getGenderID(this, genderID, isFriendToo, isMarriedWithMe):
            dictionary = {0:{0:{0:0, 1:1}, 1:{0:2, 1:3}}, 1:{0:{0:4, 1:5}, 1:{0:6, 1:7}}, 2:{0:{0:8, 1:9}, 1:{0:10, 1:11}}}
            return dictionary[genderID][int(isMarriedWithMe)][int(isFriendToo)]

        def getPlayerLastOn(this, playerName):
            player = this.server.players.get(playerName)
            if player != None:
                return this.server.players[playerName].lastOn
            else:
                this.Cursor.execute("select LastOn from Users where Username = %s", [playerName])
                rs = this.Cursor.fetchone()
                if rs:
                    return rs["LastOn"]
                else:
                    return 0

        def checkFriend(this, playerName, playerNameToCheck):
            checkList = this.server.players[playerName].friendsList if this.server.players.has_key(playerName) else this.getUserFriends(playerName)
            return playerNameToCheck in checkList

        def getUserFriends(this, playerName):
            this.Cursor.execute("select FriendsList from Users where Username = %s", [playerName])
            rs = this.Cursor.fetchone()
            if rs:
                return rs["FriendsList"].split(",")
            else:
                return []

        def getPlayerGender(this, playerName):
            this.Cursor.execute("select Gender from Users where Username = %s", [playerName])
            rs = this.Cursor.fetchone()
            if rs:
                return rs["Gender"]
            else:
                return 0

        def getPlayerTribeRank(this, playerName):
            this.Cursor.execute("select TribeRank from Users where Username = %s", [playerName])
            rs = this.Cursor.fetchone()
            if rs:
                return rs["TribeRank"]
            else:
                return 0

        def getPlayerMarriage(this, playerName):
            this.Cursor.execute("select Marriage from Users where Username = %s", [playerName])
            rs = this.Cursor.fetchone()
            if rs:
                return rs["Marriage"]
            else:
                return ""

        def removeMarriage(this, playerName, time):
            this.Cursor.execute("update Users set Marriage = '', LastDivorceTimer = %s where Username = %s", [time, playerName])

        def getInGenderMarriage(this, playerName):
            if this.server.players.has_key(playerName):
                player = this.server.players.get(playerName)
                gender = player.gender
                marriage = player.marriage
            else:
                gender = this.getPlayerGender(playerName)
                marriage = this.getPlayerMarriage(playerName)
            return (5 if gender == 1 else 9 if gender == 2 else 1) if marriage == "" else (7 if gender == 1 else 11 if gender == 2 else 3)

        def getInGendersMarriage(this, marriage, gender):
            return (5 if gender == 1 else 9 if gender == 2 else 1) if marriage == "" else (7 if gender == 1 else 11 if gender == 2 else 3)

        def updateTribeRanks(this):
            this.Cursor.execute("update Tribe set Ranks = %s where Code = %s", [this.client.tribeRanks, this.client.tribeCode])

        def getTribeMembers(this, tribeCode):
            this.Cursor.execute("select Members from Tribe where Code = %s", [tribeCode])
            rs = this.Cursor.fetchone()
            if rs:
                return rs["Members"].split(",")
            else:
                return []

        def setTribeMembers(this, tribeCode, members):
            this.Cursor.execute("update Tribe set Members = %s where Code = %s", [",".join(map(str, members)), tribeCode])

        def checkExistingTribe(this, tribeName):
            this.Cursor.execute("select 1 from Tribe where Name = %s", [tribeName])
            return this.Cursor.fetchone() != None

        def checkExistingTribeRank(this, rankName):
            for rank in this.client.tribeRanks.values():
                checkRankName = rank.split("|")[0]
                if checkRankName == rankName:
                    return True
            return False

        def getTribeHistorique(this, tribeCode):
            this.Cursor.execute("select Historique from Tribe where Code = %s", [tribeCode])
            rs = this.Cursor.fetchone()
            if rs:
                return rs["Historique"]
            else:
                return ""

        def setTribeCache(this, tribeCode, historique):
            this.Cursor.execute("update Tribe set Historique = %s where Code = %s", [historique, tribeCode])

        def setTribeHistorique(this, tribeCode, *data):
            historique = this.getTribeHistorique(tribeCode)
            if historique == "":
                historique = "/".join(map(str, data))
            else:
                historique = "/".join(map(str, data)) + "|" + historique
            this.setTribeCache(tribeCode, historique)

        def getChatID(this, chatName):
            this.Cursor.execute("select ID from Chats where Name = %s", [chatName])
            rs = this.Cursor.fetchone()
            if rs:
                return rs["ID"]
            else:
                return -1

        def getPlayerTribeCode(this, playerName):
            this.Cursor.execute("select TribeCode from Users where Username = %s", [playerName])
            rs = this.Cursor.fetchone()
            if rs:
                return rs["TribeCode"]
            else:
                return 0

        def getTribeInfo(this, tribeCode):
            tribeRanks = ""
            this.Cursor.execute("select * from Tribe where Code = %s", [tribeCode])
            rs = this.Cursor.fetchone()
            if rs:
                tribeRanks = rs["Ranks"]
                return [rs["Name"], rs["Message"], rs["House"], tribeRanks, rs["Chat"]]
            else:
                return ["", "", 0, tribeRanks, 0]
    except:
        pass
