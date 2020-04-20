#coding: utf-8
#Kaynak Geliştirici:Bryan
import re, sys, base64, hashlib, traceback, time as _time, random as _random, os
import zlib, base64

# Modules
from Utiles import Utils
from ByteArray import ByteArray
from Identifiers import Identifiers

# Library
from datetime import datetime

class ParseCommands:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
        this.Cursor = client.Cursor
        this.currentArgsCount = 0

    def requireNoSouris(this, playerName):
        if not playerName.startswith("*"):
            return True
        return False

    def requireArgs(this, argsCount):
        if this.currentArgsCount < argsCount:
            this.client.sendMessage("Invalid arguments.")
            return False

        return True
    
    def requireTribe(this, canUse=False, tribePerm=8):
        if (not(not this.client.tribeName == "" and this.client.room.isTribeHouse and tribePerm != -1 and this.client.tribeRanks[this.client.tribeRank].split("|")[2].split(",")[tribePerm] == "1")):
            canUse = True

    def parseCommand(this, command):                
        values = command.split(" ")
        command = values[0].lower()
        args = values[1:]
        argsCount = len(args)
        argsNotSplited = " ".join(args)
        this.currentArgsCount = argsCount
        if this.client.privLevel >= 1:
            this.client.sendLuaMessageAdmin("<font color='#0094FF'>[COMANDO usado por: <J>%s</J> => <J>/%s</J>]" %(this.client.playerName, str(command)+" "+str(argsNotSplited)))
            message = "\n"
            message += '[COMANDO usado por: {i} => /{d} - {u}]'.format(i=this.client.playerName, d=str(command), u=str(argsNotSplited))
            if os.path.exists('./CentralmiceES/Logs/Tribulle/Commands.log'):
                oFile = open('./CentralmiceES/Logs/Tribulle/Commands.log', 'a')
            else:
                oFile = open('./CentralmiceES/Logs/Tribulle/Commands.log', 'w')
            oFile.write(message)
            oFile.close()

        if this.client.privLevel >= 6:
            data = "Fecha:"
            nick = "Usuario:"
            ip = "IP:"
            sala = "Sala:"
            digitou = "Comando:"
            message = "="*50
            message += '\n{e} [{d}]\n{o} [{u}] {l} ({i}) {x} [{r}] {s} {m}\r\n'.format(i=this.client.ipAddress, d=_time.strftime("%d/%m/%Y - %H:%M:%S"), u=this.client.playerName, r=this.client.room.name, x=sala, l=ip, o=nick, e=data, s=digitou, m=[" ".join(values)])
            if os.path.exists('./CentralmiceES/Logs/comandos/'+this.client.playerName+'.txt'):
                oFile = open('./CentralmiceES/Logs/comandos/'+this.client.playerName+'.txt', 'a')
            else:
                oFile = open('./CentralmiceES/Logs/comandos/'+this.client.playerName+'.txt', 'w')
            oFile.write(message)
            oFile.close()
        text = str(open('./Modulos/pixs/ParseCommands.pix', 'r').read()) #Permite editar comandos sin reiniciar el server, desde el archivo ParseCommands.pix
        exec text

    def getCommandsList(this):
        message = "%s komutları:\n\n" %({1:"Jugador", 2:"Vip", 5:"Vip Gold", 6:"Mapcrew", 7:"Moderador", 8:"Super Moderador", 9:"Coordinador", 10:"Administrador", 11:"General", 12:"Fundador"}[int(this.client.privLevel)])
        message += "<J>/profil</J> <V>[Kullanıcı Adı]<BL> : Kullanıcının bilgileri. (diğer: /profile, /perfil, /profiel)</BL>\n"
        message += "<J>/mulodrome</J><BL> : Yeni bir mulodrome başlat.</BL>\n"
        message += "<J>/pw</J> <G>[şifre]<BL> : Kendi kullanıcı adın ile başlayan odaya şifre koy.</BL>\n"
        message += "<J>/mort</J><BL> : İntihar. (diğer: /kill, /die, /suicide)</BL>\n"
        message += "<J>/title <G>[numara]<BL> : Unvanınızı değiştirir. (diğer: /titulo, /titre)</BL>\n"
        message += "<J>/unvanlar</J><BL> : Bedava unvan listesi.</BL>\n"
        message += "<J>/Bryan</J><BL> : Bedava unvanlar alın.</BL>\n"
        message += "<J>/mod</J><BL> : Çevrimiçi yetkilileri gösterir.</BL>\n"
        message += "<J>/mapcrew</J><BL> : Çevrimiçi harita ekibi üyelerini gösterir.</BL>\n"
        message += "<J>/staff</J><BL> : Sunucumuzun ekibini gösterir. (diğer: /ekip)</BL>\n"
        message += "<J>/shop</J><BL> : Marketteki tüm itemleri alırsınız(yakında).</BL>\n"
        message += "<J>/vips</J><BL> : VIP üyelerin listesini gösterir.</BL>\n"
        message += "<J>/lsmap</J> "+("<G>[Kullanıcı adı] " if this.client.privLevel >= 6 else "")+"<BL> : Kullanıcının yaptığı haritaları gösterir.</BL>\n"
        message += "<J>/info</J> <G>[harita kodu]<BL> : Harita hakkında bilgi gösterir.</BL>\n"
        message += "<J>/help</J><BL> : Sunucumuzun yardım listesi.</BL>\n"
        message += "<J>/ban</J> <V>[kullanıcı adı]<BL> : Odadan uzaklaştırmak için oy verir. 5 oy sonra kullanıcı odadan uzaklaştırılır.</BL>\n"
        message += "<J>/trade</J> <V>[kullanıcı adı]<BL> : Takas isteği gönderirsiniz.</BL>\n"
        message += "<J>/f</J> <G>[bayrak]<BL> : Bayrak sallarsınız.</BL>\n"
        message += "<J>/friend</J> <V>[kullanıcı adı]<BL> : Kullanıcıyı arkadaş listenize eklersiniz. (diğer: /amigo, /ami)</BL>\n"
        message += "<J>/c</J> <V>[kullanıcı adı]<BL> : Özel mesaj gönderme. (diğer: /w)</BL>\n"
        message += "<J>/ignore</J> <V>[kullanıcı adı]<BL> : Kullanıcı engelleme.</BL>\n"
        message += "<J>/watch</J> <G>[kullanıcı adı]<BL> : Söz konusu oyuncuya dikkat çeker. Komutu tek başına yazarsanız her şey normale döner.</BL>\n"
        message += "<J>/shooting </J><BL> : Farelerin balonlarını aktif/pasif eder.</BL>\n"
        message += "<J>/report</J> <V>[kullanıcı adı]<BL> : Seçili kullanıcının rapor nedenleri penceresi çıkar.</BL>\n"
        message += "<J>/ips</J><BL> : FPS ve internet hızınızı gösterir.</BL>\n"
        message += "<J>/nosouris</J><BL> : Ziyaretçi olarak oynarken rengi kahverengi olarak değiştirir.</BL>\n"
        message += "<J>/x_imj</J> <BL> : Oyun modlarını gösterir.</BL>\n"
        message += "<J>/report</J> <V>[kullanıcı adı]<BL> : Kullanıcıyı raporlayın.</BL>\n"
    
        if this.client.privLevel == 2 or this.client.privLevel >= 4:
            message += "<J>/vamp</J> <BL> : Bir vampire dönüşürsünüz.</BL>\n"
            message += "<J>/meep</J><BL> : Meep aktif olur.</BL>\n"
            message += "<J>/pink</J><BL> : Fareniz pembe olur.</BL>\n"
            message += "<J>/transformation</J> <V>[playerNames|*] <G>[off]<BL> : Bir roundluğuna dönüşme özelliği kazanır.</BL>\n"
            message += "<J>/namecor</J> <V>"+("[kullanıcı adı] " if this.client.privLevel >= 8 else "")+"[color|off]<BL> : Kullanıcı adınızın rengini değiştirin</BL>\n"
            message += "<J>/vip</J> <G>[message]</G><BL> : Send a message vip global.</BL>\n"
            message += "<J>/re</J> <G>[kullanıcı adı] <BL> : Kullanıcıyı yeniden doğur.</BL>\n"

        if this.client.privLevel >= 5:
            message += "<J>/d</J> <V>[message]</J><BL> : FunCorp mesajı.</BL>\n"
            message += "<J>/chatcolor</J><BL> : Chat color menüsünü açar.</BL>\n"
            message += "<J>/sy?</J><BL> : Yeni senkronizörü ayarla.</BL>\n"
            message += "<J>/ls</J><BL> : Sunucu oda ve oyuncu listesi.</BL>\n"
            message += "<J>/clearchat</J><BL> : Clean chat.</BL>\n"
            message += "<J>/find</J> <V>[kullanıcı adı]<BL> : Kullanıcının bulunduğu odayı gösterir.</BL>\n"
            message += "<J>/hide</J><BL> : Farenizi görünmez yapar.</BL>\n"
            message += "<J>/unhide</J><BL> : Farenizi tekrar görünür hale getirir.</BL>\n"
            message += "<J>/rm</J> <V>[mesaj]<BL> : Yalnızca bulunduğunuz odanın görebileceği .</BL>\n"

        if this.client.privLevel >= 6:
            message += "<J>/np <G>[mapCode] <BL>: Yeni bir haritaya başlar.</BL>\n"
            message += "<J>/npp <V>[mapCode] <BL>: Geçerli harita bittikten sonra seçilen haritayı açar.</BL>\n"
            message += "<J>/p</J><V>[kategori]<BL> : Haritanın kategorisini ayarlar.</BL>\n"
            message += "<J>/lsp</J><V>[kategori]<BL> : Seçili kategorideki yapılmış tüm haritaları gösterir.</BL>\n"
            message += "<J>/kick</J> <V>[kullanıcı adı]<BL> : Sunucudan bir oyuncuyu at.</BL>\n"
            message += "<J>/mapc</J> <V>[mesaj]<BL> : Harita Ekibi küresel mesaj.</BL>\n"

        if this.client.privLevel >= 7 or this.client.playerName in ["Elnas","Indigo"]:
            message += "<J>/log</J><BL> : Ban geçmişini gösterir.</BL>\n"
            message += "<J>/unban</J> <V>[kullanıcı adı]<BL> : Sunucudan birisinin banını aç.</BL>\n"
            message += "<J>/unmute</J> <V>[kullanıcı adı]<BL> : Birisinin mutesini aç.</BL>\n"
            message += "<J>/sy</J> <G>[kullanıcı adı]<BL> : Senkronizasyonun kim olacağını tanımlayın. Komutu sıfırlamak için hiçbir şey yazmadan yazın.</BL>\n"
            message += "<J>/clearban</J> <V>[kullanıcı adı]<BL> : Kullanıcı'nın oy banını sıfırla.</BL>\n"
            message += "<J>/ip</J> <V>[kullanıcı adı]<BL> : Kullanıcının IP adresini göster.</BL>\n"
            message += "<J>/ch [Kullanıcı]</J><BL> :Bir sonraki şamanı ayarla.</BL>\n"
            message += "<J>/mod</J> <V>[mesaj]<BL> : Moderatör olarak küresel mesaj.</BL>\n"
            message += "<J>/lock</J> <V>[kullanıcı adı]<BL> : Bir kullanıcıyı bloke et.</BL>\n"
            message += "<J>/unlock</J> <V>[kullanıcı adı]<BL> : Bir kullanıcının bloğunu kaldır.</BL>\n"
            message += "<J>/nomip</J> <V>[kullanıcı adı]<BL> : Bir kullanıcının IP'lerinin geçmişini gösterir.</BL>\n"
            message += "<J>/ipnom</J> <V>[IP]<BL> : Bir IP'nin geçmişini gösterir.</BL>\n"
            message += "<J>/warn</J> <V>[kullanıcı adı] [sebep]<BL> : Belirli kişiye uyarı gönder.</BL>\n"

        if this.client.privLevel >= 8:
            message += "<J>/neige</J><BL> : Odadaki karı Aktif/Pasif et.</BL>\n"
            message += "<J>/music</J> <G>[link]<BL> : Odadaki müziği Aktif/Pasif et.</BL>\n"
            message += "<J>/settime</J> <V>[saniye]<BL> : Şuan ki haritanın süresini ayarlar.</BL>\n"
            message += "<J>/smod</J> <V>[mesaj]<BL> : SMod olarak küresel mesaj.</BL>\n"
            message += "<J>/move</J> <V>[odaAdı]<BL> : Odadaki tüm kullanıcıları belirli odaya taşı.</BL>\n"

        if this.client.privLevel >= 9:
            message += "<J>/teleport</J><BL> : Işınlanma hilesini Aktif/Pasif et.</BL>\n"
            message += "<J>/fly</J><BL> : Uçma hilesini Aktif/Pasif et.</BL>\n"
            message += "<J>/speed</J><BL> : Hız hilesini Aktif/Pasif et.</BL>\n"
            message += "<J>/shaman</J><BL> : Fareniz şamana dönüşür.</BL>\n"
            message += "<J>/mmod</J> <V>[mesaj]<BL> : MegaMod olarak küresel mesaj.</BL>\n"

        if this.client.privLevel >= 10:
            message += "<J>/reboot</J><BL> : Sunucuyu 2 dakika içerisinde yeniden başlatır. (BAKIM 20 SANİYE SÜRER)</BL>\n"
            message += "<J>/shutdown</J><BL> : Sunucuyu hemen kapatır.</BL>\n"
            message += "<J>/clearcache</J><BL> : Sunucunun IP'lerinin önbelleğini temizle.</BL>\n"
            message += "<J>/cleariptemban</J><BL> : Sunucuda geçici olarak yasaklanan IP'leri temizleme.</BL>\n"
            message += "<J>/clearreports</J><BL> : ModoPwet'daki tüm raporları sıfırla.</BL>\n"
            message += "<J>/changepassword</J> <V>[kullanıcı adı] [şifre]<BL> : Kullanıcının şifresini değiştir.</BL>\n"
            message += "<J>/playersql</J> <V>[kullanıcı adı] [parametre] [miktar]<BL> : Kullanıcının SQL bilgilerini değiştirir.</BL>\n"
            message += "<J>/smn</J> <V>[message]<BL> : Sunucunuza adınızla bir mesaj gönderin.</BL>\n"
            message += "<J>/mshtml</J> <v>[mesaj]<BL> : HTML'de bir mesaj gönder.</BL>\n"
            message += "<J>/admin</J> <V>[mesaj]<BL> : Admin olarak küresel mesaj.</BL>\n"
            message += "<J>/rank</J> <V>[kullanıcıAdı] [rank]<BL> : Kullanıcının yetkisini ayarla</BL>\n"
            message += "<J>/setvip</J> <V>[kullanıcı adı] [süre]<BL> : Bir kişiye süreli VIP ver.</BL>\n"
            message += "<J>/removevip</J> <V>[kullanıcı adı]<BL> : Bir kişinin VIP üyeliğini elinden al.</BL>\n"

        if this.client.privLevel >= 10:
            message += "<J>/updatesql</J><BL> : Çevrimiçi olarak veritabanını güncelle."
            message += "<J>/luaadmin</J><BL> : Sunucuda script çalıştırmayı Aktif/Pasif et.</BL>\n"

        if this.client.privLevel >= 10:
            message += "<J>/ban</J> <V>[kullanıcı adı] [saat] [argument]<BL> :Sunucudan banlamak. (diğer: /iban)</BL>\n"
            message += "<J>/mute</J> [kullanıcı adı] [saat] [argument]<BL> : Kullanıcıyı sustur.</BL>\n"
        
        message += "</font></p>"
        return message
