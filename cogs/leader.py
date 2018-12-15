import discord
from discord.ext import commands
import json
from os.path import isfile
import calendar
import datetime

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
    async def add(self,ctx,ltype : str,user : discord.Member,desc : str = None,badgeName : str = None,challengeMonth : str = calendar.month_name[(datetime.datetime.today().month+1 if datetime.datetime.today().month < 12 else 1)],challengeYear : int = datetime.datetime.today().year):
        challengeMonthNum = list(calendar.month_name).index(challengeMonth)
        await self.bot.SQL.connect()
        challengerid = (await self.bot.SQL.fetch_all_list((await self.bot.SQL.query("SELECT max(id) FROM challengers")),'max(id)'))[0] + 1
        if ltype.replace(" ","")[:3].lower() == "gym":
            cursor = await self.bot.SQL.query("SELECT max(id) FROM badges")
            badgeid = (await self.bot.SQL.fetch_all_list(cursor,'max(id)'))[0] + 1
            await self.bot.SQL.query("\
                    REPLACE INTO badges\
                    SET id={},\
                        description=\"{}\",\
                        name=\"{}\",\
                        start_available=\"{}-{}-01\",\
                        end_available=\"{}-{}-{}\";".format(\
                        badgeid,desc,badgeName,\
                        challengeYear,challengeMonthNum,\
                        challengeYear,challengeMonthNum,calendar.monthrange(challengeYear,challengeMonthNum)[1]))
            await self.bot.SQL.query("\
                    REPLACE INTO challengers\
                    SET id={},\
                        name=\"Gym Leader\",\
                        user_fk={},\
                        badge_fk={},\
                        active=1,\
                        description=\"{}, {}\";".format(challengerid,user.id,badgeid,challengeMonth,challengeYear))

            await self.bot.send_message(ctx.message.channel,"Gym Leader added:\n{}\n{}\n{}".format(user.mention,self.gymleader[user.id]['desc'],self.gymleader[user.id]['badgeName']))
        elif ltype.replace(" ","")[:9].lower() == "elitefour":
            ##Adds an Elite Four Member
            await self.bot.SQL.query("\
                    REPLACE INTO challengers\
                    SET id={},\
                        user_fk={},\
                        name=\"Elite Four\",\
                        active=1,\
                        description=\"{}, {}\";".format(challengerid,user.id,challengeMonth,challengeYear))


            await self.bot.send_message(ctx.message.channel,"Elite Four Added:\n{}".format(user.mention))
            #open("elitefour.json",'w').write(json.dumps(self.elite))
        else:
            await self.bot.sent_message(ctx.message.channel,"I'm not sure I got that. Please try again")

        self.bot.SQL.disconnect()

    @leader.command(pass_context=True)
    async def remove(self,ctx,ltype : str,user : discord.Member):
        if ltype.replace(" ","")[:3].lower() == "gym":
            #del self.gymleader[user.id]
            await self.bot.SQL.connect()
            await self.bot.SQL.query("UPDATE challengers SET active=0 WHERE user_fk={} and name=\"Gym Leader\";".format(user.id))
            self.bot.SQL.disconnect()

            await self.bot.send_message(ctx.message.channel,"Gym Leader removed: {}".format(user.mention))
        elif ltype.replace(" ","")[:9].lower() == "elitefour":
            #del self.elite[user.id]
            await self.bot.SQL.connect()
            await self.bot.SQL.query("UPDATE challengers SET active=0 WHERE user_fk={} and name=\"Elite Four\";".format(user.id))
            self.bot.SQL.disconnect()
            await self.bot.send_message(ctx.message.channel,"Elite Four Member removed: {}".format(user.mention))
        else:
            await self.bot.send_message(ctx.message.channel,"I'm not sure I got that. Please try again")

def setup(bot):
    bot.add_cog(Leader(bot))
