import discord
from discord.ext import commands
import json
from os.path import isfile


class Gym():
    def __init__(self, bot):
        self.bot= bot
        self.gymleader = json.loads(open("gymleaders.json").read()) if isfile("gymleaders.json") else {}
        self.elite = json.loads(open("elitefour.json").read()) if isfile("elitefour.json") else []


    @commands.group(pass_context=True)
    async def list(self,ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_message(ctx.message.channel,"~list <type>\nTypes:\nleaders\nelitefour")

    @list.command(pass_context=True)
    async def elitefour(self,ctx):
        url1 = "http://static.tumblr.com/8ead6fd4ef321fc779d824ec3d39f5cd/9vi46my/6uso1uc3y/tumblr_static_515l7v2awykgk0sgcwow4wgog.png"
        for userid in self.elite:
            user = ctx.message.server.get_member(userid)
            em = discord.Embed(name="Elite Four",description="Elite Four")
            em.set_thumbnail(url=url1)
            em.add_field(name="Discord Username",value=user.mention,inline=True)
            await self.bot.send_message(ctx.message.channel,embed=em)

    @list.command(pass_context=True)
    async def leaders(self,ctx):
        url1 = "https://pokemongo.gamepress.gg/sites/pokemongo/files/2018-02/Badge_GymLeader_GOLD_01.png"
        for userid in self.gymleader.keys():
            user = ctx.message.server.get_member(userid)
            em = discord.Embed(name="Gym Leader", description="Gym Leader")
            em.set_thumbnail(url=url1)
            em.add_field(name="Discord Username",value=user.mention,inline=True)
            em.add_field(name="Badge Title",value=self.gymleader[userid]['badgeName'],inline=True)
            em.add_field(name="Challenge Description",value=self.gymleader[userid]['desc'],inline=True)
            await self.bot.send_message(ctx.message.channel,embed=em)

    @commands.group(pass_context=True)
    async def add(self,ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say("~add <type>\nTypes include:\nleader\nelitefour")

    @add.command(pass_context=True)
    async def leader(self,ctx,user : discord.Member, desc : str, badgeName : str):
        """Adds a gym leader"""
        self.gymleader[user.id] = {}
        self.gymleader[user.id]['desc'] = desc
        self.gymleader[user.id]['badgeName'] = badgeName
        await self.bot.send_message(ctx.message.channel,"Gym Leader added:\n{}\n{}\n{}".format(user.mention,self.gymleader[user.id]['desc'],self.gymleader[user.id]['badgeName']))
        open("gymleaders.json",'w').write(json.dumps(self.gymleader))

    @add.command(pass_context=True)
    async def elite_four(self,ctx,user : discord.Member):
        """Adds an Elite Four Member"""
        self.elite.append(user.id)
        await self.bot.send_message(ctx.message.channel,"Elite Four Added:\n{}".format(user.mention))
        open("elitefour.json",'w').write(json.dumps(self.elite))

def setup(bot):
    bot.add_cog(Gym(bot))
