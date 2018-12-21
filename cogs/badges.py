import discord
from discord.ext import commands
from datetime import datetime

class Badges:
    def __init__(self, bot):
        self.bot = bot

    async def badge_embed(self, user_id,badge_id):
        #returns an discord embed with badge info

        #obtain badge data and make the embed, this is for display without user data
        defaultImage = "https://i.imgur.com/g9VaBDJ.jpg"
        user = await self.bot.get_user_info(user_id)
        res = await self.bot.SQL.query("SELECT * FROM badges WHERE id={}".format(int(badge_id)))
        badgeInfo = await res.fetchone()
        desc = str(badgeInfo['description'])
        image = defaultImage
        if(badgeInfo['thumbnail_path'] != None):
            image = badgeInfo['thumbnail_path']
        title = badgeInfo['name']
        desc = "***{}***\n".format(desc)        
        embed = discord.Embed(title=title)
        embed.add_field(name="__Description__", value=desc, inline=False)
        
        #now we're gonna attach user info, if they've earned the badge
        res = await self.bot.SQL.query("SELECT earned, granter FROM user_to_badge WHERE user_fk={} AND badge_fk={}".format(int(user_id), str(badge_id)))
        if (res.rowcount > 0):
            dateInfo = await res.fetchone()
            granterName = "Unavailable"
            if dateInfo['granter'] != None:
                granterName = await self.bot.get_user_info(dateInfo['granter']).name
            embed.add_field(name="__Earned__", inline=False,value="Awarded to {} at {}. Awarded by {}".format(user.mention, dateInfo['earned'], granterName))

        else:
            embed.set_footer(text="You have not earned this badge")
        embed.set_thumbnail(url=image)
        return embed

    async def grant_badge(self, user_id, badge_id):
        sqlString = "SELECT * FROM user_to_badge WHERE user_fk={} AND badge_fk={}".format(int(user_id), str(badge_id))
        res = await self.bot.SQL.query(sqlString)
        if(res.rowcount > 0):
            return -1
        else:
            sqlString = "INSERT INTO user_to_badge(user_fk, badge_fk, earned) VALUES({}, '{}', '{}')".format(int(user_id), badge_id, datetime.now())
            print(sqlString)
            await self.bot.SQL.query(sqlString)
            return int(badge_id)

    @commands.group(pass_context=True)
    async def badge(self, ctx):
        """Lookup Badges, list earned, grant badges"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_message(ctx.message.channel,"You need a subcommand for this to work! Please try again")

    @badge.command(pass_context=True)
    async def grant(self, ctx):
        """Lets the commanding user grant a badge to the first tagged user.
            Usage: badge grant @user"""
        mentions = ctx.message.mentions
        user = None
        if(len(mentions) == 0):
            await self.bot.say("Please mention a user...")
            return
        else:
            user = mentions[0]
        await self.bot.SQL.connect()
        sqlString = "SELECT * FROM challengers WHERE user_fk={} AND active=1".format(ctx.message.author.id)
        res = await self.bot.SQL.query(sqlString)
        newBadge = -1
        if (res.rowcount == 1):
            #add badge if the user only has one badge available to grant
            res = await res.fetchone()
            print(res['badge_fk'])
            newBadge = await self.grant_badge(int(user.id), res['badge_fk'])
        elif (res.rowcount > 1):
            await self.bot.say("We need to figure out which badge you'd like to grant.")
            #determine which badge to add if they have more than one challenge active
        else:
            #user has no badges they can grant... get outta here 
            self.bot.SQL.disconnect()
            await self.bot.say("You do not have any badges to grant...")
            return
        
        if(newBadge > 0):
            await self.bot.say("Congratulations on earning the new badge")
            em = await self.badge_embed(int(user.id), newBadge)
            await self.bot.send_message(ctx.message.channel, embed=em)
        else:
            await self.bot.say("It would appear they already have that badge...")
        self.bot.SQL.disconnect()

    @badge.command(pass_context=True)
    async def lookup(self, ctx, badge_name):
        """Used to lookup a badge
            usage: badge lookup 'badge name'"""
        sqlString = "SELECT * FROM badges WHERE name='{}'".format(badge_name)
        await self.bot.SQL.connect()
        resp = await self.bot.SQL.query(sqlString)
        if (resp.rowcount == 0):
            await self.bot.say("Hmm... can't seem to find that badge, make sure you surround the name with quotes")
            return
        badgeData = await resp.fetchone()
        badgeID = badgeData['id']

        em = await self.badge_embed(int(ctx.message.author.id), badgeID)
        self.bot.SQL.disconnect()
        await self.bot.send_message(ctx.message.channel, embed=em)

    @badge.command(pass_context=True)
    async def test(self, ctx):
        userId = 151846248784199680
        badgeId = 5
        await self.bot.SQL.connect()
        em = await self.badge_embed(userId, badgeId)
        #used to test badge related commands
        self.bot.SQL.disconnect()
        await self.bot.send_message(ctx.message.channel, embed=em)

def setup(bot):
    bot.add_cog(Badges(bot))
