import os
from cogs.utils.dataIO import dataIO
import discord
from discord.ext import commands
from cogs.utils import checks
from random import choice, shuffle

class Faces:
    """Shortcut for faces."""
    
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(pass_context=True, no_pm=True)
    async def lenny(self, ctx):
        await self.bot.edit_message(ctx.message, "( ͡° ͜ʖ ͡°)")
    

    @commands.command(pass_context=True, no_pm=True)
    async def shrug(self, ctx):
        await self.bot.edit_message(ctx.message, "{} ¯\_(ツ)_/¯".format(repalce(ctx.message, "/shrug", "")))
    

def setup(bot):
    bot.add_cog(Faces(bot))
