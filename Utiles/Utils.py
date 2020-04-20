# coding: utf-8
import re, time, random, string, time as thetime

# Library
from datetime import datetime

class Utils:
    @staticmethod
    def getTFMLangues(langueID):
        return {0:"en", 1:"fr", 2:"fr", 3:"br", 4:"es", 5:"cn", 6:"tr", 7:"vk", 8:"pl", 9:"hu", 10:"nl", 11:"ro", 12:"id", 13:"de", 14:"e2", 15:"ar", 16:"ph", 17:"lt", 18:"jp", 19:"ch", 20:"fi", 21:"cz", 22:"sk", 23:"hr", 24:"bu", 25:"lv", 26:"he", 27:"it", 29:"et", 30:"az", 31:"pt"}[langueID]
		
    @staticmethod
    def getTime():
        return int(long(str(time.time())[:10]))

    @staticmethod
    def getRanks(*array):
        return {
           13: "<font color='#00EEFF'>Programmer</font>",
           12: "<font color='#FFBF00'>Fundador</font>",
           11: "<font color='#00FF15'>Supervisor</font>",
           10: "<font color='#FFFF00'>Administrador</font>",
           9: "<ROSE>Coordinador<N>",
           8: "<J>Super Moderador<N>",
           7: "<font color='#ffaa22'>Moderador</font>",
           6: "<font color='#00FFFF'>MapCrew</font>",
           5: "VIP Gold",
           4: "cont",
           3: "VIP Pro",
           2: "VIP",
           1: "Player",
           0: "Message Serveur"
           }

    @staticmethod
    def getRanksColor(*array):
        return {
           13: ["<font color='#00EEFF'>","</font>"],
           12: ["<font color='#FFBF00'>","</font>"],
           11: ["<font color='#00FF15'>","</font>"],
           10: ["<font color='#FFFF00'>","</font>"],
           9: ["<ROSE>","<N>"],
           8: ["<J>","<N>"],
           7: ["<font color='#ffaa22'>","</font>"],
           6: ["<font color='#00FFFF'>","</font>"],
           5: ["",""],
           4: ["",""],
           3: ["",""],
           2: ["",""],
           1: ["",""],
           0: ["",""]
           }

    @staticmethod
    def getRankNames(*array):
        return {
           13: "Programmer",
           12: "Fundador",
           11: "Supervisor",
           10: "Administrador",
           9: "Coordinador",
           8: "Super Moderador",
           7: "Moderador",
           6: "MapCrew",
           5: "cont",
           4: "cont",
           3: "cont",
           2: "cont",
           1: "Player",
           0: "Serveur"
           }

    @staticmethod
    def getValue(*array):
        return random.choice(array)

    @staticmethod
    def binarizar(decimal):
        binario = ''
        while decimal // 2 != 0:
            binario = str(decimal % 2) + binario
            decimal = decimal // 2
        return str(decimal) + binario
		
    @staticmethod
    def getHoursDiff(endTimeMillis):
        startTime = Utils.getTime()
        startTime = datetime.fromtimestamp(float(startTime))
        endTime = datetime.fromtimestamp(float(endTimeMillis))
        result = endTime - startTime
        seconds = (result.microseconds + (result.seconds + result.days * 24 * 3600) * 10 ** 6) / float(10 ** 6)
        hours = int(int(seconds) / 3600) + 1
        return hours
    
    @staticmethod
    def getDiffDays(time):
        diff = time - Utils.getTime()
        return diff / (24 * 60 * 60)

    @staticmethod
    def getSecondsDiff(endTimeMillis):
        return int(long(str(thetime.time())[:10]) - endTimeMillis)

    @staticmethod
    def getRandomChars(size):
        return "".join(random.choice(string.digits + string.ascii_uppercase + string.ascii_lowercase) for x in range(size))

    @staticmethod
    def getDaysDiff(endTimeMillis):
        startTime = datetime.fromtimestamp(float(Utils.getTime()))
        endTime = datetime.fromtimestamp(float(endTimeMillis))
        result = endTime - startTime
        return result.days + 1

    @staticmethod
    def parsePlayerName(playerName):
        return (playerName[0] + playerName[1:].lower().capitalize()) if playerName.startswith("*") or playerName.startswith("+") else playerName.lower().capitalize()

    @staticmethod
    def joinWithQuotes(list):
        return "\"" + "\", \"".join(list) + "\""

    @staticmethod
    def getYoutubeID(url):
        matcher = re.compile(".*(?:youtu.be\\/|v\\/|u\\/\\w\\/|embed\\/|watch\\?v=)([^#\\&\\?]*).*").match(url)
        return matcher.group(1) if matcher else None

    @staticmethod
    def Duration(duration):
        time = re.compile('P''(?:(?P<years>\d+)Y)?''(?:(?P<months>\d+)M)?''(?:(?P<weeks>\d+)W)?''(?:(?P<days>\d+)D)?''(?:T''(?:(?P<hours>\d+)H)?''(?:(?P<minutes>\d+)M)?''(?:(?P<seconds>\d+)S)?'')?').match(duration).groupdict()
        for key, count in time.items():
            time[key] = 0 if count is None else time[key]
        return (int(time["weeks"]) * 7 * 24 * 60 * 60) + (int(time["days"]) * 24 * 60 * 60) + (int(time["hours"]) * 60 * 60) + (int(time["minutes"]) * 60) + (int(time["seconds"]) - 1)

    @staticmethod
    def getUptime(time):
        text = ""
        time = str(time).split(".")[0].split(":")
        hours = time[0]
        minutes = time[1]
        seconds = time[2]

        minutes = minutes.replace("00", "0") if minutes == "00" else minutes.replace("0", "") if len("0") == 1 and not minutes in ["10", "20", "30", "40", "50", "60"] else minutes
        seconds = seconds.replace("00", "0") if seconds == "00" else seconds.replace("0", "") if len("0") == 1 and not seconds in ["10", "20", "30", "40", "50", "60"] else seconds
        if hours > "0": text += hours + (" hours " if hours > "1" else " hour ")
        if minutes > "0": text += minutes + (" minutes " if minutes > "1" else " minute ")
        if seconds > "0": text += seconds + (" seconds " if seconds > "1" else " second ")
        return text
