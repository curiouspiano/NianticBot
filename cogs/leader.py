import discord
from discord.ext import commands
import calendar
import datetime

class Leader(commands.Cog):

    def __init__(self, bot):
        self.bot= bot

    async def create_queue(self):
        await self.bot.SQL.connect()
        gymList = (await self.bot.SQL.fetch_all_list((await self.bot.SQL.query("SELECT user_fk FROM challengers WHERE active=1 and name=\"Gym Leader\" ORDER BY id ASC;")),"user_fk"))
        eliteList =await (await self.bot.SQL.query("SELECT user_fk, users.friendCode FROM challengers INNER JOIN users ON users.id=challengers.user_fk WHERE active=1 AND name=\"Elite Four\" ORDER BY challengers.id ASC;")).fetchall()
        self.bot.SQL.disconnect()
        self.leaderQueue = {\
                "gym" : {},\
                "elite": {}}
        for gym in gymList:
            self.leaderQueue["gym"][gym] = []
        for elite in eliteList:
            self.leaderQueue["elite"][elite] = []
    
    @commands.group(pass_context=True)
    async def leader(self,ctx):
        """Manage and List Frontier League Leaders"""
        if ctx.invoked_subcommand is None:
            await ctx.send("You need a subcommand for this to work! Please try again")

    @leader.command(pass_context=True)
    async def list(self,ctx,*,ltype : str = None):
        """List all leaders of given type. If no type given, lists all leaders"""
        #leader list [ltype]
        isError=False
        if ltype.replace(" ","")[:3].lower() == "gym" if ltype is not None else True:
            url1 = "https://pokemongo.gamepress.gg/sites/pokemongo/files/2018-02/Badge_GymLeader_GOLD_01.png"
            await self.bot.SQL.connect()
            userList = (await self.bot.SQL.fetch_all_list((await self.bot.SQL.query("SELECT user_fk FROM challengers WHERE active=1 and name=\"Gym Leader\" ORDER BY id ASC;")),"user_fk"))
            if len(userList) != 0:
                badgeCursor = (await self.bot.SQL.query("\
                        SELECT challengers.user_fk, badges.name, badges.description, users.friendCode, badges.thumbnail_path\
                        FROM challengers\
                        INNER JOIN badges ON badges.id=challengers.badge_fk\
                        INNER JOIN users ON challengers.user_fk=users.id\
                        WHERE challengers.active=1 and challengers.name='Gym Leader'\
                        ORDER BY challengers.id ASC;"))
                result = await badgeCursor.fetchall()

                self.bot.SQL.disconnect()
                for row in result:
                    user = ctx.message.guild.get_member(str(row['user_fk']))
                    em = discord.Embed(name="Gym Leader", description="Gym Leader")
                    if row['thumbnail_path'] != None:
                        url1 = row['thumbnail_path']
                    em.set_thumbnail(url=url1)
                    if user != None:
                        em.add_field(name="Discord Username",value=user.mention,inline=True)
                    em.add_field(name="Friend Code",value=row['friendCode'],inline=True)
                    em.add_field(name="Badge Title",value=row['name'],inline=True)
                    em.add_field(name="Challenge Description",value=str(row['description']),inline=True)
                    await ctx.send(embed=em)
            else:
                self.bot.SQL.disconnect()
        else:
            isError=True
        if ltype.replace(" ","")[:9].lower() == "elitefour" if ltype is not None else True:

            url1 = "https://i.imgur.com/l48LJkw.png"
            await self.bot.SQL.connect()
            userList =await (await self.bot.SQL.query("SELECT user_fk, users.friendCode FROM challengers INNER JOIN users ON users.id=challengers.user_fk WHERE active=1 AND name=\"Elite Four\" ORDER BY challengers.id ASC;")).fetchall()
            self.bot.SQL.disconnect()
            for userDict in userList:
                user = ctx.message.guild.get_member(str(userDict["user_fk"]))
                em = discord.Embed(name="Elite Four",description="Elite Four")
                em.set_thumbnail(url=url1)
                em.add_field(name="Discord Username",value=user.mention,inline=True)
                em.add_field(name="Friend Code",value=userDict["friendCode"],inline=True)
                await ctx.send(embed=em)
        else:
            isError=True
        if isError:
            await ctx.send("I'm not sure I got that. Please try again")
 
    @leader.command(pass_context=True)
    @commands.has_any_role('Admin','Mod','admin')
    async def add(self,ctx,ltype : str,user : discord.Member,desc : str = None,badgeName : str = None,badgeImageUrl : str = None,challengeMonth : str = calendar.month_name[(datetime.datetime.today().month+1 if datetime.datetime.today().month < 12 else 1)],challengeYear : int = datetime.datetime.today().year):
        """Adds a leader to the Frontier League. This command is for admins only"""
        if ctx.message.guild.id != 488144913230462989:
            await ctx.send("ya can't trick me!")
            return
        challengeMonthNum = list(calendar.month_name).index(challengeMonth)
        await self.bot.SQL.connect()
        if ltype.replace(" ","")[:3].lower() == "gym":
            cursor = await self.bot.SQL.query("SELECT max(id) FROM badges")

            await self.bot.SQL.query("\
                    REPLACE INTO badges\
                    SET description=\"{}\",\
                        name=\"{}\",\
                        thumbnail_path=\"{}\",\
                        start_available=\"{}-{}-01\",\
                        end_available=\"{}-{}-{}\";".format(\
                        desc,badgeName,badgeImageUrl,\
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

            gymRole = discord.utils.get(ctx.message.guild.roles,name="Gym Leader")
            await self.bot.add_roles(user,gymRole)
            await ctx.send("Gym Leader added:\nLeader: {}\nDescription: {}\nBadge Name: {}".format(user.mention,desc,badgeName))
        elif ltype.replace(" ","")[:9].lower() == "elitefour":
            ##Adds an Elite Four Member
            await self.bot.SQL.query("\
                    REPLACE INTO challengers\
                    SET user_fk={},\
                        name=\"Elite Four\",\
                        active=1,\
                        description=\"{}, {}\";".format(\
                        user.id,challengeMonth,challengeYear))

            eliteRole = discord.utils.get(ctx.message.guild.roles,name="Elite Four")
            await self.bot.add_roles(user,eliteRole)
            await ctx.send("Elite Four Added:\n{}".format(user.mention))
        else:
            await ctx.send("I'm not sure I got that. Please try again")

        self.bot.SQL.disconnect()

    @add.error
    async def add_error(ctx, error,other):
        if isinstance(error, commands.CheckFailure):
            await ctx.bot.say("You do not have the permission to add leaders. Please contact an Admin")

    @leader.command(pass_context=True)
    @commands.has_any_role('Admin','Mod','admin','Gym Leader')
    async def remove(self,ctx,ltype : str,user : discord.Member):
        """Sets a leader as inactive in the Frontier League"""
        if ltype.replace(" ","")[:3].lower() == "gym":
            await self.bot.SQL.connect()
            await self.bot.SQL.query("UPDATE challengers SET active=0 WHERE user_fk={} and name=\"Gym Leader\";".format(user.id))
            self.bot.SQL.disconnect()

            gymRole = discord.utils.get(ctx.message.guild.roles,name="Gym Leader")
            await self.bot.remove_roles(user,gymRole)

            await ctx.send("Gym Leader removed: {}".format(user.mention))
        elif ltype.replace(" ","")[:9].lower() == "elitefour":
            await self.bot.SQL.connect()
            await self.bot.SQL.query("UPDATE challengers SET active=0 WHERE user_fk={} and name=\"Elite Four\";".format(user.id))
            self.bot.SQL.disconnect()

            eliteRole = discord.utils.get(ctx.message.guild.roles,name="Elite Four")
            await self.bot.remove_roles(user,eliteRole)

            await ctx.send("Elite Four Member removed: {}".format(user.mention))
        else:
            await ctx.send("I'm not sure I got that. Please try again")

    @remove.error
    async def remove_error(ctx, error,other):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You do not have the permission to remove leaders. Please contact an Admin")

    @leader.command(pass_context=True)
    @commands.has_role('Frontier League Participant')
    async def challenge(self,ctx,ltype : str,user : discord.Member, challenger : discord.Member = None):
        """Challenge a leader
        leader challenge <ltype> <@user> [@challenger]
        """
        if 'leaderQueue' not in vars(self):
            await self.create_queue()
        if challenger is None:
            challenger = ctx.message.author
        await self.bot.SQL.connect()
        if ltype.replace(" ","")[:3].lower() == "gym":
            gymLeader = (await self.bot.SQL.query("SELECT user_fk FROM challengers WHERE active=1 and name=\"Gym Leader\" and user_fk={} ORDER BY id ASC;".format(user.id))).fetchone()#[0]
            await self.bot.say(gymLeader)
            if gymLeader is None:
                ctx.send("{} is not a Gym Leader".format(user.mention))
            else:
                if user.id not in self.leaderQueue["gym"]:
                    self.leaderQueue["gym"][user.id] = []
                self.leaderQueue["gym"][user.id].append(challenger.id)
        elif ltype.replace(" ","")[:9].lower() == "elitefour":
            eliteFour =await (await self.bot.SQL.query("SELECT user_fk, users.friendCode FROM challengers INNER JOIN users ON users.id=challengers.user_fk WHERE active=1 AND name=\"Elite Four\" and challengers.user_fk={} ORDER BY challengers.id ASC;".format(user.id))).fetchall()
            if eliteFour is None:
                ctx.send("{} is not in the Elite Four".format(user.mention))
            else:
                if user.id not in self.leaderQueue["elite"]:
                    self.leaderQueue["elite"][user.id] = []
                self.leaderQueue["elite"][user.id].append(challenger.id)

    @challenge.error
    async def chal_error(self,error,ctx):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("Something went wrong, please try again in a moment")
            print(error)
            await self.create_queue()
            await ctx.command.invoke(ctx.command,ctx)
        else:
            await ctx.send("Exception not caught")

    @leader.command(pass_context=True)
    @commands.has_role('Frontier League Participant')
    async def listQueue(self,ctx,leader : discord.Member):
        if 'leaderQueue' not in vars(self):
            await self.create_queue()
        value = ""
        if leader.id in self.leaderQueue["gym"]:
            value += "Gym:\n"
            for userId in self.leaderQueue["gym"][leader.id]:
                user = ctx.message.guild.get_member(userId)
                value += "{}\n".format(user.mention)
        if leader.id in self.leaderQueue["elite"]:
            value += "\nElite Four:\n"
            for userId in self.leaderQueue["elite"][leader.id]:
                user = ctx.message.guild.get_member(userId)
                value += "{}\n".format(user.mention)
        if value != "":
            em = discord.Embed(name="Leader Queue",description="Leader Queue for {}".format(leader.mention))
            em.add_field(value=value)
            await ctx.send(embed=em)
        else:
            await ctx.send("{} has 0 challengers in their queue!".format(leader.mention))

    @listQueue.error
    async def lqueue_error(self,error,ctx):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("Something went wrong, please try again in a moment")
            print("{}\n\n\n\n\n\n".format(error))
            await self.create_queue()
            await ctx.command.invoke(ctx)
        else:
            await ctx.send("Exception not caught")

def setup(bot):

    bot.add_cog(Leader(bot))
