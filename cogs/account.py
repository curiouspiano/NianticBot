import discord
import logging
from discord.ext import commands
from datetime import date
from lib.common import *

class Account(commands.Cog):
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
                await ctx.send("You're alread registered... xxx")
                self.bot.SQL.disconnect()
                return
            msg1 = await ctx.send("Alright, let's get you ready to fight!")
            msg2 = await ctx.send("First, I need your PokemonGO trainer name:")

            def check(message):
                return message.author == user

            resp = await self.bot.wait_for('message', check=check, timeout=180)

            trainerName = resp.content
            await resp.delete()
            await msg1.delete()
            await msg2.delete()

            msg1 = await ctx.send("Alright, now I need your friend code, please input it in one string <000000000000>")

            resp = await self.bot.wait_for('message', check=check, timeout=180)

            trainerCode = resp.content
            trainerCode = trainerCode.strip("<")
            trainerCode = trainerCode.strip(">")
            trainerCode = trainerCode.strip(" ")
            await msg1.delete()
            await resp.delete()
            nick = user.name
            sqlStr = "INSERT INTO users(id, nick, trainerName, friendCode, joinDate) VALUES ({}, '{}', '{}', '{}', '{}')".format(int(user.id), nick, trainerName, trainerCode, date.today())
            await self.bot.SQL.query(sqlStr)
            await ctx.send("Welcome {} to the League!\n".format(nick))
            self.bot.SQL.disconnect()
            #
            try:
                bfRole = None
                bfRole = discord.utils.get(ctx.message.guild.roles, name="Frontier League Participant")
                await ctx.message.author.add_roles(bfRole)
            except Exception as e:
                logging.warning(e)
                await ctx.send("....however, I can not assign you the role, sorry.")

        except Exception as e:
            logging.warning(e)
            await ctx.send("There was an issue... please ensure you're not adding spaces to your responses and try again")


    @commands.group(pass_context=True)
    async def profile(self, ctx):
        """Used to access the players profile, or view anothers' by using @user"""
        if ctx.invoked_subcommand is None:
            async with ctx.channel.typing():
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
                    await ctx.send("That user doesn't seem to be registered in the league... Let them know to register!")
                else:
                    res = await res.fetchone()
                    desc = "Trainer Name: {}\n".format(res['trainerName'])
                    desc += "Friend Code: {}\n".format(res['friendCode'])
                    desc += "Join Date: {}\n".format(res['joinDate'])
                    msg = discord.Embed(title=user.display_name, description=desc)
                    await ctx.send(embed=msg)
                self.bot.SQL.disconnect()

    @profile.command(pass_context=True)
    async def edit(self, ctx):
        """Usage :::"""

        user = ctx.message.author

        options = ["Name", "Friend Code"]

        choice = await make_selection(self.bot, ctx, options)
        
        await ctx.send("Alright, editing [{0}]. What is your new [{0}]?".format(choice))

        def check(message):
            return message.author == user

        resp = await self.bot.wait_for('message', check=check, timeout=180)

        await self.bot.SQL.connect()
        sql = None

        if choice == "Name":
            sql = "UPDATE users SET trainerName='{0}' WHERE id='{1}'".format(resp.content, int(user.id))

        elif choice == "Friend Code":
            sql = "UPDATE users SET friendCode='{0}' WHERE id='{1}'".format(resp.content, int(user.id))

        res = await self.bot.SQL.query(sql)
        self.bot.SQL.disconnect()

        await ctx.send("Your {0} has been updated to {1}".format(choice, str(resp.content)))

def setup(bot):
    bot.add_cog(Account(bot))
