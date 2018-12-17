import discord
from discord.ext import commands

class Snap():
    def __init__(self, bot):
        self.bot= bot
        self.roles = {}
        self.possible_victims = []

    @commands.command(pass_context=True)
    async def start(self, ctx):
        await self.bot.say("Initiation snap...")
        try:
            roleChoices = "Which role would you like...```"
            for i in ctx.message.server.roles:
                self.roles[i.id] = i
                roleChoices += "{} - {}\n".format(i.id, i.name)
            roleChoices += "```"
            await self.bot.say(roleChoices)
            msg = await self.bot.wait_for_message(author=ctx.message.author)
            baseRole = self.roles[msg.content]
            await self.get_susceptibles(ctx.message.server, baseRole)
            #newRole = await self.create_new_role(ctx.message.server, baseRole)
            #newChannel = await self.create_channel(ctx.message.server, newRole)
            await self.bot.say("Balance has been restored")
        except Exception as e:
            await self.bot.say("Error... exiting sequence\n```{}```".format(e))

    async def create_new_role(self, server, original_role):
        newName = "In_The_" + original_role.name + "_Stone"
        newRole = await self.bot.create_role(server, name=newName, reason="I don't feel so good......")
        return newRole

    async def create_channel(self, server, newRole):
        newChannel = await self.bot.create_channel(server, name="The stone of " + newRole.name)
        return newChannel


    async def get_susceptibles(self, server, baseRole):
        for i in server.members:
            for j in i.roles:
                if baseRole == j:
                    self.possible_victims.append(i)
        for i in self.possible_victims:
            print("{} is a possible victim".format(i.name))

def setup(bot):
    bot.add_cog(Snap(bot))
