import discord
from discord.ext import commands
import json
from os.path import isfile


class Gym():
    def __init__(self, bot):
        self.bot= bot
        self.gymleader = json.loads(open("gymleaders.json").read()) if isfile("gymleaders.json") else {}


    @commands.group(pass_context=True)
    async def list(self,ctx):
        if ctx.invoked_subcommand is None:
            url1 = "https://pokemongo.gamepress.gg/sites/pokemongo/files/2018-02/Badge_GymLeader_GOLD_01.png"
            for userid in self.gymleader.keys():
                user = ctx.message.server.get_member(userid)
                em = discord.Embed(name="Gym Leader", description="Gym Leader")
                em.set_thumbnail(url=url1)
                em.add_field(name="Discord Username",value=user.mention,inline=True)
                em.add_field(name="Badge Title",value=self.gymleader[userid]['badgeName'],inline=True)
                em.add_field(name="Challenge Description",value=self.gymleader[userid]['desc'],inline=True)
                await self.bot.send_message(ctx.message.channel,embed=em)

    @list.command(pass_context=True)
    async def leaders(self,ctx):
        names = [ctx.message.server.get_member(user).mention for user in self.gymleader.keys()]
        await self.bot.say(["Gym Leaders: ",', '.join(names)])

    @commands.command(pass_context=True,usage='<@user> <description> <badgeName>')
    async def addleader(self,ctx,user : discord.Member,desc : str, badgeName : str):
        """Adds a gym leader"""
        self.gymleader[user.id] = {}
        self.gymleader[user.id]['desc'] = desc
        self.gymleader[user.id]['badgeName'] = badgeName
        user2 = ctx.message.server.get_member(user.id)
        await self.bot.say("Gym Leader added:\n%s\n%s\n%s"%(user2.mention,self.gymleader[user.id]['desc'],self.gymleader[user.id]['badgeName']))
        open("gymleaders.json",'w').write(json.dumps(self.gymleader))


def setup(bot):
    bot.add_cog(Gym(bot))
