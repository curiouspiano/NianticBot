import discord
from discord.ext import commands
import calendar
import datetime

class Leader():
    def __init__(self, bot):
        self.bot= bot

    @commands.group(pass_context=True)
    async def leader(self,ctx):
        """Manage and List Frontier League Leaders"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_message(ctx.message.channel,"You need a subcommand for this to work! Please try again")

    @leader.command(pass_context=True)
    async def list(self,ctx,*,ltype : str = None):
        """List all leaders of given type. If no type given, lists all leaders"""
        #leader list [ltype]
        isError=False
        if ltype.replace(" ","")[:3].lower() == "gym" if ltype is not None else True:

            url1 = "https://pokemongo.gamepress.gg/sites/pokemongo/files/2018-02/Badge_GymLeader_GOLD_01.png"
            await self.bot.SQL.connect()
            userList = (await self.bot.SQL.fetch_all_list((await self.bot.SQL.query("SELECT user_fk FROM challengers WHERE active=1 and name=\"Gym Leader\" ORDER BY id ASC;")),"user_fk"))
            if len(userList) == 0:
                self.bot.SQL.disconnect()
                return
            badgeCursor = (await self.bot.SQL.query("SELECT badges.name as name FROM challengers INNER JOIN badges ON badges.id=challengers.badge_fk WHERE challengers.active=1 ORDER BY challengers.id ASC;"))
            badgeNameList = (await self.bot.SQL.fetch_all_list(badgeCursor,"name"))
            descCursor = (await self.bot.SQL.query("SELECT badges.description as description FROM challengers INNER JOIN badges ON badges.id=challengers.badge_fk WHERE challengers.active=1 ORDER BY challengers.id ASC;"))
            badgeDescList = (await self.bot.SQL.fetch_all_list(descCursor,"description"))
            self.bot.SQL.disconnect()
            for i in range(len(userList)):
                user = ctx.message.server.get_member(str(userList[i]))
                em = discord.Embed(name="Gym Leader", description="Gym Leader")
                em.set_thumbnail(url=url1)
                em.add_field(name="Discord Username",value=user.mention,inline=True)
                em.add_field(name="Badge Title",value=badgeNameList[i],inline=True)
                em.add_field(name="Challenge Description",value=str(badgeDescList[i]).replace("b","").replace("'",""),inline=True)
                await self.bot.send_message(ctx.message.channel,embed=em)
        else:
            isError=True
        if ltype.replace(" ","")[:9].lower() == "elitefour" if ltype is not None else True:

            url1 = "http://static.tumblr.com/8ead6fd4ef321fc779d824ec3d39f5cd/9vi46my/6uso1uc3y/tumblr_static_515l7v2awykgk0sgcwow4wgog.png"
            await self.bot.SQL.connect()
            userList = (await self.bot.SQL.fetch_all_list((await self.bot.SQL.query("SELECT user_fk FROM challengers WHERE active=1 AND name=\"Elite Four\" ORDER BY id ASC;")),"user_fk"))

            for userid in userList:
                user = ctx.message.server.get_member(str(userid))
                em = discord.Embed(name="Elite Four",description="Elite Four")
                em.set_thumbnail(url=url1)
                em.add_field(name="Discord Username",value=user.mention,inline=True)
                await self.bot.send_message(ctx.message.channel,embed=em)
        else:
            isError=True
        if isError:
            await self.bot.send_message(ctx.message.channel,"I'm not sure I got that. Please try again")

    @leader.command(pass_context=True)
    async def add(self,ctx,ltype : str,user : discord.Member,desc : str = None,badgeName : str = None,challengeMonth : str = calendar.month_name[(datetime.datetime.today().month+1 if datetime.datetime.today().month < 12 else 1)],challengeYear : int = datetime.datetime.today().year):
        """Adds a leader to the Frontier League. This command is for admins only"""
        challengeMonthNum = list(calendar.month_name).index(challengeMonth)
        await self.bot.SQL.connect()
        if ltype.replace(" ","")[:3].lower() == "gym":
            cursor = await self.bot.SQL.query("SELECT max(id) FROM badges")

            await self.bot.SQL.query("\
                    REPLACE INTO badges\
                    SET description=\"{}\",\
                        name=\"{}\",\
                        start_available=\"{}-{}-01\",\
                        end_available=\"{}-{}-{}\";".format(\
                        desc,badgeName,\
                        challengeYear,challengeMonthNum,\
                        challengeYear,challengeMonthNum,calendar.monthrange(challengeYear,challengeMonthNum)[1]))
            badgeid = (await self.bot.SQL.fetch_all_list((await self.bot.SQL.query("\
            SELECT id FROM badges\
            WHERE\
                name=\"{}\" and start_available=\"{}-{}-01\";".format(\
                badgeName,challengeYear,challengeMonthNum))),"id"))[0]
            await self.bot.SQL.query("\
                    REPLACE INTO challengers\
                    SET name=\"Gym Leader\",\
                        user_fk={},\
                        badge_fk={},\
                        active=1,\
                        description=\"{}, {}\";".format(\
                        user.id,badgeid,challengeMonth,challengeYear))

            gymRole = discord.utils.get(ctx.message.server.roles,name="Gym Leader")
            await self.bot.add_roles(user,gymRole)
            await self.bot.send_message(ctx.message.channel,"Gym Leader added:\nLeader: {}\nDescription: {}\nBadge Name: {}".format(user.mention,desc,badgeName))
        elif ltype.replace(" ","")[:9].lower() == "elitefour":
            ##Adds an Elite Four Member
            await self.bot.SQL.query("\
                    REPLACE INTO challengers\
                    SET user_fk={},\
                        name=\"Elite Four\",\
                        active=1,\
                        description=\"{}, {}\";".format(\
                        user.id,challengeMonth,challengeYear))

            eliteRole = discord.utils.get(ctx.message.server.roles,name="Elite Four")
            await self.bot.add_roles(user,eliteRole)
            await self.bot.send_message(ctx.message.channel,"Elite Four Added:\n{}".format(user.mention))
        else:
            await self.bot.sent_message(ctx.message.channel,"I'm not sure I got that. Please try again")

        self.bot.SQL.disconnect()

    @leader.command(pass_context=True)
    async def remove(self,ctx,ltype : str,user : discord.Member):
        """Sets a leader as inactive in the Frontier League"""
        if ltype.replace(" ","")[:3].lower() == "gym":
            await self.bot.SQL.connect()
            await self.bot.SQL.query("UPDATE challengers SET active=0 WHERE user_fk={} and name=\"Gym Leader\";".format(user.id))
            self.bot.SQL.disconnect()

            gymRole = discord.utils.get(ctx.message.server.roles,name="Gym Leader")
            await self.bot.remove_roles(user,gymRole)

            await self.bot.send_message(ctx.message.channel,"Gym Leader removed: {}".format(user.mention))
        elif ltype.replace(" ","")[:9].lower() == "elitefour":
            await self.bot.SQL.connect()
            await self.bot.SQL.query("UPDATE challengers SET active=0 WHERE user_fk={} and name=\"Elite Four\";".format(user.id))
            self.bot.SQL.disconnect()

            eliteRole = discord.utils.get(ctx.message.server.roles,name="Elite Four")
            await self.bot.remove_roles(user,eliteRole)

            await self.bot.send_message(ctx.message.channel,"Elite Four Member removed: {}".format(user.mention))
        else:
            await self.bot.send_message(ctx.message.channel,"I'm not sure I got that. Please try again")

def setup(bot):
    bot.add_cog(Leader(bot))
