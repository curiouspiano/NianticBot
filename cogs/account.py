import discord
from discord.ext import commands
from datetime import date

class Account:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def register(self, ctx):
        user = ctx.message.author
        discID = user.id
        trainerName = None
        trainerCode = None
        nick = user.display_name
        try:
            await self.bot.SQL.connect()
            result = await self.bot.SQL.query("SELECT id FROM users WHERE id={}".format(int(user.id)))
            if result.rowcount > 0:
                await self.bot.say("You're alread registered... xxx")
                self.bot.SQL.disconnect()
                return
            msg1 = await self.bot.say("Alright, let's get you ready to fight!")
            msg2 = await self.bot.say("First, I need your PokemonGO trainer name:")
            resp = await self.bot.wait_for_message(author=user, timeout=180)
            trainerName = resp.content
            await self.bot.delete_message(msg1)
            await self.bot.delete_message(msg2)
            msg1 = await self.bot.say("Alright, now I need your friend code, please input it in one string <000000000000>")
            resp = await self.bot.wait_for_message(author=user, timeout=180)
            trainerCode = resp.content
            trainerCode = trainerCode.strip("<")
            trainerCode = trainerCode.strip(">")
            trainerCode = trainerCode.strip(" ")
            trainerCode
            await self.bot.delete_message(msg1)
            await self.bot.delete_message(resp)
            nick = user.name
            sqlStr = "INSERT INTO users(id, nick, trainerName, friendCode, joinDate) VALUES ({}, '{}', '{}', '{}', '{}')".format(int(user.id), nick, trainerName, trainerCode, date.today())
            await self.bot.SQL.query(sqlStr)
            await self.bot.say("Welcome {} to the League!\n".format(nick))
            self.bot.SQL.disconnect()
        except Exception as e:
            await self.bot.say("There was an issue... please ensure you're not adding spaces to your responses and try again")
            print(e)


    @commands.command(pass_context=True)
    async def profile(self, ctx):
        await self.bot.send_typing(ctx.message.channel)
        mentions = ctx.message.mentions
        user = None
        if(len(mentions) == 0):
            user = ctx.message.author
        else:
            user = mentions[0]
        badgeCount = None
        badges = []
        await self.bot.SQL.connect()
        sql = "SELECT * FROM user_to_badge WHERE user_fk={}".format(int(user.id))
        res = await self.bot.SQL.query(sql)
        badgeCount = res.rowcount
        res = await res.fetchall()
        sql = "SELECT * FROM users WHERE id={}".format(int(user.id))
        res = await self.bot.SQL.query(sql)
        if(res.rowcount == 0):
            await self.bot.say("That user doesn't seem to be registered in the league... Let them know to register!")
        else:
            res = await res.fetchone()
            desc = "Trainer Name: {}\n".format(res['trainerName'])
            desc += "Friend Code: {}\n".format(res['friendCode'])
            desc += "Join Date: {}\n".format(res['joinDate'])
            msg = discord.Embed(title=user.display_name, description=desc)
            await self.bot.send_message(ctx.message.channel, embed=msg)
        self.bot.SQL.disconnect()

def setup(bot):
    bot.add_cog(Account(bot))