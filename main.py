import time
import random
import logging
import discord
import asyncio
import nest_asyncio
nest_asyncio.apply()
import requests
import locale
import re

logging.basicConfig(level=logging.INFO)

locale.setlocale(locale.LC_ALL, '')

TOKEN = <TOKEN>

API_KEYS = <API_KEYS>

client = discord.Client()

global stop_spam
stop_spam = {}

ez_messages = [
    "Wait... This isn't what I typed!", "Anyone else really like Rick Astley?",
    "Hey helper, how play game?",
    "Sometimes I sing soppy, love songs in the car.",
    "I like long walks on the beach and playing Hypixel",
    "Please go easy on me, this is my first game!",
    "You're a great person! Do you want to play some Hypixel games with me?",
    "In my free time I like to watch cat videos on Youtube",
    "When I saw the witch with the potion, I knew there was trouble brewing.",
    "If the Minecraft world is infinite, how is the sun spinning around it?",
    "Hello everyone! I am an innocent player who loves everything Hypixel.",
    "Plz give me doggo memes!",
    "I heard you like Minecraft, so I built a computer in Minecraft in your Minecraft so you can Minecraft while you Minecraft",
    "Why can't the Ender Dragon read a book? Because he always starts at the End.",
    "Maybe we can have a rematch?",
    "I sometimes try to say bad things then this happens :(",
    "Behold, the great and powerful, my magnificent and almighty nemisis!",
    "Doin a bamboozle fren.", "Your clicks per second are godly. :scream:",
    "What happens if I add chocolate milk to macaroni and cheese?",
    "Can you paint with all the colors of the wind",
    "Blue is greener than purple for sure",
    "I had something to say, then I forgot it.",
    "When nothing is right, go left.", "I need help, teach me how to play!",
    "Your personality shines brighter than the sun.",
    "You are very good at the game friend.", "I like pineapple on my pizza",
    "I like pasta, do you prefer nachos?",
    "I like Minecraft pvp but you are truly better than me!",
    "I have really enjoyed playing with you! <3", "ILY <3",
    "Pineapple doesn't go on pizza!",
    "Lets be friends instead of fighting okay?"
]


async def spam(sentence, message, times):
    for i in range(0, times):
        if stop_spam[message.channel.id]:
            break
        await message.channel.send(sentence)
        time.sleep(1)


def prefix(player):
    if "prefix" in player:
        return re.sub("§.", "", player["prefix"]) + " "
    elif "rank" in player:
        if player["rank"] == "YOUTUBER":
            return "[YOUTUBE] "
        else:
            return "[ADMIN] "
    elif "monthlyPackageRank" in player and player[
            "monthlyPackageRank"] is not None and player[
                "monthlyPackageRank"] != "NONE":
        # print(player["monthlyPackageRank"])
        if player["monthlyPackageRank"] == "SUPERSTAR":
            return "[MVP++] "
    elif "newPackageRank" in player:
        return "[" + player["newPackageRank"].replace("_PLUS", "+") + "] "
    else:
        return ""


def start(channel):
    global stop_spam
    stop_spam[channel] = False


def mock(sentence, type):
    if type == 0:
        mocked = []
        i = 0

        for char in sentence:
            if char.isalpha():
                if i % 2 == 0:
                    mocked.append(char.lower())
                else:
                    mocked.append(char.upper())
            else:
                mocked.append(char)
                i = i + 1

            i = i + 1

        return "".join(mocked)
    elif type == 1:
        mocked = []

        for char in sentence:
            if char.isalpha():
                if random.random() > 0.5:
                    mocked.append(char.lower())
                else:
                    mocked.append(char.upper())
            else:
                mocked.append(char)

        return "".join(mocked)


