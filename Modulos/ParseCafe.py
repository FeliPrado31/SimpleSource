#coding: utf-8
#Kaynak Geliştirici:Forsak3n
# Modules
from Utiles import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers

class Cafe:
    def __init__(this, player, server):
        this.client = player
        this.server = player.server
        this.CursorCafe = player.server.CursorCafe
    
    def loadCafeMode(this):
        can = this.client.privLevel >= 5 or (this.client.privLevel != 0 and this.client.cheeseCount >= 4000)
        if not can:
            this.client.sendMessage("<ROSE>Kafede konuşabilmek için 10 kez deliğe peynir götürmelisin.")
            #this.client.sendLangueMessage("", "<ROSE>$PasAutoriseParlerSurServeur")
        this.client.sendPacket(Identifiers.send.Open_Cafe, ByteArray().writeBoolean(can).toByteArray())

        packet = ByteArray()
        this.CursorCafe.execute("select * from CafeTopics where Langue = ? order by Date desc limit 0, 20", [this.client.langue])
        for rs in this.CursorCafe.fetchall():
            packet.writeInt(rs["TopicID"]).writeUTF(rs["Title"]).writeInt(this.server.getPlayerID(rs["Author"])).writeInt(rs["Posts"]).writeUTF(rs["LastPostName"]).writeInt(Utils.getSecondsDiff(rs["Date"]))
        this.client.sendPacket(Identifiers.send.Cafe_Topics_List, packet.toByteArray())

    def openCafeTopic(this, topicID):
        packet = ByteArray().writeBoolean(True).writeInt(topicID)
        this.CursorCafe.execute("select * from CafePosts where TopicID = ? order by PostID asc", [topicID])
        for rs in this.CursorCafe.fetchall():
            packet.writeInt(rs["PostID"]).writeInt(this.server.getPlayerID(rs["Name"])).writeInt(Utils.getSecondsDiff(rs["Date"])).writeUTF(rs["Name"]).writeUTF(rs["Post"]).writeBoolean(str(this.client.playerCode) not in rs["Votes"].split(",")).writeShort(rs["Points"])
        this.client.sendPacket(Identifiers.send.Open_Cafe_Topic, packet.toByteArray())

    def createNewCafeTopic(this, title, message):
        this.CursorCafe.execute("insert into CafeTopics values (null, ?, ?, '', 0, ?, ?)", [title, this.client.playerName, Utils.getTime(), this.client.langue])
        this.createNewCafePost(this.CursorCafe.lastrowid, message)
        this.loadCafeMode()

    def createNewCafePost(this, topicID, message):
        commentsCount = 0
        this.CursorCafe.execute("insert into CafePosts values (null, ?, ?, ?, ?, 0, ?)", [topicID, this.client.playerName, message, Utils.getTime(), this.client.playerCode])
        this.CursorCafe.execute("update CafeTopics set Posts = Posts + 1, LastPostName = ?, Date = ? where TopicID = ?", [this.client.playerName, Utils.getTime(), topicID])
        this.CursorCafe.execute("select count(*) as count from CafePosts where TopicID = ?", [topicID])
        rs = this.CursorCafe.fetchone()
        commentsCount = rs["count"]
        this.openCafeTopic(topicID)
        for player in this.server.players.values():
            if player.isCafe:
                player.sendPacket(Identifiers.send.Cafe_New_Post, ByteArray().writeInt(topicID).writeUTF(this.client.playerName).writeInt(commentsCount).toByteArray())

    def voteCafePost(this, topicID, postID, mode):
        points = 0
        votes = ""

        this.CursorCafe.execute("select Points, Votes from CafePosts where TopicID = ? and PostID = ?", [topicID, postID])
        rs = this.CursorCafe.fetchone()
        if rs:
            points = rs["Points"]
            votes = rs["Votes"]

        votes += str(this.client.playerID) if votes == "" else "," + str(this.client.playerID)
        if mode:
            points += 1
        else:
            points -= 1

        this.CursorCafe.execute("update CafePosts set Points = ?, Votes = ? where TopicID = ? and PostID = ?", [points, votes, topicID, postID])
        this.openCafeTopic(topicID)

    def deleteCafePost(this, topicID, postID):
        this.CursorCafe.execute("delete from CafePosts where TopicID = ? and PostID = ?", [topicID, postID])
        this.client.sendPacket(Identifiers.send.Delete_Cafe_Message, ByteArray().writeInt(topicID).writeInt(postID).toByteArray())
        this.openCafeTopic(topicID)

    def deleteAllCafePost(this, topicID, playerName):
        this.CursorCafe.execute("delete from CafePosts where TopicID = ? and Name = ?", [topicID, playerName])
        this.CursorCafe.execute("delete from CafeTopics where TopicID = ?", [topicID])
        this.loadCafeMode()
        this.openCafeTopic(topicID)
