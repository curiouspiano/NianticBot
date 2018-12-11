import discord
from discord.ext import commands
import json
from os.path import isfile


class Gym():
    def __init__(self, bot):
        self.bot= bot
#        self.gymleaders = []
        self.gymleader = json.loads(open("gymleaders.json").read()) if isfile("gymleaders.json") else {}

    @commands.command(pass_context=True)
    async def listleaders(self,ctx):
        leaderids = self.gymleader.keys()
        names = [ctx.message.server.get_member(user).mention for user in leaderids]
        await self.bot.say(', '.join(names))

    @commands.command(pass_context=True)
    async def addleader(self,ctx,user : discord.Member,desc : str, badgeName : str):
        print(user.id)
        self.gymleader[user.id] = {}
        self.gymleader[user.id]['desc'] = desc
        self.gymleader[user.id]['badgeName'] = badgeName
        user2 = ctx.message.server.get_member(user.id)
        await self.bot.say("Gym Leader added:\n%s\n%s\n%s"%(user2.mention,self.gymleader[user.id]['desc'],self.gymleader[user.id]['badgeName']))
        open("gymleaders.json",'w').write(json.dumps(self.gymleader))


def setup(bot):
    bot.add_cog(Gym(bot))
