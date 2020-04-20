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
                this.client.sendMessage("<ROSE>[INVOCATION] - <N>Usted posee: "+str(this.client.invocationpoints)+" items!")
            else:
                this.client.sendMessage("<ROSE>[INVOCATION] - <N>No hay artículos en este momento...")

    def sendMessageLoginAventura(this):
        this.client.sendMessage("<J>[EVENTO] <VP>Bienvenido al <CH>Evento de Aventura, <VP>"+str(this.client.playerName)+"!")
        this.client.sendMessage("<J>[EVENTO] <CH>¿Cómo funciona este evento? <N> Es simple, usted necesita recoger los elementos que aparecen en el mapa y entrar con él en la madriguera.")
        this.client.sendMessage("<J>[EVENTO] <N>Si usted firstea con el elemento del evento, ganará 7 firsts / monedas y acumulará el elemento en su perfil en <CH> Puntos de Aventura <N>, con 30/30 usted ganará medallas y títulos personalizados.")

    def sendMessageLoginTribewar(this):
        this.client.sendMessage("<N>[TRIBEWAR] <ROSE>-> Bienvenido a la sala: <N>#tribewar")

    def sendMessageLoginInvocation(this):
        this.client.sendMessage("<ROSE>[INVOCATION] - <N>Bienvenido a la sala <ROSE>#Invocation!")
        this.client.sendMessage("<ROSE>[INVOCATION] - <N>Apriete el espacio en el teclado para usar items")
        this.client.sendMessage("<ROSE>[INVOCATION] - <N>Usted posee: "+str(this.client.invocationpoints)+" items!")

    def ballonEventKeyboard(this, playerName, keyCode, down, xPlayerPosition, yPlayerPosition):
        if keyCode == 32:
            if this.client.ballons >= 1:
                this.client.spawnObject(28, xPlayerPosition+2, yPlayerPosition-25, 1)
                this.client.room.sendAll([8, 16], [this.client.playerCode])
                this.client.ballons -= 1
                this.client.sendMessage("<ROSE>[BALLON] - <N>Usted posee: "+str(this.client.ballons)+" ballons!")
            else:
                this.client.sendMessage("<ROSE>[BALLON] - <N>No tienes ballones, esperas...")

    def sendMessageLoginBallonRace(this):
        this.client.sendMessage("<ROSE>[BALLON] - <N>Bienvenido a la sala <ROSE>#BallonRace!")
        this.client.sendMessage("<ROSE>[BALLON] - <N>Apriete el espacio en su teclado para usar <ROSE>#Ballons.")
        this.client.sendMessage("<ROSE>[BALLON] - <N>Usted posee: "+str(this.client.ballons)+" ballon's!")

    def explosionEventKeyboard(this, playerName, keyCode, down, xPlayerPosition, yPlayerPosition):
        if keyCode == 32:
            if this.client.explosion >= 1:
                this.client.spawnObject(24, xPlayerPosition+4, yPlayerPosition+16, 0)
                this.client.explosion -= 1
                this.client.sendMessage("<ROSE>[EXPLOSION] - <N>Uste posee: "+str(this.client.explosion)+" explosion's!")
            else: this.client.sendMessage("<ROSE>[EXPLOSION] - <N>Usted no tiene explosión, espere...")

    def sendMessageLoginExplosion(this):
        this.client.sendMessage("<ROSE>[EXPLOSION] - <N>Bienvenido a la sala <ROSE>#Explosion!")
        this.client.sendMessage("<ROSE>[EXPLOSION] - <N>Apriete el espacio en su teclado para usar <ROSE>#Explosion.")
        this.client.sendMessage("<ROSE>[EXPLOSION] - <N>Usted posee: "+str(this.client.explosion)+" explosion's!")

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
        this.client.sendMessage("<ROSE>[POKELUA] - <N>Bienvenido a la sala <ROSE>#PokeLua!")
        this.client.sendMessage("<ROSE>[POKELUA] - <N>Poke Animes numeros: [Poke 0-50].")
        this.client.sendMessage("<ROSE>[POKELUA] - <N>Use el comando <ROSE>/poke (numero [0-50]).")

    def sendMessageLoginFly(this):
        this.client.sendMessage("<ROSE>[FLY] - <N>Bienvenido a la sala de <ROSE>#Fly!")
        this.client.sendMessage("<ROSE>[FLY] - <N>Aprieta el espacio en tu teclado para volar.")
        this.client.sendMessage("<ROSE>[FLY] - <N>Usted posee: "+str(this.client.flypoints)+" fly's.")           
