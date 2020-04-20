# -*- coding: cp1252 -*-
from datetime import datetime
import random
import time
import re
import logging
import json
import os
import urllib2
import xml.etree.ElementTree
import xml.parsers.expat
import sys, string, os, traceback
import struct
import math
import smtplib
import thread, threading
import time as thetime
#from requests import get
import ast
import exceptions
#import psutil
import string
import fnmatch
#modulos tornado & mysql
from DBUtils.PooledDB import PooledDB
import MySQLdb


Start = datetime.now()

print "[Elnas](Forums & Others) Cargado"
class Elnas:

	def __init__(this, server):
		this.server = server
		# this.Cursor = player.Cursor
		
		
################################################################################
########################	FUNCIONES GIVE ITEMS		########################
################################################################################
#	Estas funciones son usadas por Frodo y por CentralMice Forum
#	para editar el perfil de los usuarios conectados y desconectados


	# Players	: (LIST)	Lista con los nombres de usuarios a 
	# Amount 	: (INT) 	Cantidad de fresas a sumar/restar

	def shopFraises(this, players, amount):
		for playerName in players:
			player = this.server.players.get(playerName)
			if player != None:
				player.shopFraises += amount
			else:
				this.server.Cursor.execute("update Users set ShopFraises = ShopFraises+%s where Username = %s", [amount, playerName])
	def shopCheeses(this, players, amount):
		for playerName in players:
			player = this.server.players.get(playerName)
			if player != None:
				player.shopCheeses += amount
			else:
				this.server.Cursor.execute("update Users set shopCheeses = shopCheeses+%s where Username = %s", [amount, playerName])
	def prBootcamps(this, players, amount):
		for playerName in players:
			player = this.server.players.get(playerName)
			if player != None:
				player.bootcampCount += amount
			else:
				this.server.Cursor.execute("update Users set BootcampCount = BootcampCount+%s where Username = %s", [amount, playerName])
				
	def prFirst(this, players, amount):
		for playerName in players:
			player = this.server.players.get(playerName)
			if player != None:
				player.firstCount += amount
			else:
				this.server.Cursor.execute("update Users set FirstCount = FirstCount+%s where Username = %s", [amount, playerName])
	def prCheese(this, players, amount):
		for playerName in players:
			player = this.server.players.get(playerName)
			if player != None:
				player.cheeseCount += amount
			else:
				this.server.Cursor.execute("update Users set CheeseCount = CheeseCount+%s where Username = %s", [amount, playerName])
	def prSaves(this, players, amount):
		for playerName in players:
			player = this.server.players.get(playerName)
			if player != None:
				player.shamanSaves += amount
			else:
				this.server.Cursor.execute("update Users set ShamanSaves = ShamanSaves+%s where Username = %s", [amount, playerName])
	def prHardSaves(this, players, amount):
		for playerName in players:
			player = this.server.players.get(playerName)
			if player != None:
				player.hardModeSaves += amount
			else:
				this.server.Cursor.execute("update Users set HardModeSaves = HardModeSaves+%s where Username = %s", [amount, playerName])
	def prDivineSaves(this, players, amount):
		for playerName in players:
			player = this.server.players.get(playerName)
			if player != None:
				player.divineModeSaves += amount
			else:
				this.server.Cursor.execute("update Users set DivineModeSaves = DivineModeSaves+%s where Username = %s", [amount, playerName])
	def newReferido(this, players, amount):
		# Cuando un usuario recibe un nuevo referido (Amount es la cantidad de referidos)
		# se le suma las siguentes estadisticas al perfil
		# ademas de sumarsele la cantidad de referidos traidos
		for playerName in players:
			player = this.server.players.get(playerName)
			if player != None:
				player.shopFraises += 100*amount
				player.firstCount += 50*amount
				player.cheeseCount += 50*amount
				player.nowCoins += 1*amount
				player.referidos += 1*amount
				player.sendMessage('<font color="#88FF88">Tu referido ha subido de nivel, por tanto recibes '+str(100*amount)+' fresas, '+str(50*amount)+' first y '+str(1*amount)+' CentralCoin.</font> ')
			else:
				this.server.Cursor.execute("update Users set ShopFraises = ShopFraises+%s, FirstCount = FirstCount+%s, CheeseCount = CheeseCount+%s, Coins = Coins+%s , Referidos = Referidos+%s  where Username = %s", [100*amount, 50*amount, 50*amount, 1*amount, 1*amount, playerName])
	def oldReferido(this, players, amount, nivel = 0):
		# Cuando un usuario referido sube de nivel al referidor
		# solo se le suman ciertas estadisticas y no nuevos referidos
		puntos = nivel/2
		for playerName in players:
			player = this.server.players.get(playerName)
			if player != None:
				player.shopFraises += 100*amount
				player.firstCount += 5*amount
				player.cheeseCount += 5*amount
				player.nowCoins += 1*amount
				player.referidos += 1*puntos
				player.sendMessage('<font color="#88FF88">Has recibido '+str(100*amount)+' fresas, '+str(5*amount)+' first y '+str(1*amount)+' CentralCoin por referidos</font> ')
			else:
				this.server.Cursor.execute("update Users set ShopFraises = ShopFraises+%s, FirstCount = FirstCount+%s, CheeseCount = CheeseCount+%s, Coins = Coins+%s, Referidos = Referidos+%s  where Username = %s", [100*amount, 5*amount, 5*amount, 1*amount, 1*puntos, playerName])