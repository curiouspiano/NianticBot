from discord.ext import commands
import json
from os import listdir
from os.path import isfile, join
from random import *
import asyncio
import discord

cogs_dir = "cogs"
config = json.loads(open("config.json").read())
prefix = config["prefix"]

bot = commands.Bot(self_bot=False, description="Niantic...", command_prefix=prefix)

@bot.command(hidden=True)
async def link():
    link = "https://discordapp.com/oauth2/authorize?client_id={}&scope=bot"
    await bot.say(link.format(bot.user.id))

@bot.command(hidden = True)
async def load(extension_name : str):
    """Loads an extension."""
    try:
        bot.load_extension(extension_name)
    except (AttributeError, ImportError) as e:
        await bot.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await bot.say("{} loaded.".format(extension_name))

@bot.command(hidden=True)
async def reload(extension_name : str):
    try:
        bot.unload_extension(extension_name)
        bot.load_extension(extension_name)
        await bot.say("reload succesful")
    except Exception as e:
        print(e)
        await bot.say("reload failed")

@bot.command(hidden=True)
async def unload(extension_name : str):
    """Unloads an extension."""
    bot.unload_extension(extension_name)
    await bot.say("{} unloaded.".format(extension_name))

@bot.command(hidden=True)
async def shutdown():
    """Shuts down the bot"""
    bot.client.logout()
    bot.client.close()
    exit()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


            
if __name__ == "__main__":
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except Exception as e:
            print('Failed to load extension {extension}.', extension)
    bot.run(config["token"], bot=True)
