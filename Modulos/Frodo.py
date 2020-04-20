#coding: utf-8
#Kaynak Geliştirici:Elnas
import re, time as _time

# Modules
from Utiles import Utils
from ByteArray import ByteArray

# Library
from collections import deque
from twisted.internet import reactor

    
class Frodo:
    def __init__(this, server):
        this.server = server
        this.bot = None
        
    def getFrodo(this):
        this.bot = this.server.players.get("Frodo")
        if this.bot != None:
            print "[Frodo] Connected"

    def logout(this):
        this.bot = None
        print "[Frodo] Logout"
        reactor.callLater(5, this.getFrodo)
    
    def parsePacket(this, packet):
        code = packet.readShort()
        if code == 1:
            referidor, ip1,ip2, playerName = packet.readUTF(),packet.readUTF(),packet.readUTF(),packet.readUTF()
            client = this.server.players.get(playerName)
            if client != None:
                print "["+playerName+"]",referidor, ip1,ip2 
                if client.nivel < 3:
                    client.referidor = referidor
                    client.fresasreferidos(referidor, ip1 != ip2)
                if  ip1 == ip2 :
                    packet = ByteArray().writeBoolean(client.nivel < 3).writeUTF(client.playerName).writeUTF(client.ipAddress).writeUTF(this.server.serverID)
                    this.sendPacket(2, packet.toByteArray())
        elif code == 2:
            keep = packet.readBoolean()
            cantidad = packet.readInt()
            if not keep: this.server.blackList = []
            for x in range(cantidad):
                site = packet.readUTF()
                this.server.blackList.append(site)
            this.server.log("[Frodo] Backlist: "+str(len(this.server.blackList))+" Sitios")
        elif code == 3:
            keep = packet.readBoolean()
            cantidad = packet.readInt()
            if not keep: this.server.whiteList = []
            for x in range(cantidad):
                site = packet.readUTF()
                this.server.whiteList.append(site)
            this.server.log("[Frodo] WhiteList: "+str(len(this.server.whiteList))+" Sitios")
        
    def sendPacket(this, code, packet):
        if this.bot != None:
            this.bot.sendPacket([24,code], packet)
            # try:this.bot.sendPacket([Identifiers.frodo.C,code], packet)
            # except:pass
    def checkReferido(this, client):
        packet = ByteArray().writeUTF(client.playerName).writeUTF(client.ipAddress).writeUTF(this.server.serverID)
        this.sendPacket(1, packet.toByteArray())
    def new(this):
        pass