import discord
from discord.ext import commands
import json
from os.path import isfile


class Leader():
    def __init__(self, bot):
        self.bot= bot
        self.gymleader = json.loads(open("gymleaders.json").read()) if isfile("gymleaders.json") else {}
        self.elite = json.loads(open("elitefour.json").read()) if isfile("elitefour.json") else []

    @commands.group(pass_context=True)
    async def leader(self,ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.send_message(ctx.message.channel,"You need a subcommand for this to work! Please try again")

    @leader.command(pass_context=True)
    async def list(self,ctx,ltype : str):
        #leader list <ltype>
        if ltype.replace(" ","")[:3].lower() == "gym":

            url1 = "https://pokemongo.gamepress.gg/sites/pokemongo/files/2018-02/Badge_GymLeader_GOLD_01.png"
            for userid in self.gymleader.keys():
                user = ctx.message.server.get_member(userid)
                em = discord.Embed(name="Gym Leader", description="Gym Leader")
                em.set_thumbnail(url=url1)
                em.add_field(name="Discord Username",value=user.mention,inline=True)
                em.add_field(name="Badge Title",value=self.gymleader[userid]['badgeName'],inline=True)
                em.add_field(name="Challenge Description",value=self.gymleader[userid]['desc'],inline=True)
                await self.bot.send_message(ctx.message.channel,embed=em)
        elif ltype.replace(" ","")[:9].lower() == "elitefour":

            url1 = "http://static.tumblr.com/8ead6fd4ef321fc779d824ec3d39f5cd/9vi46my/6uso1uc3y/tumblr_static_515l7v2awykgk0sgcwow4wgog.png"
            for userid in self.elite:
                user = ctx.message.server.get_member(userid)
                em = discord.Embed(name="Elite Four",description="Elite Four")
                em.set_thumbnail(url=url1)
                em.add_field(name="Discord Username",value=user.mention,inline=True)
                await self.bot.send_message(ctx.message.channel,embed=em)
        else:
            await self.bot.sent_message(ctx.message.channel,"I'm not sure I got that. Please try again")

    @leader.command(pass_context=True)
    async def add(self,ctx,ltype : str,user : discord.Member,desc : str = None,badgeName : str = None):
        if ltype.replace(" ","")[:3].lower() == "gym":
            #Adds a gym leader
            self.gymleader[user.id] = {}
            self.gymleader[user.id]['desc'] = desc
            self.gymleader[user.id]['badgeName'] = badgeName
            await self.bot.send_message(ctx.message.channel,"Gym Leader added:\n{}\n{}\n{}".format(user.mention,self.gymleader[user.id]['desc'],self.gymleader[user.id]['badgeName']))
            open("gymleaders.json",'w').write(json.dumps(self.gymleader))
        elif ltype.replace(" ","")[:9].lower() == "elitefour":
            #Adds an Elite Four Member
            self.elite.append(user.id)
            await self.bot.send_message(ctx.message.channel,"Elite Four Added:\n{}".format(user.mention))
            open("elitefour.json",'w').write(json.dumps(self.elite))
        else:
            await self.bot.sent_message(ctx.message.channel,"I'm not sure I got that. Please try again")

    @leader.command(pass_context=True)
    async def remove(self,ctx,ltype : str,user : discord.Member):
        if ltype.replace(" ","")[:3].lower() == "gym":
            del self.gymleader[user.id]
            await self.bot.send_message(ctx.message.channel,"Gym Leader removed: {}".format(user.mention))
        elif ltype.replace(" ","")[:9].lower() == "elitefour":
            del self.elite[user.id]
            await self.bot.send_message(ctx.message.channel,"Elite Four Member removed: {}".format(user.mention))
        else:
            await self.bot.send_message(ctx.message.channel,"I'm not sure I got that. Please try again")

def setup(bot):
    bot.add_cog(Leader(bot))
