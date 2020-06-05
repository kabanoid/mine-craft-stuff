import json
import re
from .connection import Connection

class Minecraft:
    def __init__(self, connection):
        self.conn = connection

    def getPlayersUIDs(self):
        uuidsResp = self.conn.send("/list")
        uuids = re.search(r'(?<=online: ).+', uuidsResp)
        if (uuids):
            return uuids.group(0).split(', ')
        else:
            return []

    def postToChat(self, msg):
        self.conn.send(" ".join(["/say", msg]))

    def whisper(self, uuid, msg):
        self.conn.send(" ".join(["/w", uuid, msg]))

    def fillRange(self, start, end, block):
        self.conn.send(" ".join(["/fill",
            str(start[0]), str(start[1]), str(start[2]),
            str(end[0]), str(end[1]), str(end[2]),
            block]))

    def giveItem(self, uuid, item, amount = 1):
        self.conn.send(" ".join(["/give", uuid, item, str(amount)]))

    def getMobs(self, mob):
        # under construction
        mobs = self.conn.send("")
        return mobs

    def getPlayerData(self, uuid):
        playerDataResp = self.conn.send(" ".join(["/data", "get", "entity", uuid]))
        # convert playerDataResp to a hash
        playerDataStr = re.search(r'(?<=entity data: ).+', playerDataResp)
        if (playerDataStr):
            rawPlayerData = re.sub(r'(\w+):\s', r'"\1": ', playerDataStr.group(0))
            rawPlayerData = re.sub(r'(\d+)[a-zA-Z](\W)', r'\1\2', rawPlayerData)

            print rawPlayerData

            return json.loads(rawPlayerData)
        else:
            return {}

    def getPlayerPosition(self, uuid):
        positionResp = self.conn.send(" ".join(["/data", "get", "entity", uuid, "Pos"]))
        positionMatcher = re.search(r'(?<=entity data: ).+', positionResp)
        if (positionMatcher):
            positionData = re.sub(r'(\w+):\s', r'"\1": ', positionMatcher.group(0))
            positionData = re.sub(r'(\d+)[a-zA-Z](\W)', r'\1\2', positionData)
            return map(int, json.loads(positionData))
        else:
            return [0, 0, 0]

    def getPlayerRotation(self, uuid):
        rotationResp = self.conn.send(" ".join(["/data", "get", "entity", uuid, "Rotation"]))
        rotationMatcher = re.search(r'(?<=entity data: ).+', rotationResp)
        if (rotationMatcher):
            rotationData = re.sub(r'(\w+):\s', r'"\1": ', rotationMatcher.group(0))
            rotationData = re.sub(r'(\d+)[a-zA-Z](\W)', r'\1\2', rotationData)
            return map(int, json.loads(rotationData))
        else:
            return [0, 0]

    def modifyEntity(self):
        res = self.conn.send(" ".join([
            "/data",
            "merge",
            "entity",
            "@e[type=sheep,name=Jebb,limit=1]",
            "{Color:13}"
        ]))
        print res

    def paintEntityByName(self, name, color):
        res = self.conn.send(" ".join([
            "/data merge entity",
            "@e[type=sheep,name="+name+",limit=1]",
            "{Color:"+str(color)+"}"
        ]))

    def setTime(self, time):
        self.conn.send(" ".join(["/time", "set", str(time)]))

    def setBlock(self, position, block):
        res = self.conn.send(" ".join(["/setblock", str(position[0]), str(position[1]), str(position[2]), block]))
        print res

    def summonMob(self, mob = "sheep", position = [69, 65, -30], nbt = {}):
        res = self.conn.send(" ".join([
            "/summon",
            mob,
            str(position[0]), str(position[1]), str(position[2]),
            json.dumps(nbt)
        ]))
        print res

    @staticmethod
    def create(address = "localhost", secret = "mysecret"):
        return Minecraft(Connection(address, None, secret));
