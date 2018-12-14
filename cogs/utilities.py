import discord
from discord.ext import commands

class Utilities():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def link(self, ctx):
        await self.bot.say("https://discordapp.com/api/oauth2/authorize?client_id={}&permissions=0&scope=bot".format(self.bot.user.id))

def setup(bot):
    bot.add_cog(Utilities(bot))