from struct import *class ByteArray:    def __init__(stormice, bytes=""):        stormice.bytes = bytes    def writeByte(stormice, value):        if type(value) == unicode:            value = value.encode("utf-8")        pass        stormice.bytes += pack('!b', int(value))        return stormice    def writeUnsignedByte(stormice, value):        if type(value) == unicode:            value = value.encode("utf-8")        pass        stormice.bytes += pack('!B', int(value))        return stormice    def writeShort(stormice, value):        if type(value) == unicode:            value = value.encode("utf-8")        pass        stormice.bytes += pack('!h', int(value))        return stormice    def writeUnsignedShort(stormice, value):        if type(value) == unicode:            value = value.encode("utf-8")        pass        stormice.bytes += pack('!H', int(value))        return stormice        def writeInt(stormice, value):        if type(value) == unicode:            value = value.encode("utf-8")        pass        stormice.bytes += pack('!i', int(value))        return stormice    def writeUnsignedInt(stormice, value):        if type(value) == unicode:            value = value.encode("utf-8")        pass        stormice.bytes += pack('!I', int(value))        return stormice    def writeBoolean(stormice, value):        if type(value) == unicode:            value = value.encode("utf-8")        pass        stormice.bytes += pack('!?', int(value))        return stormice    def writeUTF(stormice, value):        if type(value) == unicode:            value = value.encode("utf-8")        pass        value = str(value)        size = len(value)        stormice.writeShort(size)        stormice.write(value)        return stormice    def writeUTFBytes(stormice, value, size):        if type(value) == unicode:            value = value.encode("utf-8")        pass        for data in str(pack('!b', 0)) * int(size):            if len(value) < int(size):                value = value + pack('!b', 0)        stormice.write(value)        return stormice    def writeBytes(stormice, value):        stormice.bytes += value        return stormice    def write(stormice, value):        stormice.bytes += value    def readByte(stormice):        value = unpack('!b', stormice.bytes[:1])[0]        stormice.bytes = stormice.bytes[1:]        return value    def readUnsignedByte(stormice):        value = unpack('!B', stormice.bytes[:1])[0]        stormice.bytes = stormice.bytes[1:]        return value    def readShort(stormice):        value = unpack('!h', stormice.bytes[:2])[0]        stormice.bytes = stormice.bytes[2:]        return value    def readUnsignedShort(stormice):        value = unpack('!H', stormice.bytes[:2])[0]        stormice.bytes = stormice.bytes[2:]        return value    def readInt(stormice):        value = unpack('!i', stormice.bytes[:4])[0]        stormice.bytes = stormice.bytes[4:]        return value		    def readUnsignedInt(stormice):        value = unpack('!I', stormice.bytes[:4])[0]        stormice.bytes = stormice.bytes[4:]        return value    def readUTF(stormice):        size = unpack('!h', stormice.bytes[:2])[0]        value = stormice.bytes[2:2 + size]        stormice.bytes = stormice.bytes[size + 2:]        return value    def readBoolean(stormice):        value = unpack('!?', stormice.bytes[:1])[0]        stormice.bytes = stormice.bytes[1:]        return (True if value == 1 else False)    def readUTFBytes(stormice, size):        value = stormice.bytes[:int(size)]        stormice.bytes = stormice.bytes[int(size):]        return value    def getLength(stormice):        return len(stormice.bytes)    def bytesAvailable(stormice):        return len(stormice.bytes) > 0    def toByteArray(stormice):        return stormice.bytes