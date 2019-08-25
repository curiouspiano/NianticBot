import discord
from discord.ext import commands

class Example(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @commands.command(pass_context=True)
    async def test(self, ctx):
        await self.bot.say("HI, this is an example Cog!")


def setup(bot):
    bot.add_cog(Example(bot))