@client.event
async def on_message(message):
    global stop_spam

    if message.author == client.user:
        return

    if message.content.startswith('-help'):
        await message.channel.send("""`-mock <text>` or `-m <text>`
rEtUrN tHe TeXt LiKe ThIs
`-rmock <text>` or `-rm <text>`
reTuRN The tEXt lIkE tHIS (RAnDom cAPitaLIZatIoN)     
`-spam <text> <# of times>`
spam the text n times  
`-stopall`
stop all ongoing spamming       
`-dab`
<o/        
`-bw <player name>`
return a player's Bedwars stats        
`-bwfkdr <player name>`
return a player's Bedwars Final-Kill-to-Death-Ratio
`-bwkdr <player name>`
return a player's Bedwars Kill-to-Death-Ratio
`-bwwl <player name>`
return a player's Bedwars Win-to-Loss-Ratio
`-sw <player name>`
return a player's Skywars stats
`-swkdr <player name>`
return a player's Skywars Kill-to-Death-Ratio
`-swwl <player name>`
return a player's Skywars Win-to-Loss-Ratio
`-sb <player name> <profile (optional)>`
return a player's Skyblock stats
`ez`
you're not allowed to say ez!""")

    if message.content.startswith('-mock '):
        sentence = message.content[6:len(message.content)]

        await message.channel.send(mock(sentence, 0).format(message))
    elif message.content.startswith('-m '):
        sentence = message.content[3:len(message.content)]

        await message.channel.send(mock(sentence, 0).format(message))
    elif message.content.startswith('-rmock '):
        sentence = message.content[7:len(message.content)]

        await message.channel.send(mock(sentence, 1).format(message))
    elif message.content.startswith('-rm '):
        sentence = message.content[4:len(message.content)]

        await message.channel.send(mock(sentence, 1).format(message))
    elif message.content.startswith('-spam '):
        args = message.content.split(' ')

        if '@' not in message.content:
            if len(args) > 2 and args[len(args) - 1].isnumeric():
                if int(args[len(args) - 1]) <= 100:

                    def stop():
                        task.cancel()

                    sentence = message.content[6:len(message.content) -
                                            len(args[len(args) - 1]) - 1]

                    # loop = asyncio.get_event_loop()

                    # loop.call_later(int(args[len(args) - 1]), stop)

                    # task = loop.create_task(spam(sentence, message, int(args[len(args) - 1])))

                    stop_spam[message.channel.id] = False

                    await spam(sentence, message, int(args[len(args) - 1]))

                    # try:
                    #   loop.run_until_complete(task)
                    # except asyncio.CancelledError:
                    #   pass

                else:
                    await message.channel.send("You can only spam up to 100 times")
            else:
                await message.channel.send(
                    "You need to write how many times you want to spam")
        else:
            await message.channel.send("You cannot spam a mention")
    elif message.content == '-stopall':
        stop_spam[message.channel.id] = True
        loop = asyncio.get_event_loop()
        loop.call_later(2, start, message.channel.id)
    elif message.content == ('-dab'):
        await message.channel.send("<o/")
    elif message.content.startswith('-bw '):
        player = requests.get(
            "https://api.hypixel.net/player?key=" + random.choice(API_KEYS) + "&name="
            + message.content.split(' ')[1]).json()
        if not player['success']:
            await message.channel.send(player['cause'])
        else:
            player = player['player']
            if player is not None:
                await message.channel.send("**" + prefix(player) +
                                        message.content.split(' ')[1] +
                                        "\'s Bedwars Stats**")
                if "Bedwars" in player["stats"]:
                    try:
                        await message.channel.send(
                            "Final-Kill-to-Death-Ratio: " +
                            str(player["stats"]["Bedwars"]["final_kills_bedwars"])
                            + "/" + str(player["stats"]["Bedwars"]
                                        ["final_deaths_bedwars"]) + " = **" +
                            str(player["stats"]["Bedwars"]["final_kills_bedwars"] /
                                player["stats"]["Bedwars"]["final_deaths_bedwars"])
                            + "**")
                        await message.channel.send(
                            "Kill-to-Death-Ratio: " +
                            str(player["stats"]["Bedwars"]["kills_bedwars"]) +
                            "/" +
                            str(player["stats"]["Bedwars"]["deaths_bedwars"]) +
                            " = **" +
                            str(player["stats"]["Bedwars"]["kills_bedwars"] /
                                player["stats"]["Bedwars"]["deaths_bedwars"]) +
                            "**")
                        await message.channel.send(
                            "Win-to-Loss-Ratio: " +
                            str(player["stats"]["Bedwars"]["wins_bedwars"]) + "/" +
                            str(player["stats"]["Bedwars"]["losses_bedwars"]) +
                            " = **" +
                            str(player["stats"]["Bedwars"]["wins_bedwars"] /
                                player["stats"]["Bedwars"]["losses_bedwars"]) +
                            "**")
                    except KeyError:
                        await message.channel.send(
                            message.content.split(' ')[1] +
                            " hasn't played Bedwars")
                else:
                    await message.channel.send(
                        message.content.split(' ')[1] + " hasn't played Bedwars")
            else:
                await message.channel.send(
                    "Player doesn't exist or hasn't logged on to Hypixel")
    elif message.content.startswith('-bwfkdr '):
        player = requests.get(
            "https://api.hypixel.net/player?key=" + random.choice(API_KEYS) + "&name="
            + message.content.split(' ')[1]).json()
        if not player['success']:
            await message.channel.send(player['cause'])
        else:
            player = player['player']
            if player is not None:
                if "Bedwars" in player["stats"] and "final_kills_bedwars" in player[
                        "stats"]["Bedwars"]:
                    await message.channel.send(
                        prefix(player) + message.content.split(' ')[1] +
                        "\'s Bedwars Final-Kill-to-Death-Ratio: " +
                        str(player["stats"]["Bedwars"]["final_kills_bedwars"]) +
                        "/" +
                        str(player["stats"]["Bedwars"]["final_deaths_bedwars"]) +
                        " = **" +
                        str(player["stats"]["Bedwars"]["final_kills_bedwars"] /
                            player["stats"]["Bedwars"]["final_deaths_bedwars"]) +
                        "**")
                else:
                    await message.channel.send(
                        message.content.split(' ')[1] + " hasn't played Bedwars")
            else:
                await message.channel.send(
                    "Player doesn't exist or hasn't logged on to Hypixel")
    elif message.content.startswith('-bwkdr '):
        player = requests.get(
            "https://api.hypixel.net/player?key=" + random.choice(API_KEYS) + "&name="
            + message.content.split(' ')[1]).json()
        if not player['success']:
            await message.channel.send(player['cause'])
        else:
            player = player['player']
            if player is not None:
                if "Bedwars" in player["stats"] and "kills_bedwars" in player[
                        "stats"]["Bedwars"]:
                    await message.channel.send(
                        prefix(player) + message.content.split(' ')[1] +
                        "\'s Bedwars Kill-to-Death-Ratio: " +
                        str(player["stats"]["Bedwars"]["kills_bedwars"]) + "/" +
                        str(player["stats"]["Bedwars"]["deaths_bedwars"]) +
                        " = **" +
                        str(player["stats"]["Bedwars"]["kills_bedwars"] /
                            player["stats"]["Bedwars"]["deaths_bedwars"]) + "**")
                else:
                    await message.channel.send(
                        message.content.split(' ')[1] + " hasn't played Bedwars")
            else:
                await message.channel.send(
                    "Player doesn't exist or hasn't logged on to Hypixel")
    elif message.content.startswith('-bwwl '):
        player = requests.get(
            "https://api.hypixel.net/player?key=" + random.choice(API_KEYS) + "&name="
            + message.content.split(' ')[1]).json()
        if not player['success']:
            await message.channel.send(player['cause'])
        else:
            player = player['player']
            if player is not None:
                if "Bedwars" in player["stats"] and "losses_bedwars" in player[
                        "stats"]["Bedwars"]:
                    await message.channel.send(
                        prefix(player) + message.content.split(' ')[1] +
                        "\'s Bedwars Win-to-Loss-Ratio: " +
                        str(player["stats"]["Bedwars"]["wins_bedwars"]) + "/" +
                        str(player["stats"]["Bedwars"]["losses_bedwars"]) +
                        " = **" +
                        str(player["stats"]["Bedwars"]["wins_bedwars"] /
                            player["stats"]["Bedwars"]["losses_bedwars"]) + "**")
                else:
                    await message.channel.send(
                        message.content.split(' ')[1] + " hasn't played Bedwars")
            else:
                await message.channel.send(
                    "Player doesn't exist or hasn't logged on to Hypixel")
    elif message.content.startswith('-sw '):
        player = requests.get(
            "https://api.hypixel.net/player?key=" + random.choice(API_KEYS) + "&name="
            + message.content.split(' ')[1]).json()
        if not player['success']:
            await message.channel.send(player['cause'])
        else:
            player = player['player']
            if player is not None:
                await message.channel.send("**" + prefix(player) +
                                        message.content.split(' ')[1] +
                                        "\'s SkyWars Stats**")
                if "SkyWars" in player["stats"]:
                    try:
                        await message.channel.send(
                            "Kill-to-Death-Ratio: " +
                            str(player["stats"]["SkyWars"]["kills"]) + "/" +
                            str(player["stats"]["SkyWars"]["deaths"]) + " = **" +
                            str(player["stats"]["SkyWars"]["kills"] /
                                player["stats"]["SkyWars"]["deaths"]) + "**")
                        await message.channel.send(
                            "Win-to-Loss-Ratio: " +
                            str(player["stats"]["SkyWars"]["wins"]) + "/" +
                            str(player["stats"]["SkyWars"]["losses"]) + " = **" +
                            str(player["stats"]["SkyWars"]["wins"] /
                                player["stats"]["SkyWars"]["losses"]) + "**")
                    except KeyError:
                        await message.channel.send(
                            message.content.split(' ')[1] +
                            " hasn't played SkyWars")
                else:
                    await message.channel.send(
                        message.content.split(' ')[1] + " hasn't played SkyWars")
            else:
                await message.channel.send(
                    "Player doesn't exist or hasn't logged on to Hypixel")
    elif message.content.startswith('-swkdr '):
        player = requests.get(
            "https://api.hypixel.net/player?key=" + random.choice(API_KEYS) + "&name="
            + message.content.split(' ')[1]).json()
        if not player['success']:
            await message.channel.send(player['cause'])
        else:
            player = player['player']
            if player is not None:
                if "SkyWars" in player["stats"]:
                    try:
                        await message.channel.send(
                            prefix(player) + message.content.split(' ')[1] +
                            "\'s SkyWars Kill-to-Death-Ratio: " +
                            str(player["stats"]["SkyWars"]["kills"]) + "/" +
                            str(player["stats"]["SkyWars"]["deaths"]) + " = **" +
                            str(player["stats"]["SkyWars"]["kills"] /
                                player["stats"]["SkyWars"]["deaths"]) + "**")
                    except KeyError:
                        await message.channel.send(
                            message.content.split(' ')[1] +
                            " hasn't played SkyWars")
                else:
                    await message.channel.send(
                        message.content.split(' ')[1] + " hasn't played SkyWars")
            else:
                await message.channel.send(
                    "Player doesn't exist or hasn't logged on to Hypixel")
    elif message.content.startswith('-swwl '):
        player = requests.get(
            "https://api.hypixel.net/player?key=" + random.choice(API_KEYS) + "&name="
            + message.content.split(' ')[1]).json()
        if not player['success']:
            await message.channel.send(player['cause'])
        else:
            player = player['player']
            if player is not None:
                if "SkyWars" in player["stats"]:
                    try:
                        await message.channel.send(
                            prefix(player) + message.content.split(' ')[1] +
                            "\'s SkyWars Win-to-Loss-Ratio: " +
                            str(player["stats"]["SkyWars"]["wins"]) + "/" +
                            str(player["stats"]["SkyWars"]["losses"]) + " = **" +
                            str(player["stats"]["SkyWars"]["wins"] /
                                player["stats"]["SkyWars"]["losses"]) + "**")
                    except KeyError:
                        await message.channel.send(
                            message.content.split(' ')[1] +
                            " hasn't played SkyWars")
                else:
                    await message.channel.send(
                        message.content.split(' ')[1] + " hasn't played SkyWars")
            else:
                await message.channel.send(
                    "Player doesn't exist or hasn't logged on to Hypixel")
    elif message.content.startswith('-sb '):
        player = requests.get(
            "https://api.hypixel.net/player?key=" + random.choice(API_KEYS) + "&name="
            + message.content.split(' ')[1]).json()
        if not player['success']:
            await message.channel.send(player['cause'])
        else:
            player = player['player']
            if player is not None:
                if "SkyBlock" in player["stats"]:
                    profile_names = {}
                    for profile in player["stats"]["SkyBlock"]["profiles"]:
                        profile_names[player["stats"]["SkyBlock"]["profiles"][
                            profile]["cute_name"]] = player["stats"]["SkyBlock"][
                                "profiles"][profile]["profile_id"]
                    # print(profile_names)

                    async def sbstats(profile_id):
                        sbprofile = requests.get(
                            "https://api.hypixel.net/skyblock/profile?key=" + random.choice(API_KEYS) + "&profile="
                            + profile_id).json()["profile"]
                        sbplayer = sbprofile["members"][player["uuid"]]
                        await message.channel.send(
                            "**" + prefix(player) + message.content.split(' ')[1] +
                            "\'s Skyblock Stats on " + player["stats"]["SkyBlock"]
                            ["profiles"][profile_id]["cute_name"] + "**")
                        await message.channel.send(
                            "<" + " | ".join(list(profile_names.keys())) + ">")
                        try:
                            await message.channel.send("Money in purse: **" + str(
                                locale.currency(sbplayer["coin_purse"],
                                                symbol=False,
                                                grouping=True)) + "**")
                            await message.channel.send("Money in bank: **" + str(
                                locale.currency(sbprofile["banking"]["balance"],
                                                symbol=False,
                                                grouping=True)) + "**")
                        except KeyError:
                            await message.channel.send(
                                "This player has not enabled the banking API on this profile"
                            )
                        try:
                            sbstats = sbplayer["stats"]
                            await message.channel.send("Deaths: **" + str(
                                locale.currency(sbstats["deaths"],
                                                symbol=False,
                                                grouping=True)) + "**")
                            await message.channel.send("Kills: **" + str(
                                locale.currency(sbstats["kills"],
                                                symbol=False,
                                                grouping=True)) + "**")
                        except KeyError:
                            await message.channel.send(
                                "This player has not enabled the stats API on this profile"
                            )

                    if len(player["stats"]["SkyBlock"]["profiles"]) == 1 or len(
                            message.content.split(' ')) == 2:
                        # sbdata = requests.get("https://api.hypixel.net/skyblock/profile?key=KEY&profile=" + list(profile_names.values())[0]).json()["profile"]["members"][player["uuid"]]
                        await sbstats(list(profile_names.values())[0])
                    # elif len(message.content.split(' ')) == 2:
                    #     await sbstats(list(profile_names.values())[0])
                    #     await message.channel.send("Please specify a profile: -sb " + message.content.split(' ')[1] + " <" + " | ".join(list(profile_names.keys())) + ">")
                    elif not message.content.split(' ')[2].capitalize() in list(
                            profile_names.keys()):
                        await message.channel.send("Profile doesn't exist")
                    else:
                        profile_id = profile_names[message.content.split(' ')
                                                [2].capitalize()]
                        # sbdata = requests.get("https://api.hypixel.net/skyblock/profile?key=KEY&profile=" + profile_id).json()["profile"]["members"][player["uuid"]]
                        await sbstats(profile_id)
                else:
                    await message.channel.send(
                        message.content.split(' ')[1] + " hasn't played Skyblock")
            else:
                await message.channel.send(
                    "Player doesn't exist or hasn't logged on to Hypixel")

    if 'ez' in message.content.lower():
        await message.channel.send(random.choice(ez_messages))


@client.event
async def on_ready():
    print('\nLogged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game("-help"))


client.run(TOKEN)
