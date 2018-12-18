import discord
from discord.ext import commands

class Badges:
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Badges(bot))
