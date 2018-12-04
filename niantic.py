import discord
import json
import time
from random import *
import asyncio

config = json.loads(open("config.json").read())
prefix = config["prefix"]
token = config["token"]
prefix = "?"
admins = ['366348310698655752', '151846248784199680']
client = discord.Client()

async def slow_send(channel, text):
    await client.send_typing(channel)
    await asyncio.sleep(2)
    await client.send_message(channel, text)
    
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    newGame = discord.Game(name="We did nothing wrong...")
    await client.change_presence(game=newGame)

@client.event
async def on_message(message):
        split = message.content.split(' ')
        if((message.author.id in admins) and message.content.startswith(prefix)):
            print("accessing admin commands")
            
        if(client.user.mentioned_in(message)):
            await client.send_typing(message.channel)
            await asyncio.sleep(2)
            if(randint(1,25) == 1):
                await client.send_file(message.channel, 'shiny.png')
            else:
                await client.send_message(message.channel, "¯\_(ツ)_/¯")
        #elif('bug' in split):
            #await slow_send(message.channel, "I have no clue what you're talking about. Bugs are a type of pokemon...")
            

client.run(token)
