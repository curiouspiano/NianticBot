import discord
from discord.ext import commands
from datetime import datetime
from lib.common import make_selection
import asyncio

from lib.ocr import getTeam
from lib.ocr import getLevel
from lib.ocr import getName

import urllib

class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel = 488153124633182219
        self.DISALLOWED_CHANNELS = [519302286389018674, 488170130161926174, 488153124633182219]

    @commands.Cog.listener()
    async def on_message(self, message):
        #verify the bot isn't responding to itself...
        if(message.author.id != self.bot.user.id):
            #channel_verification on main server
            if(message.channel.id == self.channel):
                print("Valid attempt, {} attachments".format(len(message.attachments)))
                if(len(message.attachments) > 0):
                    for i in message.attachments:
                        await i.save("temp.png")

                    fails = []

                    #Get mod @mention
                    mod = message.guild.get_role(488160235085889537)
                    admin = message.guild.get_role(488147164757753859)
                    try:
                        res = getTeam("temp.png")
                        #possible team roles.
                        POSSIBLE = [488146122091528194, 488146121886138369, 488146121613508608, 519304919631527956]

                        addTeam = True

                        for j in message.author.roles:
                            if j.id in POSSIBLE:
                                await message.channel.send("You've been assigned a team already.\nTalk to a mod about getting your role changed...")
                                addTeam = False

                        #If the user isn't already in a team, add them.
                        if addTeam:
                            newRole = None
                            if res == 'instinct':
                                newRole = 488146122091528194
                            elif res == 'valor':
                                newRole = 488146121886138369
                            elif res == 'mystic':
                                newRole = 488146121613508608
                            else:
                                await message.channel.send("I'm sorry... couldn't determine your team")

                            rol = message.guild.get_role(newRole)
                            await message.author.add_roles(rol)
                            await message.channel.send("Welcome {} to team {}!".format(message.author.mention, res))

                        #Attempt to determine users level & pokemonGo name
                        try:
                            userLevel = getLevel("temp.png")
                            if userLevel >= 30:
                                #add the user to level 30+
                                await message.author.add_roles(message.guild.get_role(489511929392660480))
                                await message.channel.send("Looks like you're invited to the thriving thirties!")
                            if userLevel >= 40:
                                #add the user to levle 40
                                await message.author.add_roles(message.guild.get_role(517399593735028736))
                                await message.channel.send("Welcome to the ELITE level 40 club!")
                            await message.delete()
                        except Exception as e:
                            print(e)
                            await message.channel.send("... but I could not determine your level...\n {} or {}, could you please double check?".format(mod.mention, admin.mention))
                    except Exception as e:
                        await message.channel.send("Sorry... I had some issues")
                        await message.channel.send("Could a {} please help me out?".format(mod.mention))

            elif(self.bot.user.mentioned_in(message) and message.author != self.bot.user and not message.mention_everyone):
                await message.channel.send('¯\_(ツ)_/¯')

            elif(message.channel.id in self.DISALLOWED_CHANNELS and message.author.bot):
                await message.delete()

                slap = await message.channel.send(content="Stop using bot commands in this channel, you're making me angry!!!")
                await asyncio.sleep(3)

                await slap.delete()

def setup(bot):
    bot.add_cog(Verification(bot))
