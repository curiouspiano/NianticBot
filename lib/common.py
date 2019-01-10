import requests
import asyncio
from lib.mysql import *

#function loads our database with all of the existing pokemon, their ID/Name/shiny sprite
async def fetch_poke_data(bot):
    await bot.SQL.connect()
    baseSQL = "INSERT INTO shiny_ref(poke_id, name, image) VALUES({}, '{}', '{}')"
    baseLINK = "https://pokeapi.co/api/v2/pokemon/{}"
    
    for i in range(700):
        try:
            data = requests.get(baseLINK.format(i))
            data = data.json()
            poke_id = data["id"]
            poke_name = data["name"]
            shinyURL = data["sprites"]["front_shiny"]
            executeSQL = baseSQL.format(int(poke_id), poke_name, shinyURL)
            print(executeSQL)
            await bot.SQL.query(executeSQL)
            print("pokemon {} registered to the DB".format(poke_name))
            await asyncio.sleep(1)
        except Exception as e:
            print(e)
    bot.SQL.disconnect()

async def make_selection(bot, ctx, options):
    print("ey man make yo stuff here")