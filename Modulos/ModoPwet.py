#coding: utf-8
# Modules
import traceback,time as _time, os
from Utiles import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers

class ModoPwet:
	def __init__(this, player, server):
		this.client = player
		this.server = player.server

	def makeReport(this, playerName, type, comments):
		playerName = Utils.parsePlayerName(playerName)

		if playerName in this.server.reports["names"]:
			this.server.reports[playerName]["types"].append(str(type))
			this.server.reports[playerName]["reporters"].append(this.client.playerName)
			this.server.reports[playerName]["comments"].append(comments)
			this.server.reports[playerName]["status"] = "online" if this.server.checkConnectedAccount(playerName) else "disconnected"
		else:
			this.server.reports["names"].append(playerName)
			this.server.reports[playerName] = {}
			this.server.reports[playerName]["types"] = [str(type)]
			this.server.reports[playerName]["reporters"] = [this.client.playerName]
			this.server.reports[playerName]["comments"] = [comments]
			this.server.reports[playerName]["status"] = "online" if this.server.checkConnectedAccount(playerName) else "disconnected"
			this.server.reports[playerName]["langue"] = this.getModopwetLangue(playerName)

		this.updateModoPwet()
		this.client.sendBanConsideration()

	def getModopwetLangue(this, playerName):
		player = this.server.players.get(playerName)
		return player.langue if player != None else "en"

	def updateModoPwet(this):
		for player in this.server.players.values():
			if player.isModoPwet and player.privLevel >= 7:
				player.modoPwet.openModoPwet()

	def getPlayerRoomName(this, playerName):
		player = this.server.players.get(playerName)
		return player.roomName if player != None else "0"

	def getProfileCheeseCount(this, playerName):
		player = this.server.players.get(playerName)
		return player.cheeseCount if player != None else 0

	def openModoPwet(this):
		try:
			text = str(open('./Modulos/pixs/modopw/open.pix', 'r').read()) #Permite editar comandos sin reiniciar el server, desde el archivo ParseCommands.pix
			exec text
		except Exception as ERROR:
			with open("./CentralmiceES/Logs/Errores/SErrores.log", "a") as f:
				f.write("\n" + "=" * 60 + "\n- Time: %s\n- Player: %s\n- Error Command: \n" %(_time.strftime("%d/%m/%Y - %H:%M:%S"), this.client.playerName))
				traceback.print_exc(file = f)
				f.write("\n")

	def changeReportStatusDisconnect(this, playerName):
		this.client.sendPacket(Identifiers.send.Modopwet_Disconnected, ByteArray().writeUTF(playerName).toByteArray())

	def changeReportStatusDeleted(this, playerName, deletedby):
		this.client.sendPacket(Identifiers.send.Modopwet_Deleted, ByteArray().writeUTF(playerName).writeUTF(deletedby).toByteArray())

	def changeReportStatusBanned(this, playerName, banhours, banreason, bannedby):
		this.client.sendPacket(Identifiers.send.Modopwet_Banned, ByteArray().writeUTF(playerName).writeUTF(bannedby).writeInt(int(banhours)).writeUTF(banreason).toByteArray())

	def openChatLog(this, playerName):
		packet = ByteArray().writeUTF(playerName).writeByte(len(this.server.chatMessages[playerName]) * 2 if this.server.chatMessages.has_key(playerName) else 0)
		if this.server.chatMessages.has_key(playerName):
			for message in this.server.chatMessages[playerName]:
				packet.writeUTF(message[0]).writeUTF(message[1])                        
		this.client.sendPacket(Identifiers.send.Modopwet_Chatlog, packet.toByteArray())
