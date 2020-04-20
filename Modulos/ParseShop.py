#coding: utf-8
import binascii

from ByteArray import ByteArray
from Identifiers import Identifiers

class ParseShop:
    def __init__(this, player, server):
        this.client = player
        this.server = player.server
        this.Cursor = player.Cursor

    def getShopLength(this):
        return 0 if this.client.shopItems == "" else len(this.client.shopItems.split(","))

    def checkUnlockShopTitle(this):
        if this.server.shopTitleList.has_key(this.getShopLength()):
            title = this.server.shopTitleList[this.getShopLength()]
            this.client.checkAndRebuildTitleList("shop")
            this.client.sendUnlockedTitle(int(title - (title % 1)), int(round((title % 1) * 10)))
            this.client.sendCompleteTitleList()
            this.client.sendTitleList()

    def checkAndRebuildBadges(this):
        rebuild = False
        for badge in this.server.shopBadges.items():
            if not badge[0] in this.client.shopBadges and this.checkInShop(badge[0]):
                this.client.shopBadges.append(str(badge[1]))
                rebuild = True

        if rebuild:
            badges = map(int, this.client.shopBadges)
            this.client.shopBadges = []
            for badge in badges:
                if not badge in this.client.shopBadges:
                    this.client.shopBadges.append(badge)

    def checkUnlockShopBadge(this, itemID):
        if not this.client.isGuest:
            if this.server.shopBadges.has_key(itemID):
                unlockedBadge = this.server.shopBadges[itemID]
                this.sendUnlockedBadge(unlockedBadge)
                this.checkAndRebuildBadges()

    def checkInShop(this, checkItem):
        if not this.client.shopItems == "":
            for shopItem in this.client.shopItems.split(","):
                if checkItem == int(shopItem.split("_")[0] if "_" in shopItem else shopItem):
                    return True
        else:
            return False

    def checkInShamanShop(this, checkItem):
        if not this.client.shamanItems == "":
            for shamanItems in this.client.shamanItems.split(","):
                if checkItem == int(shamanItems.split("_")[0] if "_" in shamanItems else shamanItems):
                    return True
        else:
            return False

    def checkInPlayerShop(this, type, playerName, checkItem):
        this.Cursor.execute("select %s from Users where Username = %s" %(type), [playerName])
        for rs in this.Cursor.fetchall():
            items = rs[type]
            if not items == "":
                for shopItem in items.split(","):
                    if checkItem == int(shopItem.split("_")[0] if "_" in shopItem else shopItem):
                        return True
            else:
                return False

    def getItemCustomization(this, checkItem, isShamanShop):
        items = this.client.shamanItems if isShamanShop else this.client.shopItems
        if not items == "":
            for shopItem in items.split(","):
                itemSplited = shopItem.split("_")
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                if int(itemSplited[0]) == checkItem:
                    return "" if custom == "" else ("_" + custom)
        else:
            return ""

    def getShamanItemCustom(this, code):
        item = this.client.shamanItems.split(",")
        if "_" in item:
            itemSplited = item.split("_")
            custom = (itemSplited[1] if len(itemSplited) >= 2 else "").split("+")
            if int(itemSplited[0]) == code:
                packet = ByteArray().writeByte(len(custom))
                x = 0
                while x < len(custom):
                    packet.writeInt(int(custom[x], 16))
                    x += 1
                return packet.toByteArray()
        return chr(0)

    def getShopItemPrice(this, fullItem):
        itemCat = (0 if fullItem / 10000 == 1 else fullItem / 10000) if fullItem > 9999 else fullItem / 100
        item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem
        return this.getItemPromotion(itemCat, item, this.server.shopListCheck[str(itemCat) + "|" + str(item)][1])
                
    def getShamanShopItemPrice(this, fullItem):
        return this.server.shamanShopListCheck[str(fullItem)][1]

    def getItemPromotion(this, itemCat, item, price):
        for promotion in this.server.shopPromotions:
            if promotion[0] == itemCat and promotion[1] == item:
                return int(promotion[2] / 100.0 * price)
        return price

    def sendShopList(this):
        this.sendShopList(True)

    def sendShopList(this, sendItems=True):
        shopItems = [] if this.client.shopItems == "" else this.client.shopItems.split(",")
        
        packet = ByteArray().writeInt(this.client.shopCheeses).writeInt(this.client.shopFraises).writeUTF(this.client.playerLook).writeInt(len(shopItems))
        for item in shopItems:
            if "_" in item:
                itemSplited = item.split("_")
                realItem = itemSplited[0]
                custom = itemSplited[1] if len(itemSplited) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")
                packet.writeByte(len(realCustom)+1).writeInt(int(realItem))
                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeByte(0).writeInt(int(item))

        shop = this.server.shopList if sendItems else []
        packet.writeInt(len(shop))
        for item in shop:
            value = item.split(",")
            packet.writeShort(value[0]).writeShort(value[1]).writeByte(value[2]).writeByte(value[3]).writeByte(value[4]).writeInt(value[5]).writeInt(value[6]).writeShort(0)

        visuais = this.server.newVisuList
        packet.writeByte(len(visuais))
        i = len(visuais)
        visu = []
        for visual in visuais.items():
            visu.append(visual[1])
            if visual[1] in visu:
                visu.remove(visual[1])
            packet.writeShort(visual[0])
            a = visual[1]
            packet.writeUTF(''.join(a))
            packet.writeByte(2 if visual[0] in [52] else 1 if visual[0] in [53] else 2)
            i -= 1
        
        packet.writeShort(len(this.client.clothes))
        
        for clothes in this.client.clothes:
            clotheSplited = clothes.split("/")
            packet.writeUTF(clotheSplited[1] + ";" + clotheSplited[2] + ";" + clotheSplited[3])

        shamanItems = [] if this.client.shamanItems == "" else this.client.shamanItems.split(",")
        packet.writeShort(len(shamanItems))
        for item in shamanItems:
            if "_" in item:
                itemSplited = item.split("_")
                realItem = itemSplited[0]
                custom = itemSplited[1] if (len(itemSplited) >= 2) else ""
                realCustom = [] if custom == "" else custom.split("+")
                packet.writeShort(int(realItem)).writeBoolean(item in this.client.shamanLook.split(",")).writeByte(len(realCustom) + 1)
                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeShort(int(item)).writeBoolean(item in this.client.shamanLook.split(",")).writeByte(0)

        shamanShop = this.server.shamanShopList if sendItems else []
        packet.writeShort(len(shamanShop))
        for item in shamanShop:
            value = item.split(",")
            packet.writeInt(value[0]).writeByte(value[1]).writeByte(value[2]).writeByte(value[3]).writeInt(value[4]).writeShort(value[5])
        this.client.sendPacket(Identifiers.send.Shop_List, packet.toByteArray())
             
    def sendShamanItems(this):
        shamanItems = [] if this.client.shamanItems == "" else this.client.shamanItems.split(",")

        packet = ByteArray().writeShort(len(shamanItems))
        for item in shamanItems:
            if "_" in item:
                custom = item.split("_")[1] if len(item.split("_")) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")
                packet.writeShort(int(item.split("_")[0])).writeBoolean(item in this.client.shamanLook.split(",")).writeByte(len(realCustom) + 1)
                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16))
                    x += 1
            else:
                packet.writeShort(int(item)).writeBoolean(item in this.client.shamanLook.split(",")).writeByte(0)
        this.client.sendPacket(Identifiers.send.Shaman_Items, packet.toByteArray())

    def sendLookChange(this):
        kostum, giysiler = this.client.playerLook.split(";")
        giysiler = giysiler.split(',')
        giysiler.append('0')
        packet = ByteArray().writeByte(int(kostum))

        for item in giysiler:
            if "_" in item:
                custom = item.split("_")[1] if len(item.split("_")) >= 2 else ""
                realCustom = [] if custom == "" else custom.split("+")
                packet.writeInt(int(item.split("_")[0])).writeByte(len(realCustom))
                
                x = 0
                while x < len(realCustom):
                    packet.writeInt(int(realCustom[x], 16) if realCustom[x].isdigit() else int("FADE55", 16))
                    x += 1
            else:
                packet.writeInt(int(item)).writeByte(0)

        try:
            packet.writeInt(int(this.client.mouseColor, 16))
        except:
            packet.writeInt(int("78583A", 16))
        this.client.sendPacket(Identifiers.send.Look_Change, packet.toByteArray())
    def sendShamanLook(this):
        items = ByteArray()

        count = 0        
        for item in this.client.shamanLook.split(","):
            realItem = int(item.split("_")[0]) if "_" in item else int(item)
            if realItem != 0:
                items.writeShort(realItem)
                count += 1
        this.client.sendPacket(Identifiers.send.Shaman_Look, ByteArray().writeShort(count).writeBytes(items.toByteArray()).toByteArray())

    def sendItemBuy(this, fullItem):
        this.client.sendPacket(Identifiers.send.Item_Buy, ByteArray().writeShort(fullItem).writeByte(1).toByteArray())

    def sendUnlockedBadge(this, badge):
        this.client.room.sendAll(Identifiers.send.Unlocked_Badge, ByteArray().writeInt(this.client.playerCode).writeShort(badge).toByteArray())

    def sendGiftResult(this, type, playerName):
        this.client.sendPacket(Identifiers.send.Gift_Result, ByteArray().writeByte(type).writeUTF(playerName).writeByte(0).writeShort(0).toByteArray())

    def equipClothe(this, packet):
        clotheID = packet.readByte()
        for clothe in this.client.clothes:
            values = clothe.split("/")
            if values[0] == "%02d" %(clotheID):
                this.client.playerLook = values[1]
                this.client.mouseColor = values[2]
                this.client.shamanColor = values[3]
                break
        save = this.client.playerLook.split(";")
        this.client.checkElection(int(save[0]))
        this.sendLookChange()
        this.sendShopList(False)

    def saveClothe(this, packet):
        clotheID = packet.readByte()
        for clothe in this.client.clothes:
            values = clothe.split("/")
            if values[0] == "%02d" %(clotheID):
                values[1] = this.client.playerLook
                values[2] = this.client.mouseColor
                values[3] = this.client.shamanColor
                this.client.clothes[this.client.clothes.index(clothe)] = "/".join(values)
                break

        this.sendShopList(False)

    def sendShopInfo(this):            
        this.client.sendPacket(Identifiers.send.Shop_Info, ByteArray().writeInt(this.client.shopCheeses).writeInt(this.client.shopFraises).toByteArray())

    def equipItem(this, packet):
        fullItem = packet.readInt()
        itemCat = (0 if fullItem / 10000 == 1 else fullItem / 10000) if fullItem > 9999 else fullItem / 100
        item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem
        lookList = this.client.playerLook.split(";")
        lookItems = lookList[1].split(",")
        lookCheckList = lookItems[:]
        i = 0
        while i < len(lookCheckList):
            lookCheckList[i] = lookCheckList[i].split("_")[0] if "_" in lookCheckList[i] else lookCheckList[i]
            i += 1

        if itemCat <= 10:
            lookItems[itemCat] = "0" if lookCheckList[itemCat] == str(item) else str(item) + this.getItemCustomization(fullItem, False)
        elif itemCat == 21:
            lookList[0] = "1"
            color = "bd9067" if item == 0 else "593618" if item == 1 else "8c887f" if item == 2 else "dfd8ce" if item == 3 else "4e443a" if item == 4 else "e3c07e" if item == 5 else "272220" if item == 6 else "78583a"
            this.client.mouseColor = "78583a" if this.client.mouseColor == color else color
        else:
            lookList[0] = "1" if lookList[0] == str(item) else str(item)
            this.client.mouseColor = "78583a"
            this.client.checkElection(int(lookList[0]))

        this.client.playerLook = lookList[0] + ";" + ",".join(map(str, lookItems))
        this.sendLookChange()

    def buyItem(this, packet):
        fullItem, withFraises = packet.readShort(), packet.readBoolean()
        buyItem = fullItem
        fullItem = 230100+(32044+fullItem) if fullItem < 0 else fullItem
        itemCat = (0 if fullItem / 10000 == 1 else fullItem / 10100) if fullItem > 9999 else fullItem / 100
        item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem
        this.client.shopItems += str(fullItem) if this.client.shopItems == "" else "," + str(fullItem)
        price = this.getItemPromotion(itemCat, item, this.server.shopListCheck[str(itemCat) + "|" + str(item)][1 if withFraises else 0])
        if withFraises:
            this.client.shopFraises -= price
        else:
            this.client.shopCheeses -= price

        this.sendItemBuy(buyItem)
        this.sendShopList(False)
        this.client.sendAnimZelda(0, fullItem)
        this.checkUnlockShopTitle()
        this.checkUnlockShopBadge(fullItem)

    def customItemBuy(this, packet):
        fullItem, withFraises = packet.readShort(), packet.readBoolean()

        items = this.client.shopItems.split(",")
        for shopItem in items:
            item = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(item):
                items[items.index(shopItem)] = shopItem + "_"
                break

        this.client.shopItems = ",".join(items)
        if withFraises:
            this.client.shopFraises -= 20
        else:
            this.client.shopCheeses -= 2000

        if len(this.client.custom) == 1:
            if not fullItem in this.client.custom:
                this.client.custom.append(fullItem)
        else:
            if not str(fullItem) in this.client.custom:
                this.client.custom.append(str(fullItem))
                
        this.sendShopList(False)

    def customItem(this, packet):
        fullItem, length = packet.readShort(), packet.readByte()
        custom = length
        customs = list()

        i = 0
        while i < length:
            customs.append(packet.readInt())
            i += 1

        items = this.client.shopItems.split(",")
        for shopItem in items:
            sItem = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(sItem):
                newCustoms = map(lambda color: "%06X" %(0xffffff & color), customs)

                items[items.index(shopItem)] = sItem + "_" + "+".join(newCustoms)
                this.client.shopItems = ",".join(items)

                itemCat = (0 if fullItem / 10000 == 1 else fullItem / 10000) if fullItem > 9999 else fullItem / 100
                item = fullItem % 1000 if fullItem > 9999 else fullItem % 100 if fullItem > 999 else fullItem % (100 * itemCat) if fullItem > 99 else fullItem
                equip = str(item) + this.getItemCustomization(fullItem, False)
                lookList = this.client.playerLook.split(";")
                lookItems = lookList[1].split(",")

                if "_" in lookItems[itemCat]:
                    if lookItems[itemCat].split("_")[0] == str(item):
                        lookItems[itemCat] = equip
                                
                elif lookItems[itemCat] == str(item):
                    lookItems[itemCat] = equip
                this.client.playerLook = lookList[0] + ";" + ",".join(lookItems)
                this.sendShopList(False)
                this.sendLookChange()
                break

    def buyShamanItem(this, packet):
        fullItem, withFraises = packet.readShort(), packet.readBoolean()
        price = this.server.shamanShopListCheck[str(fullItem)][1 if withFraises else 0]
        this.client.shamanItems += str(fullItem) if this.client.shamanItems == "" else "," + str(fullItem)

        if withFraises:
            this.client.shopFraises -= price
        else:
            this.client.shopCheeses -= price

        this.sendShopList(False)
        this.client.sendAnimZelda(1, fullItem)

    def equipShamanItem(this, packet):
        fullItem = packet.readInt()
        item = str(fullItem) + this.getItemCustomization(fullItem, True)
        itemStr = str(fullItem)
        itemCat = int(itemStr[:len(itemStr)-2])
        index = itemCat if itemCat <= 4 else itemCat - 1 if itemCat <= 7 else 7 if itemCat == 10 else 8 if itemCat == 17 else 9
        index -= 1
        lookItems = this.client.shamanLook.split(",")

        if "_" in lookItems[index]:
            if lookItems[index].split("_")[0] == itemStr:
                lookItems[index] = "0"
            else:
                lookItems[index] = item

        elif lookItems[index] == itemStr:
            lookItems[index] = "0"
        else:
            lookItems[index] = item

        this.client.shamanLook = ",".join(lookItems)
        this.sendShamanLook()

    def customShamanItemBuy(this, packet):
        fullItem, withFraises = packet.readShort(), packet.readBoolean()

        items = this.client.shamanItems.split(",")
        for shopItem in items:
            item = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(item):
                items[items.index(shopItem)] = shopItem + "_"
                break

        this.client.shamanItems = ",".join(items)
        if withFraises:
            this.client.shopFraises -= 150
        else:
            this.client.shopCheeses -= 4000
                
        this.sendShopList(False)

    def customShamanItem(this, packet):
        fullItem, length = packet.readShort(), packet.readByte()
        customs = []
        i = 0
        while i < length:
            customs.append(packet.readInt())
            i += 1

        items = this.client.shamanItems.split(",")
        for shopItem in items:
            sItem = shopItem.split("_")[0] if "_" in shopItem else shopItem
            if fullItem == int(sItem):
                newCustoms = map(lambda color: "%06X" %(0xFFFFFF & color), customs)

                items[items.index(shopItem)] = sItem + "_" + "+".join(newCustoms)
                this.client.shamanItems = ",".join(items)

                item = str(fullItem) + this.getItemCustomization(fullItem, True)
                itemStr = str(fullItem)
                itemCat = int(itemStr[len(itemStr)-2:])
                index = itemCat if itemCat <= 4 else itemCat - 1 if itemCat <= 7 else 7 if itemCat == 10 else 8 if itemCat == 17 else 9
                index -= 1
                lookItems = this.client.shamanLook.split(",")

                if "_" in lookItems[index]:
                    if lookItems[index].split("_")[0] == itemStr:
                        lookItems[index] = item
                                
                elif lookItems[index] == itemStr:
                    lookItems[index] = item

                this.client.shamanLook = ",".join(lookItems)
                this.sendShopList()
                this.sendShamanLook()
                break

    def buyClothe(this, packet):
        clotheID, withFraises = packet.readByte(), packet.readBoolean()
        this.client.clothes.append("%02d/1;0,0,0,0,0,0,0,0,0,0/78583a/%s" %(clotheID, "fade55" if this.client.shamanSaves >= 1000 else "95d9d6"))
        if withFraises:
            this.client.shopFraises -= 5 if clotheID == 0 else 50 if clotheID == 1 else 100
        else:
            this.client.shopCheeses -= 40 if clotheID == 0 else 1000 if clotheID == 1 else 2000 if clotheID == 2 else 4000

        this.sendShopList(False)

    def sendGift(this, packet):
        playerName, isShamanItem, fullItem, message = packet.readUTF(), packet.readBoolean(), packet.readShort(), packet.readUTF()
        if not this.server.checkExistingUser(playerName):
            this.sendGiftResult(1, playerName)
        else:
            player = this.server.players.get(playerName)
            if player != None:
                if (player.parseShop.checkInShamanShop(fullItem) if isShamanItem else player.parseShop.checkInShop(fullItem)):
                    this.sendGiftResult(2, playerName)
                else:
                    this.server.lastGiftID += 1
                    player.sendPacket(Identifiers.send.Shop_Gift, ByteArray().writeInt(this.server.lastGiftID).writeUTF(this.client.playerName).writeUTF(this.client.playerLook).writeBoolean(isShamanItem).writeShort(fullItem).writeUTF(message).writeBoolean(False).toByteArray())
                    this.sendGiftResult(0, playerName)
                    this.server.shopGifts[this.server.lastGiftID] = [this.client.playerName, isShamanItem, fullItem]
                    this.client.shopFraises -= this.getShamanShopItemPrice(fullItem) if isShamanItem else this.getShopItemPrice(fullItem)
                    this.sendShopList()
            else:
                gifts = ""
                if (this.checkInPlayerShop("ShamanItems" if isShamanItem else "ShopItems", playerName, fullItem)):
                    this.sendGiftResult(2, playerName)
                else:
                    this.Cursor.execute("select Gifts from Users where Username = %s", [playerName])
                    rs = this.Cursor.fetchone()
                    gifts = rs["Gifts"]

                gifts += ("" if gifts == "" else "/") + binascii.hexlify("|".join(map(str, [this.client.playerName, this.client.playerLook, isShamanItem, fullItem, message])))
                this.Cursor.execute("update Users set Gifts = %s where Username = %s", [gifts, playerName])
                this.sendGiftResult(0, playerName)

    def giftResult(this, packet):
        giftID, isOpen, message, isMessage = packet.readInt(), packet.readBoolean(), packet.readUTF(), packet.readBoolean()
        if isOpen:
            values = this.server.shopGifts[int(giftID)]
            player = this.server.players.get(str(values[0]))
            if player != None:
                player.sendLangueMessage("", "$DonItemRecu", this.client.playerName)

            isShamanItem = bool(values[1])
            fullItem = int(values[2])
            if isShamanItem:
                this.client.shamanItems += str(fullItem) if this.client.shamanItems == "" else ",%s" %(fullItem)
                this.sendShopList(False)
                this.client.sendAnimZelda(1, fullItem)
            else:
                this.client.shopItems += str(fullItem) if this.client.shopItems == "" else ",%s" %(fullItem)
                this.client.sendAnimZelda(0, fullItem)
                this.checkUnlockShopTitle()
                this.checkUnlockShopBadge(fullItem)

        elif not message == "":
            values = this.server.shopGifts[int(giftID)]
            player = this.server.players.get(str(values[0]))
            if player != None:
                player.sendPacket(Identifiers.send.Shop_Gift, ByteArray().writeInt(giftID).writeUTF(this.client.playerName).writeUTF(this.client.playerLook).writeBoolean(bool(values[1])).writeShort(int(values[2])).writeUTF(message).writeBoolean(True).toByteArray())
            else:
                messages = ""
                this.Cursor.execute("select Messages from Users where Username = %s", [str(values[0])])
                rs = this.Cursor.fetchone()
                messages = rs["Messages"]

                messages += ("" if messages == "" else "/") + binascii.hexlify("|".join(map(str, [this.client.playerName, this.client.playerLook, values[1], values[2], message])))
                this.Cursor.execute("update Users set Messages = %s where Username = %s", [messages, str(values[0])])

    def checkGiftsAndMessages(this, lastReceivedGifts, lastReceivedMessages):
        needUpdate = False
        gifts = lastReceivedGifts.split("/")
        for gift in gifts:
            if not gift == "":
                values = binascii.unhexlify(gift).split("|", 4)
                this.server.lastGiftID += 1
                this.client.sendPacket(Identifiers.send.Shop_Gift, ByteArray().writeInt(this.server.lastGiftID).writeUTF(values[0]).writeUTF(values[1]).writeBoolean(bool(values[2])).writeShort(int(values[3])).writeUTF(values[4] if len(values) > 4 else "").writeBoolean(False).toByteArray())
                this.server.shopGifts[this.server.lastGiftID] = [values[0], bool(values[2]), int(values[3])]
                needUpdate = True

        messages = lastReceivedMessages.split("/")
        for message in messages:
            if not message == "":
                values = binascii.unhexlify(message).split("|", 4)
                this.client.sendPacket(Identifiers.send.Shop_GIft, ByteArray().writeShort(0).writeShort(0).writeUTF(values[0]).writeBoolean(bool(values[1])).writeShort(int(values[2])).writeUTF(values[4]).writeUTF(values[3]).writeBoolean(True).toByteArray())
                needUpdate = True

        if needUpdate:
            this.Cursor.execute("update Users set Gifts = '', Messages = '' where Username = %s", [this.client.playerName])
