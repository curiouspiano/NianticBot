import discord
from discord.ext import commands

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def link(self, ctx):
        await ctx.send(content="https://discordapp.com/api/oauth2/authorize?client_id={}&permissions=0&scope=bot".format(self.bot.user.id))

    @commands.command(pass_context=True)
    async def source(self, ctx):
        await ctx.send(content="https://github.com/curiouspiano/NianticBot")
"""
    @commands.command(pass_context=True)
    async def upDateParticipants(self, ctx):
        if int(ctx.message.author.id) != 151846248784199680:
            await sctx.send(content="Yeah right")
            return
        await self.bot.SQL.connect()
        sqlString = "SELECT id FROM users"
        res = await self.bot.SQL.query(sqlString)
        res = await res.fetchall()
        bfRole = discord.utils.get(ctx.message.server.roles, name="Frontier League Participant")
        for i in res:
            try:
                member = discord.utils.get(ctx.message.server.members, id=str(i['id']))            
                await self.bot.add_roles(member, bfRole)
            except Exception as e:
                print(e)
        self.bot.SQL.disconnect()
"""
def setup(bot):
    bot.add_cog(Utilities(bot))