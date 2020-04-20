# -*- coding: cp1252 -*-
#Este modulo ha sido creado por Hailor - v0.1
import json, time
class AntiCheat:
    def __init__(this, client, server):
        this.client = client
        this.server = client.server
    def update(this):
        ac = ("[A.C] ")
        print (ac + "Config is being reloaded")
        try:
            this.client.server.ac_config = open('./AntiCheat/Config/anticheat_config.txt', 'r').read()
            this.client.server.ac_c = json.loads(this.client.server.ac_config)
            this.client.server.learning = this.client.server.ac_c['learning']
            this.client.server.bantimes = this.client.server.ac_c['ban_times']
            this.client.server.s_list = open('./AntiCheat/Config/anticheat_allow', 'r').read()
            if this.client.server.s_list != "":
                this.client.server.s_list = this.client.server.s_list.split(',')
                this.client.server.s_list.remove("")
            else:
                this.client.server.s_list = []
            print (ac + "Config reloaded sucessfully")
        except Exception as error:
            print (ac + "Oops, your config is invalid!")
            print (error)
    def sendAC(this, message, Server=True):
        if Server:
            this.client.server.sendModMessage(5, '<font color="#AF8026">[A.C] <font color="#99cc00">'+message+"</font>")
        else:
            this.client.sendMessage('<font color="#AF8026">[A.C] <font color="#99cc00">'+message)
    def readPacket(this, packet, pd=None):
        ac = ("[A.C] ")
        if packet == " " or packet == "":
            this.list.remove(packet)
        if str(packet) not in this.server.s_list and str(packet) != "":
            if this.server.learning == "true":
                if this.client.privLevel >= 2:
                    this.sendAC('New token from ['+this.client.Username+'] - ['+str(packet)+']')
                    print (ac + "Acabo de aprender un nuevo packete ["+str(packet)+"] ["+this.client.Username+"]")
                    this.server.s_list.append(str(packet))
                    w = open('./AntiCheat/Config/anticheat_allow', 'a')
                    w.write(str(packet) + ",")
                    w.close()
            else:
                if this.client.privLevel < 8:
                    if not this.client.room.isTotemEditeur or not this.client.room.isEditeur or not this.client.room.isVillage or not this.client.room.is801Room or not this.client.room.isTutorial:
                        if packet == 55 or packet == 31:
                            this.client.dac += 1
                            history = open("./AntiCheat/Cuentas/"+this.client.Username.replace("*", "!")+".txt", 'a')
                            timex = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())
                            history.write("\nPaquete usado: "+repr(packet)+" - Data del paquete: "+repr(pd)+" - Tiempo: "+str(timex)+" - IP: "+str(this.client.ipAddress))
                            this.sendAC(this.client.Username+' ha sido tagueado en el historial. ['+str(3-this.client.dac)+'T] ['+str(packet)+'] ')
                        else:
                            this.client.dac = 3
                        if this.client.dac >= 0 and this.client.dac <= 2:
                            this.sendAC('Hello', False)
                            this.client.dac += 1
                        else:
                            bans_done = 0
                            bl = open('./AntiCheat/Config/anticheat_bans.txt', 'r').read()
                            lista = bl.split('=')
                            lista.remove("")
                            for listas in lista:
                                data = listas.split(" ")
                                try:
                                    data.remove("")
                                except:
                                    data = ["a", "e"]
                                name = data[1]
                                if name == this.client.Username:
                                    bans_done += 1
                            if bans_done == 0:
                                tb = int(this.server.bantimes)
                            elif bans_done == 1:
                                tb = int(this.server.bantimes)*2
                            elif bans_done == 2:
                                tb = int(this.server.bantimes)*3
                            elif bans_done >= 3:
                                tb = int(this.server.bantimes)*4
                            
                            print (ac + "I have banned "+this.client.Username+" for an invalid packet. ["+str(packet)+"]")
                            if int(packet) == 31:
                                info = "Fly hack"
                            elif int(packet) == 51 or int(packet) == 55:
                                info = "Speed"                    
                            else:
                                info =  "Unknown"
                            bans_done += 1
                            x = open('./AntiCheat/Config/anticheat_bans.txt', 'a')
                            x.write("= Username: "+this.client.Username+" | Time: "+str(tb)+" hora(s) | Banned for: "+str(packet)+" | Data: "+info+" | +Info: "+repr(pd)+"\n")
                            x.close()
                            this.sendAC(this.client.Username+' ha sido baneado. ['+info+'] ['+str(tb)+'H] ')
                            this.client.server.sendModMessage(5, "<V>[A.C]<J> He baneado a "+this.client.Username+" por hack durante "+str(tb)+" hour(s). ["+info+"]")
                            this.client.server.banPlayer(this.client.Username, int(tb), "Hack detectado\ [Ban #"+str(bans_done)+" - "+info+"]", "A.C", False)
                else:
                    if int(packet) == 31:
                        info = "Fly hack"
                    elif int(packet) == 51 or int(packet) == 55:
                        info = "Speed"
                    else:
                        info =  "Unknown"    
                    this.client.dac += 1
                    print ("[A.C] Packet used by Admin ["+repr(pd)+"]")
                    this.sendAC(this.client.Username+' detectado ['+info+'] ['+str(this.client.dac)+'H] ')
                    
                
    
