from discord.ext import commands
import json
import logging
from os import listdir
from os.path import isfile, join
from random import *
from lib.mysql import mysqldb
import asyncio
import discord

cogs_dir = "cogs"
config = json.loads(open("config.json").read())
prefix = config["prefix"]
admins = config["admins"]

logging.basicConfig(format='%(asctime)s:%(message)s', filename="logging.log", level=logging.WARNING)

bot = commands.Bot(self_bot=False, description="Niantic...", command_prefix=prefix)

bot.SQL = mysqldb(bot.loop, config["dbHost"], config["dbUser"], config["dbPass"], config["dbName"])

def is_admin(ctx):
    return (str(ctx.message.author.id) in admins)


@bot.command()
@commands.check(is_admin)
async def load(ctx, extension_name):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await ctx.send(content="```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send(content="{} loaded.".format(extension_name))


@bot.command()
@commands.check(is_admin)
async def reload(ctx, extension_name):
    try:
        bot.unload_extension(extension_name)
        bot.load_extension(extension_name)
        await ctx.send(content="reload succesful")
    except Exception as e:
        print(e)
        await ctx.send(content="reload failed")


@bot.command()
@commands.check(is_admin)
async def unload(ctx, extension_name):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await ctx.send(content="{} unloaded.".format(extension_name))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    try:
        await bot.SQL.connect()
        bot.SQL.disconnect()
        print("Database connection succesfully established")
    except Exception as e:
        print("Issue establishing database conenction...\n{}".format(e))


if __name__ == "__main__":
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
            print("Loaded Extension: {}".format(extension))
        except Exception as e:
            logging.error('Failed to load extension \'{}\'. \n    Issue: {}'.format(extension, e))
    bot.run(config["token"], bot=True)
