#coding: utf-8

# Modules
from ByteArray import ByteArray
from Identifiers import Identifiers

# Library
from twisted.internet import reactor

class ParseSkill:
    def __init__(this, player, server):
        this.client = player
        this.server = player.server                
        this.rangeArea = 85

    def sendExp(this, level, exp, nextLevel):
        this.client.sendPacket(Identifiers.send.Shaman_Exp, ByteArray().writeUnsignedShort(level - 1).writeInt(exp).writeInt(nextLevel).toByteArray())

    def sendGainExp(this, amount):
        this.client.sendPacket(Identifiers.send.Shaman_Gain_Exp, ByteArray().writeInt(amount).toByteArray())

    def sendEarnedExp(this, xp, numCompleted):
        this.client.sendPacket(Identifiers.send.Shaman_Earned_Exp, ByteArray().writeShort(xp).writeShort(numCompleted).toByteArray())

    def sendEarnedLevel(this, playerName, level):
        this.client.room.sendAll(Identifiers.send.Shaman_Earned_Level, ByteArray().writeUTF(playerName).writeUnsignedByte(level - 1).toByteArray())

    def sendTeleport(this, type, posX, posY):
        this.client.room.sendAll(Identifiers.send.Teleport, ByteArray().writeByte(type).writeShort(posX).writeShort(posY).toByteArray())

    def sendSkillObject(this, objectID, posX, posY, angle):
        this.client.room.sendAll(Identifiers.send.Skill_Object, ByteArray().writeShort(posX).writeShort(posY).writeByte(objectID).writeShort(angle).toByteArray())

    def sendShamanSkills(this, newBoolean):
        p = ByteArray().writeByte(len(this.client.playerSkills))
        for skill in this.client.playerSkills.items():
            p.writeUnsignedByte(skill[0]).writeUnsignedByte(5 if this.client.playerSkills[skill[0]] >= 6 else skill[1])
        this.client.sendPacket(Identifiers.send.Shaman_Skills, p.writeBoolean(newBoolean).toByteArray())

    def sendEnableSkill(this, id, count):
        this.client.sendPacket(Identifiers.send.Enable_Skill, chr(id) + chr(count))

    def sendShamanFly(this, fly):
        this.client.room.sendAllOthers(this.client, Identifiers.send.Shaman_Fly, ByteArray().writeInt(this.client.playerCode).writeBoolean(fly).toByteArray())

    def sendProjectionSkill(this, posX, posY, dir):
        this.client.room.sendAllOthers(this.client, Identifiers.send.Projection_Skill, ByteArray().writeShort(posX).writeShort(posY).writeShort(dir).toByteArray())

    def sendConvertSkill(this, objectID):
        this.client.room.sendAll(Identifiers.send.Convert_Skill, ByteArray().writeInt(objectID).writeByte(0).toByteArray())

    def sendDemolitionSkill(this, objectID):
        this.client.room.sendAll(Identifiers.send.Demolition_Skill, ByteArray().writeInt(objectID).toByteArray())

    def sendBonfireSkill(this, px, py, seconds):
        this.client.room.sendAll(Identifiers.send.Bonfire_Skill, ByteArray().writeShort(px).writeShort(py).writeByte(5 if seconds >= 100 else seconds).toByteArray())

    def sendSpiderMouseSkill(this, px, py):
        this.client.room.sendAll(Identifiers.send.Spider_Mouse_Skill, ByteArray().writeShort(px).writeShort(py).toByteArray())

    def sendRolloutMouseSkill(this, playerCode):
        this.client.room.sendAll(Identifiers.send.Rollout_Mouse_Skill, ByteArray().writeInt(playerCode).toByteArray())

    def sendDecreaseMouseSkill(this, playerCode):
        this.client.room.sendAll(Identifiers.send.Mouse_Size, ByteArray().writeInt(playerCode).writeShort(70).writeBoolean(True).toByteArray())

    def sendLeafMouseSkill(this, playerCode):
        this.client.room.sendAll(Identifiers.send.Leaf_Mouse_Skill, ByteArray().writeByte(1).writeInt(playerCode).toByteArray())

    def sendIceMouseSkill(this, playerCode, iced):
        this.client.room.sendAll(Identifiers.send.Iced_Mouse_Skill, ByteArray().writeInt(playerCode).writeBoolean(iced).toByteArray())

    def sendGravitationalSkill(this, seconds, velX, velY):
        this.client.room.sendAll(Identifiers.send.Gravitation_Skill, ByteArray().writeShort(seconds).writeShort(velX).writeShort(velY).toByteArray())
        
    def sendGrapnelSkill(this, playerCode, px, py):
        this.client.room.sendAll(Identifiers.send.Grapnel_Mouse_Skill, ByteArray().writeInt(playerCode).writeShort(px).writeShort(py).toByteArray())

    def sendEvolutionSkill(this, playerCode):
        this.client.room.sendAll(Identifiers.send.Evolution_Skill, ByteArray().writeInt(playerCode).writeUnsignedByte(200).toByteArray())

    def sendGatmanSkill(this, playerCode):
        this.client.room.sendAll(Identifiers.send.Gatman_Skill, ByteArray().writeInt(playerCode).writeByte(1).toByteArray())

    def sendRestorativeSkill(this, objectID, id):
        this.client.room.sendAll(Identifiers.send.Restorative_Skill, ByteArray().writeInt(objectID).writeInt(id).toByteArray())
        
    def sendRecyclingSkill(this, id):
        this.client.room.sendAll(Identifiers.send.Recycling_Skill, ByteArray().writeShort(id).toByteArray())

    def sendAntigravitySkill(this, objectID):
        this.client.room.sendAll(Identifiers.send.Antigravity_Skill, ByteArray().writeInt(objectID).writeShort(0).toByteArray())

    def sendHandymouseSkill(this, handyMouseByte, objectID):
        this.client.room.sendAll(Identifiers.send.Handymouse_Skill, ByteArray().writeByte(handyMouseByte).writeInt(objectID).writeByte(this.client.room.lastHandymouse[1]).writeInt(this.client.room.lastHandymouse[0]).toByteArray())

    def earnExp(this, isShaman, exp):
        gainExp = exp * (((3 if this.client.shamanLevel < 30 else (6 if this.client.shamanLevel >= 30 and this.client.shamanLevel < 60 else 10)) if this.client.shamanType == 0 else (5 if this.client.shamanLevel < 30 else (10 if this.client.shamanLevel >= 30 and this.client.shamanLevel < 60 else 20))) if isShaman else 1)
        this.client.shamanExp += gainExp
        if this.client.shamanExp < this.client.shamanExpNext:
            this.sendGainExp(this.client.shamanExp)
            this.sendExp(this.client.shamanLevel, this.client.shamanExp, this.client.shamanExpNext)
            if isShaman:
                this.sendEarnedExp(gainExp, exp)
        else:
            if this.client.shamanLevel < 300:
                this.client.shamanLevel += 1
                this.client.shamanExp -= this.client.shamanExpNext
                if this.client.shamanExp < 0:
                    this.client.shamanExp = 0

                this.client.shamanExpNext += 10 * this.client.shamanLevel

                this.sendExp(this.client.shamanLevel, 0, this.client.shamanExpNext)
                this.sendGainExp(this.client.shamanExp)
                if isShaman:
                    this.sendEarnedExp(gainExp, exp)

                if this.client.shamanLevel >= 20:
                    this.sendEarnedLevel(this.client.playerName, this.client.shamanLevel)

    def buySkill(this, skill):
        if this.client.shamanLevel - 1 > len(this.client.playerSkills):
            if this.client.playerSkills.has_key(skill):
                this.client.playerSkills[skill] += 1
            else:
                this.client.playerSkills[skill] = 1
            this.sendShamanSkills(True)

    def redistributeSkills(this):
        if this.client.shopCheeses >= this.client.shamanLevel:
            if len(this.client.playerSkills) >=  1:
                if this.client.canRedistributeSkills:
                    this.client.shopCheeses -= this.client.shamanLevel
                    this.client.playerSkills = {}
                    this.sendShamanSkills(True)
                    this.client.canRedistributeSkills = False
                    this.client.resSkillsTimer = reactor.callLater(600, setattr, this, "canRedistributeSkills", True)
                    this.client.totem = [0, ""]
                else:
                    this.client.sendPacket(Identifiers.send.Redistribute_Error_Time)
        else:
            this.client.sendPacket(Identifiers.send.Redistribute_Error_Cheeses)

    def getTimeSkill(this):
        if this.client.playerSkills.has_key(0):
            this.client.room.addTime += this.client.playerSkills[0] * 5

    def getkills(this):
        if this.client.isShaman:
            if this.client.playerSkills.has_key(4) and not this.client.room.isDoubleMap:
                this.client.canShamanRespawn = True

            for skill in [5, 8, 9, 11, 12, 26, 28, 29, 31, 41, 46, 48, 51, 52, 53, 60, 62, 65, 66, 67, 69, 71, 74, 80, 81, 83, 85, 88, 90, 93]:
                if this.client.playerSkills.has_key(skill) and not (this.client.room.isSurvivor and skill == 81):
                    this.sendEnableSkill(skill, this.client.playerSkills[skill] * 2 if skill in [28, 65, 74] else this.client.playerSkills[skill])

            for skill in [6, 30, 33, 34, 44, 47, 50, 63, 64, 70, 73, 82, 84, 92]:
                if this.client.playerSkills.has_key(skill):
                    if skill == 6: this.client.ambulanceCount = skill
                    this.sendEnableSkill(skill, 1)

            for skill in [7, 14, 27, 86, 87, 94]:
                if this.client.playerSkills.has_key(skill):
                    this.sendEnableSkill(skill, 100)

            for skill in [10, 13]:
                if this.client.playerSkills.has_key(skill):
                    this.sendEnableSkill(skill, 3)

            if this.client.playerSkills.has_key(20):
                count = this.client.playerSkills[20]            
                this.sendEnableSkill(20, [114, 118, 120, 122, 126][(5 if count > 5 else count) - 1])

            if this.client.playerSkills.has_key(21):
                this.bubblesCount = this.client.playerSkills[21]

            if this.client.playerSkills.has_key(22) and not this.client.room.currentMap in [108, 109]:
                count = this.client.playerSkills[22]
                this.sendEnableSkill(22, [25, 30, 35, 40, 45][(5 if count > 5 else count) - 1])

            if this.client.playerSkills.has_key(23):
                count = this.client.playerSkills[23]            
                this.sendEnableSkill(23, [40, 50, 60, 70, 80][(5 if count > 5 else count) - 1])

            if this.client.playerSkills.has_key(24):
                this.client.isOpportunist = True

            if this.client.playerSkills.has_key(32):
                this.client.iceCount += this.client.playerSkills[32]

            if this.client.playerSkills.has_key(40):
                count = this.client.playerSkills[40]            
                this.sendEnableSkill(40, [30, 40, 50, 60, 70][(5 if count > 5 else count) - 1])

            if this.client.playerSkills.has_key(42):
                count = this.client.playerSkills[42]            
                this.sendEnableSkill(42, [240, 230, 220, 210, 200][(5 if count > 5 else count) - 1])

            if this.client.playerSkills.has_key(43):
                count = this.client.playerSkills[43]            
                this.sendEnableSkill(43, [240, 230, 220, 210, 200][(5 if count > 5 else count) - 1])

            if this.client.playerSkills.has_key(45):
                count = this.client.playerSkills[45]
                this.sendEnableSkill(45, [110, 120, 130, 140, 150][(5 if count > 5 else count) - 1])

            if this.client.playerSkills.has_key(49):
                count = this.client.playerSkills[49]
                this.sendEnableSkill(49, [110, 120, 130, 140, 150][(5 if count > 5 else count) - 1])

            if this.client.playerSkills.has_key(54):
                this.sendEnableSkill(54, 130)

            if this.client.playerSkills.has_key(72):
                count = this.client.playerSkills[72]            
                this.sendEnableSkill(72, [25, 30, 35, 40, 45][(5 if count > 5 else count) - 1])

            if this.client.room.isSurvivor:
                this.sendEnableSkill(49, 10)
            elif this.client.playerSkills.has_key(89):
                count = this.client.playerSkills[89]            
                this.sendEnableSkill(49, [80, 70, 60, 50, 40][(5 if count > 5 else count) - 1])
                this.sendEnableSkill(54, [96, 92, 88, 84, 80][(5 if count > 5 else count) - 1])

            if this.client.playerSkills.has_key(91):
                this.client.desintegration = True

    def getPlayerSkills(this, skills):
        if skills.has_key(1):
            this.sendEnableSkill(1, [110, 120, 130, 140, 150][(5 if skills[1] > 5 else skills[1]) - 1])

        if skills.has_key(2):
            this.sendEnableSkill(2, [114, 126, 118, 120, 122][(5 if skills[2] > 5 else skills[2]) - 1])

        if skills.has_key(68):
            this.sendEnableSkill(68, [96, 92, 88, 84, 80][(5 if skills[68] > 5 else skills[68]) - 1])

    def placeSkill(this, objectID, code, px, py, angle):
        if code == 36:
            for client in this.client.room.clients.values():
                if this.checkQualifiedPlayer(px, py, client):
                    client.sendPacket(Identifiers.send.Can_Transformation, 1)
                    break

        elif code == 37:
            for client in this.client.room.clients.values():
                if this.checkQualifiedPlayer(px, py, client):
                    this.sendTeleport(36, client.posX, client.posY)
                    client.room.movePlayer(client.playerName, this.client.posX, this.client.posY, False, 0, 0, True)
                    this.sendTeleport(37, this.client.posX, this.client.posY)
                    break

        elif code == 38:
            for client in this.client.room.clients.values():
                if client.isDead and not client.hasEnter and not client.isAfk and not client.isShaman:
                    if this.client.ambulanceCount > 0:
                        this.client.ambulanceCount -= 1
                        this.client.room.respawnSpecific(client.playerName)
                        client.isDead = False
                        client.hasCheese = False
                        client.room.movePlayer(client.playerName, this.client.posX, this.client.posY, False, 0, 0, True)
                        this.sendTeleport(37, this.client.posX, this.client.posY)
                    else:
                        break
            this.client.room.sendAll(Identifiers.send.Skill, chr(38) + chr(1))

        elif code == 42:
            this.sendSkillObject(3, px, py, 0)

        elif code == 43:
            this.sendSkillObject(1, px, py, 0)

        elif code == 47:
            if this.client.room.numCompleted > 1:
                for client in this.client.room.clients.values():
                    if client.hasCheese and this.checkQualifiedPlayer(px, py, client):
                        client.playerWin(0)
                        break

        elif code == 55:
            for client in this.client.room.clients.values():
                if not client.hasCheese and this.client.hasCheese and this.checkQualifiedPlayer(px, py, client):
                    client.sendGiveCheese()
                    this.client.sendRemoveCheese()
                    this.client.hasCheese = False
                    break

        elif code == 56:
            this.sendTeleport(36, this.client.posX, this.client.posY)
            this.client.room.movePlayer(this.client.playerName, px, py, False, 0, 0, False)
            this.sendTeleport(37, px, py)

        elif code == 57:
            if this.client.room.cloudID == -1:
                this.client.room.cloudID = objectID
            else:
                this.client.room.removeObject(this.client.room.cloudID)
                this.client.room.cloudID = objectID

        elif code == 61:
            if this.client.room.companionBox == -1:
                this.client.room.companionBox = objectID
            else:
                this.client.room.removeObject(this.client.room.companionBox)
                this.client.room.companionBox = objectID

        elif code == 70:
            this.sendSpiderMouseSkill(px, py)

        elif code == 71:
            for client in this.client.room.clients.values():
                if this.checkQualifiedPlayer(px, py, client):
                    this.sendRolloutMouseSkill(client.playerCode)
                    this.client.room.sendAll(Identifiers.send.Skill, chr(71) + chr(1))
                    break

        elif code == 73:
            for client in this.client.room.clients.values():
                if this.checkQualifiedPlayer(px, py, client):
                    this.sendDecreaseMouseSkill(client.playerCode)
                    break

        elif code == 74:
            for client in this.client.room.clients.values():
                if this.checkQualifiedPlayer(px, py, client):
                    this.sendLeafMouseSkill(client.playerCode)
                    break

        elif code == 75:
            this.client.room.sendAll(Identifiers.send.Remove_All_Objects_Skill)

        elif code == 76:
            this.sendSkillObject(5, px, py, angle)

        elif code == 79:
            if not this.client.room.isSurvivor:
                for client in this.client.room.clients.values():
                    if this.checkQualifiedPlayer(px, py, client):
                        this.sendIceMouseSkill(client.playerCode, True)
                this.client.room.sendAll(Identifiers.send.Skill, chr(79) + chr(1))
                reactor.callLater(this.client.playerSkills[82] * 2, lambda: this.sendIceMouseSkill(client.playerCode, False))

        elif code == 81:
            this.sendGravitationalSkill(this.client.playerSkills[63] * 2, 0, 0)

        elif code == 83:
            for client in this.client.room.clients.values():
                if this.checkQualifiedPlayer(px, py, client):
                    client.sendPacket(Identifiers.send.Can_Meep, 1)
                    break

        elif code == 84:
            this.sendGrapnelSkill(this.client.playerCode, px, py)

        elif code == 86:
            if 86 in this.client.playerSkills:
                this.sendBonfireSkill(px, py, this.client.playerSkills[86] * 4)

        elif code == 92:
            this.getkills()
            this.client.room.sendAll(Identifiers.send.Reset_Shaman_Skills)

        elif code == 93:
            for client in this.client.room.clients.values():
                if this.checkQualifiedPlayer(px, py, client):
                    this.sendEvolutionSkill(client.playerCode)
                    break

        elif code == 94:
            this.sendGatmanSkill(this.client.playerCode)

    def parseEmoteSkill(this, emote):
        count = 0
        if emote == 0 and this.client.playerSkills.has_key(3):
            for client in this.client.room.clients.values():
                if this.client.playerSkills[3] >= count and client != this.client:
                    if client.posX >= this.client.posX - 400 and client.posX <= this.client.posX + 400:
                        if client.posY >= this.client.posY - 300 and client.posY <= this.client.posY + 300:
                            client.sendPlayerEmote(0, "", False, False)
                            count += 1
                else:
                    break

        elif emote == 4 and this.client.playerSkills.has_key(61):
            for client in this.client.room.clients.values():
                if this.client.playerSkills[61] >= count and client != this.client:
                    if client.posX >= this.client.posX - 400 and client.posX <= this.client.posX + 400:
                        if client.posY >= this.client.posY - 300 and client.posY <= this.client.posY + 300:
                            client.sendPlayerEmote(2, "", False, False)
                            count += 1
                else:
                    break

        elif emote == 8 and this.client.playerSkills.has_key(25):
            for client in this.client.room.clients.values():
                if this.client.playerSkills[25] >= count and client != this.client:
                    if client.posX >= this.client.posX - 400 and client.posX <= this.client.posX + 400:
                        if client.posY >= this.client.posY - 300 and client.posY <= this.client.posY + 300:
                            client.sendPlayerEmote(3, "", False, False)
                            count += 1
                else:
                    break

    def checkQualifiedPlayer(this, px, py, client):
        if not client.playerName == this.client.playerName and not client.isShaman:
            if client.posX >= px - 85 and client.posX <= px + 85:
                if client.posY >= py - 85 and client.posY <= py + 85:
                    return True
        return False

    def getShamanBadge(this):
        if this.client.equipedShamanBadge != 0:
            return this.client.equipedShamanBadge

        badgesCount = [0, 0, 0, 0, 0]

        for skill in this.client.playerSkills.items():
            if skill[0] > -1 and skill[0] < 14:
                badgesCount[0] += skill[1]
            elif skill[0] > 19 and skill[0] < 35:
                badgesCount[1] += skill[1]
            elif skill[0] > 39 and skill[0] < 55:
                badgesCount[2] += skill[1]
            elif skill[0] > 59 and skill[0] < 75:
                badgesCount[4] += skill[1]
            elif skill[0] > 79 and skill[0] < 95:
                badgesCount[3] += skill[1]

        return -(badgesCount.index(max(badgesCount)))
