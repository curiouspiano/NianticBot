import requests
import asyncio
from lib.mysql import *

INDEX_TO_EMOJI = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣"]
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
    #uni function to let a user make a decision based on an array of options
    #bot - bot object, used for interacting
    #ctx - context object that invoked the command
    #options - array of strings, returns the value, not index
    
    msg = "Please react with your choice\n"
    for i in range(len(options)):
        msg += "{} - {}\n".format(INDEX_TO_EMOJI[i], options[i])

    priMessage = await bot.send_message(ctx.message.channel, msg)

    reactionOptions = []

    for i in range(len(options)):
        reactionOptions.append(INDEX_TO_EMOJI[i])
        await bot.add_reaction(priMessage, INDEX_TO_EMOJI[i])

    choice = await bot.wait_for_reaction(emoji=reactionOptions, user=ctx.message.author, message=priMessage, timeout=180)
    
    answer = choice.reaction.emoji

    final = options[reactionOptions.index(answer)]

    await bot.delete_message(priMessage)

    return final
