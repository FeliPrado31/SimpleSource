# -*- coding: utf-8 -*-
import random, time, struct
from twisted.internet import reactor
from ByteArray import ByteArray
class Games:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        this.Cursor = client.Cursor
        this.deathBallonTime = time.time()

    def InvocationEventKeyboard(this, playerName, keyCode, down, xPlayerPosition, yPlayerPosition):
        if keyCode == 32:
            if this.client.invocationpoints >= 1:
                item = [28, 1, 2, 29, 30, 31, 32, 33, 34, 35, 3, 4]
                id = random.choice(item)
                this.client.spawnObject(id, xPlayerPosition+4, yPlayerPosition+16, 1)
                this.client.invocationpoints -= 1
                this.client.sendMessage("<CH>[INVOCATION] - <N>Kalan: "+str(this.client.invocationpoints)+" item hakkiniz!")
            else:
                this.client.sendMessage("<CH>[INVOCATION] - <N>Hiç öğeniz yok, lütfen bekleyin...")

    def sendMessageLoginAventura(this):
        this.client.sendMessage("<J>[StorMice Module] <VP>Hos geldiniz <CH>Event Maceraya, <VP>"+str(this.client.playerName)+"!")
        this.client.sendMessage("<J>[StorMice Module] <CH>Bu olay nasil isliyor? <N>Çok basit, haritada görünen öğeleri yakalamaniz ve deliğe girmeniz gerekiyor.")
        this.client.sendMessage("<J>[StorMice Module] <N>Etkinlik maddesiyle ilk önce siz ilk önce 100 adet ilk first kazanirsiniz ve öğeyi profilinizde biriktirirsiniz. <CH>Macera Puani<N>, 30/30 ile madalyalari ve kisisellestirilmis basliklari kazanacaksiniz.")

    def sendMessageLoginTribewar(this):
        this.client.sendMessage("<N>[TRIBEWAR] <CH>-> Hos Geldiniz! <N>#tribewar")
        this.client.sendMessage("<N>[TRIBEWAR] <CH>-> Siralamaya Bakmak Icin: <N>/ranktribewar")

    def sendMessageLoginInvocation(this):
        this.client.sendMessage("<CH>[INVOCATION] - <N>Hos Geldiniz <CH>#Invocation!")
        this.client.sendMessage("<CH>[INVOCATION] - <N>Öğeleri kullanmak için klavyenizdeki bosluğa basin")
        this.client.sendMessage("<CH>[INVOCATION] - <N>Kalan: "+str(this.client.invocationpoints)+" item hakkiniz!")

    def sendMessageLoginDeath(this):
        this.client.room.bindKeyBoard(this.client.playerName, 3, False, this.client.room.isDeathmatch)
        this.client.room.bindKeyBoard(this.client.playerName, 32, False, this.client.room.isDeathmatch)
        this.client.room.bindKeyBoard(this.client.playerName, 79, False, this.client.room.isDeathmatch)
        this.client.room.bindKeyBoard(this.client.playerName, 80, False, this.client.room.isDeathmatch)
        this.client.sendMessage("<VP>Hos Geldiniz <J>#Deathmatch!")
        this.client.sendMessage("<VP>Drag Atmayi Aktiflestirmek Icin <J>1'e <VP>basmalisiniz <J>#Deathmatch!")
        this.client.sendMessage("<VP>Yeni Deathmatch<J> Siralamamiza <VP>Göz Atmak için <J>/rankingdeath <VP>yazmaniz yeterli")
        this.client.sendMessage("<CH>Deathmatch Hakkinda:\n<CH>Profil Görmek Icin:<N> (P)'ye Basin <J>\n<CH>Drag Görüntüsü Icin:<N> (O)<J>'ya Basin")

    def deathEventKeyboard(this, _player, key, down, x, y):
        if key == 3 or key == 32 and not this.client.isDead and this.client.PlayerDeathVivo == True:										
            if not this.client.canCN:
                this.client.room.objectID += 1
                idCannon = {15: "149aeaa271c.png", 16: "149af112d8f.png", 17: "149af12c2d6.png", 18: "149af130a30.png", 19: "149af0fdbf7.png", 20: "149af0ef041.png", 21: "149af13e210.png", 22: "149af129a4c.png", 23: "149aeaa06d1.png"}
                if not this.client.isDead:
                    if str(this.client.mDirection) == "0":
                        posXLeft = x+4
                        posYLeft = y+8
                        if this.client.deathStats[0] == 2 and this.client.deathStats[1] == 8:
                            this.client.addShamanObject(1704, int(posXLeft), int(posYLeft), int(1),-90)
                            reactor.callLater(2, this.client.room.removeObject, 1704)
                        else:
                            x = int(posXLeft+this.client.deathStats[0]) if this.client.deathStats[0] < 0 else int(posXLeft+this.client.deathStats[0])
                            y = int(posYLeft+this.client.deathStats[1]) if this.client.deathStats[1] < 0 else int(posYLeft+this.client.deathStats[1])
                            this.client.sendPlaceObjectDeath(this.client.room.objectID, 17, x, y, -90, 0, 0, True, True)
                            reactor.callLater(2, this.client.room.removeObject, this.client.room.objectID)
                            if this.client.deathStats[4] in [15, 16, 17, 18, 19, 20, 21, 22, 23]:
                                if not this.client.deathStats[3] == 1:
                                    this.client.room.sendAll([29, 19], ByteArray().writeInt(this.client.playerCode).writeUTF(idCannon[this.client.deathStats[4]]).writeByte(1).writeInt(this.client.room.objectID).toByteArray()+"\xff\xf0\xff\xf0")
                if not this.client.isDead:
                    if str(this.client.mDirection) == "1":
                        posXRight = x-8
                        posYRight = y+4
                        if this.client.deathStats[0] == 2 and this.client.deathStats[1] == 8:  
                            this.client.addShamanObject(1704, int(posXRight), int(posYRight), int(1),90)
                            reactor.callLater(2, this.client.room.removeObject, 1704)
                        else:
                            x = int(posXRight+this.client.deathStats[0]) if this.client.deathStats[0] < 0 else int(posXRight+this.client.deathStats[0])
                            y = int(posYRight+this.client.deathStats[1]) if this.client.deathStats[1] < 0 else int(posYRight+this.client.deathStats[1])
                            this.client.sendPlaceObjectDeath(this.client.room.objectID, 17, x, y, 90, 0, 0, True, True)
                            reactor.callLater(2, this.client.room.removeObject, this.client.room.objectID)
                            if this.client.deathStats[4] in [15, 16, 17, 18, 19, 20, 21, 22, 23]:
                                if not this.client.deathStats[3] == 1:
                                    this.client.room.sendAll([29, 19], ByteArray().writeInt(this.client.playerCode).writeUTF(idCannon[this.client.deathStats[4]]).writeByte(1).writeInt(this.client.room.objectID).toByteArray()+"\xff\xf0\xff\xf0")

                this.client.canCN = True
                this.canCCN = reactor.callLater(0.7, this.client.cnTrueOrFalse) 


    def ballonEventKeyboard(this, playerName, keyCode, down, xPlayerPosition, yPlayerPosition):
        if keyCode == 32:
            if this.client.ballons >= 1:
                this.client.spawnObject(28, xPlayerPosition+2, yPlayerPosition-25, 1)
                this.client.room.sendAll([8, 16], [this.client.playerCode])
                this.client.ballons -= 1
                this.client.sendMessage("<CH>[BALLON] - <N>Você possui: "+str(this.client.ballons)+" ballons!")
            else:
                this.client.sendMessage("<CH>[BALLON] - <N>Você não possui ballons, aguarde...")       

    def sendMessageLoginBallonRace(this):
        this.client.sendMessage("<CH>[BALLON] - <N>Hos Geldiniz <CH>#BallonRace!")
        this.client.sendMessage("<CH>[BALLON] - <N>Balon Malzemesi Kullanmak Icin Space Basmaniz Yeterli <CH>#Ballons.")
        this.client.sendMessage("<CH>[BALLON] - <N>Kalan: "+str(this.client.ballons)+" balon hakkiniz!")

    def sendMessageLoginLegendsRace(this):
        this.client.sendMessage("<font color='#2DA2FB'>[LegendsRace]</font> - <N>Hos Geldiniz <font color='#2DA2FB'>#LegendsRace.</font>")
        this.client.sendMessage("<font color='#2DA2FB'>[LegendsRace]</font> - <N>Bu odanin amaci kiran kirana bir mucadele vermektir <font color='#2DA2FB'>#LegendsRace.</font>")
        this.client.sendMessage("<font color='#2DA2FB'>[LegendsRace]</font> - <N>Sureniz 35 Saniyedir. <font color='#2DA2FB'>#LegendsRace</font>")
        this.client.sendMessage("<font color='#2DA2FB'>[LegendsRace]</font> - <N>Bu Sure Zarfında Eger Ustun Gelirseniz Buyuk Bir Miktar Odul Kazanicaksiniz. <font color='#2DA2FB'>#LegendsRace.</font>.")
        this.client.sendMessage("<font color='#2DA2FB'>[LegendsRace]</font> - <N>Her 1.Giris 500 First'dir <font color='#2DA2FB'>#LegendsRace.</font>")

    def explosionEventKeyboard(this, playerName, keyCode, down, xPlayerPosition, yPlayerPosition):
        if keyCode == 32:
            if this.client.explosion >= 1:
                this.client.spawnObject(24, xPlayerPosition+4, yPlayerPosition+16, 0)
                this.client.explosion -= 1
                this.client.sendMessage("<CH>[EXPLOSION] - <N>Kalan: "+str(this.client.explosion)+" sp hakkiniz!")
            else: this.client.sendMessage("<CH>[EXPLOSION] - <N>Sp'n yok, lütfen bekle ...")

    def sendMessageLoginExplosion(this):
        this.client.sendMessage("<CH>[EXPLOSION] - <N>HOs Geldiniz <CH>#Explosion!")
        this.client.sendMessage("<CH>[EXPLOSION] - <N>Sp Kullanabilmek Icin Space Basiniz <CH>#Explosion.")
        this.client.sendMessage("<CH>[EXPLOSION] - <N>Kalan: "+str(this.client.explosion)+" sp hakkiniz!")

    def pokeEventKeyboard(this, player, key, down, x, y):
        if key == 39:
            # Posição Direita
            this.client.room.addImage(0, this.client.pokeSelect[0], 3, this.client.playerCode, -26, -45, "")
            this.client.room.removeImage(1, "")
        elif key == 37:
            this.client.room.addImage(1, this.client.pokeSelect[1], 3, this.client.playerCode, -26, -45, "")
            this.client.room.removeImage(0, "")
            # Posição Esquerda
            
    def pokeCommand(this, pokemon):
        if this.client.pokeList.has_key(pokemon):
            this.client.pokeSelect = this.client.pokeList[pokemon]
            
    def sendMessageLoginPokeLua(this):
        this.client.sendMessage("<CH>[POKELUA] - <N>Hos Geldiniz <CH>#PokeLua!")
        this.client.sendMessage("<CH>[POKELUA] - <N>Poke Anime Sinir: [Poke 0-50].")
        this.client.sendMessage("<CH>[POKELUA] - <N>Kullanabilmek icin <CH>/poke 1 <N>yazmaniz yeterli")

    def sendMessageLoginFly(this):
        this.client.sendMessage("<CH>[FLY] - <N>Hos Geldiniz <CH>#Fly!")
        this.client.sendMessage("<CH>[FLY] - <N>Uçmak Icin Space Basmaniz Yeterli.")
        this.client.sendMessage("<CH>[FLY] - <N>Kalan: "+str(this.client.flypoints)+" hakkiniz.")           
