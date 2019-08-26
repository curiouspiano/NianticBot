import discord
import logging
from discord.ext import commands
from datetime import datetime

class ShinyRef(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def embed_shiny(self, name, image, poke_id):
        embed = discord.Embed(title=name)
        embed.add_field(name="__Description__", value=poke_id, inline=False)
        embed.set_thumbnail(url=image)
        return embed

    @commands.group(pass_context=True)
    async def shiny(self, ctx):
        if ctx.invoked_subcommand is None:
            print("hey man. I need ")

    @shiny.command(pass_context=True)
    async def lookup(self, ctx, pokeName):
        await self.bot.SQL.connect()
        sqlString = "SELECT * FROM shiny_ref WHERE name='{}'".format(pokeName)
        resp = await self.bot.SQL.query(sqlString)
        if(resp.rowcount == 0):
            await ctx.send("I can't seem to find that pokemon in our database... DM a dev if you think this is an error")
        else:
            resp = await resp.fetchone()
            if resp['shiny'] == 1:
                name = resp['name']
                image = resp['image']
                poke_id = resp['poke_id']

                em = await self.embed_shiny(name, image, poke_id)
                await ctx.send(embed=em)
            else:
                await ctx.send("This pokemon does not have a shiny variant in pokemonGO yet...")
                                
        self.bot.SQL.disconnect()




def setup(bot):
    bot.add_cog(ShinyRef(bot))
