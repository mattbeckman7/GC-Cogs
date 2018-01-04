import os
from cogs.utils.dataIO import dataIO
import discord
from discord.ext import commands
from cogs.utils import checks
from random import choice, shuffle
import aiohttp
import functools
import asyncio
import json

GUGGY_URL = "http://text2gif.guggy.com/v2/guggify"

class Guggy:
    """Get captioned GIFs from Guggy."""
    
    def __init__(self, bot):
        self.bot = bot
        self.path = "data/guggy/settings.json"
        self.settings = dataIO.load_json(self.path)
        

    @commands.command(pass_context=True, no_pm=True)
    async def guggy(self, ctx, *keywords):
        """Usage: /guggy text caption here"""
        chan = ctx.message.channel
    
        if keywords:
            keywords = " ".join(keywords)
        else:
            await self.bot.send_cmd_help(ctx)
            return

        req_head = {"Content-Type":"application/json", "apiKey":self.settings["GUGGY_API_KEY"]}
        req_body = {"sentence":keywords}

        async with aiohttp.post(GUGGY_URL, data=json.dumps(req_body), headers=req_head) as r:
            result = await r.json()
            if r.status == 200:
                if result["reqId"]:
                    try:
                        e = discord.Embed()
                        e.set_image(url=result["animated"][0]["gif"]["hires"]["secureUrl"])
                        await self.bot.send_message(chan, embed=e)
                    except:
                        await self.bot.say("Error loading image.")
                else:
                    await self.bot.say("No results found.")
            else:
                await self.bot.say("Error contacting the API")
            


    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(administrator=True)
    async def guggyapi(self, ctx, guggyapi: str):
        self.settings["GUGGY_API_KEY"] = guggyapi
        dataIO.save_json(self.path, self.settings)
        await self.bot.delete_message(ctx.message)
        await self.bot.say("Guggy API Key Updated")
        

def check_folders():
    if not os.path.exists("data/guggy"):
        print("Creating data/guggy folder...")
        os.makedirs("data/guggy")


def check_files():
    f = "data/guggy/settings.json"
    if not dataIO.is_valid_json(f):
        print("Creating default Guggy's settings.json...")
        dataIO.save_json(f, {})


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Guggy(bot))
