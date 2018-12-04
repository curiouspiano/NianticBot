import discord
from discord.ext import commands

class Shrug():
    def __init__(self, bot):
        self.bot= bot

    async def on_message(self, message):
        print("bot was mentioned")
        print(message.content)
        print("searching if " + self.bot.user.id + "in message")
        if(self.bot.user.mentioned_in(message)):
            await self.bot.send_message(message.channel, '¯\_(ツ)_/¯')


def setup(bot):
    bot.add_cog(Shrug(bot))
