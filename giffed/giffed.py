import os
from cogs.utils.dataIO import dataIO
import discord
from discord.ext import commands
from cogs.utils import checks
from random import choice, shuffle

class Giffed:
    """Shortcut for gifs."""
    
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(pass_context=True, no_pm=True)
    async def gregg(self, ctx):
        await self.bot.send_file(ctx.message.channel, filename="data/giffed/gregg.gif")
    
    @commands.command(pass_context=True, no_pm=True)
    async def mae(self, ctx):
        await self.bot.send_file(ctx.message.channel, filename="data/giffed/mae.gif")
    

def setup(bot):
    bot.add_cog(Giffed(bot))