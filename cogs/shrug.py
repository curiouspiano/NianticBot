import discord
from discord.ext import commands

class Shrug(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    async def on_message(self, message):
        if(self.bot.user.mentioned_in(message) and message.author != self.bot.user and not message.mention_everyone):
            await self.bot.send_message(message.channel, '¯\_(ツ)_/¯')


def setup(bot):
    bot.add_cog(Shrug(bot))
