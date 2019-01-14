import discord
from discord.ext import commands

class Status():
    def __init__(self, bot):
        self.bot= bot

    @commands.command(pass_context=True)
    async def status(self, ctx,user : discord.Member = None):
        if user is None:
            user = ctx.message.author
        await self.bot.SQL.connect()
        qResult = await self.bot.SQL.query(\
              "select   badges.id as bid,\
                        badges.name as bname,\
                        challengers.name as cname,\
                        IF((SELECT 1 from user_to_badge where badge_fk=bid and user_fk={})=1,1,0) as earned \
               from badges\
               inner join challengers on challengers.badge_fk=badges.id\
               where challengers.active=1;".format(user.id))
        result = await qResult.fetchall()
        em = discord.Embed(title="**__All Currently Available Challenges__**",description=user.mention)
        challengeNames = ""
        badgeNames = ""
        earned = ""
        for row in result:
            challengeNames+="{}\n".format(row['cname'])
            badgeNames+="{}\n".format(row['bname'])
            earned+="{}\n".format("Earned" if row['earned']==1 else "Not Earned")
        em.add_field(name="__Challenge Type__", value=challengeNames)
        em.add_field(name="__Badge Name__", value=badgeNames)
        em.add_field(name="__Earned__", value=earned)
        await self.bot.send_message(ctx.message.channel,embed=em)
        self.bot.SQL.disconnect()


def setup(bot):
    bot.add_cog(Status(bot))
