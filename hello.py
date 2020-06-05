import koba.minecraft as minecraft

mc = minecraft.Minecraft.create(secret = "RCONSECRET")

mc.setTime("day")
mc.postToChat("Ahoj")

users = mc.getPlayersUIDs()
print users

for uuid in users:
    mc.whisper(uuid, "Hello " + uuid + ", take an apple")
    mc.giveItem(uuid, "minecraft:golden_apple", 1)

    position = mc.getPlayerPosition(uuid)
    rotation = mc.getPlayerRotation(uuid)

    print position

    x = position[0]
    y = position[1]
    z = position[2]

    for i in range(100):
        mc.summonMob("bee", [x, y+1, z], {"Color": 1, "CustomName":"\"Maya" + str(i) + "\""})

    mc.summonMob("skeleton", [x+5, y+5, z+5],
    {"Team":uuid,"ArmorItems":[{},{},{},{"Count":1,"id":"skeleton_skull"}],"CustomName":"\"Bishop\"","ActiveEffects":[{"Id":12,"Amplifier":0,"Duration":999999}]})
