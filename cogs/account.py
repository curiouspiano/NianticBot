import discord
from discord.ext import commands

class Account:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def register(self, ctx):
        user = ctx.message.author
        discID = user.id
        trainerName = None
        trainerCode = None
        try:
            await self.bot.SQL.connect()
            result = await self.bot.SQL.query("SELECT id FROM users WHERE id={}".format(int(user.id)))
            if result.rowcount > 0:
                await self.bot.say("You're alread registered... xxx")
                return

            await self.bot.say("Alright, let's get you ready to fight!")
            await self.bot.say("First, I need your PokemonGO trainer name:")
            resp = await self.bot.wait_for_message(author=user, timeout=180)
            trainerName = resp.content
            await self.bot.say("Alright, now I need your friend code, please input it in one string <000000000000>")
            resp = await self.bot.wait_for_message(author=user, timeout=180)
            trainerCode = resp.content
            sqlStr = "INSERT INTO users(id, trainerName, friendCode) VALUES ({}, '{}', '{}')".format(int(user.id), trainerName, trainerCode)
            print(sqlStr)
            await self.bot.SQL.query(sqlStr)
            await self.bot.say("Welcome {} to the League!\n".format(user.name))
            await self.bot.SQL.disconnect()
        except Exception as e:
            await self.bot.say("There was an issue... please ensure you're not adding spaces to your responses and try again")
            print(e)


    @commands.command(pass_context=True)
    async def profile(self, ctx, user):
        await self.bot.send_typing(ctx.message.channel)
        mentions = ctx.message.mentions
        user = mentions[0]
        badgeCount = None
        badges = []
        sql = "SELECT * FROM user_to_badge WHERE user_fk={}".format(int(user.id))
        res = await self.bot.SQL.query(sql)
        badgeCount = res.rowcount
        res = await res.fetchall()
        print(res)
        sql = "SELECT * FROM users WHERE id={}".format(int(user.id))
        await self.bot.SQL.connect()
        res = await self.bot.SQL.query(sql)
        res = await res.fetchone()
        msg = discord.Embed(title=user.display_name, description="Trainer Name: {}\nFriend Code: {}\nBadge Count: {}\n".format(res['trainerName'], res['friendCode'], badgeCount))
        await self.bot.send_message(ctx.message.channel, embed=msg)

def setup(bot):
    bot.add_cog(Account(bot))
