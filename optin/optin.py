import os
from cogs.utils.dataIO import dataIO
from discord.ext import commands
from cogs.utils import checks
from __main__ import send_cmd_help


class OptIn:
    def __init__(self, bot):
        self.bot = bot
        self.path = "data/optin/settings.json"
        self.settings = dataIO.load_json(self.path)
        self.roles =   [["nflirl","NFL Discussion"],
                        ["nbairl","NBA Discussion"],
                        ["swtlj","Star Wars: The Last Jedi Spoilers"],
                        ["mirror", "Black Mirror Channel"],
                        ["pal","Pooty Pals Channel"]]
                        
    def _set_default(self, id):
        self.settings[id] = {
            "ENABLED": False
        }
        dataIO.save_json(self.path, self.settings)

    def _is_role_in_list(self, server, role):
        return (role.lower() in [i[0] for i in self.roles])
    

    @commands.command(name="optin", pass_context=True, no_pm=True)
    async def _optin(self, ctx, role: str):
        """Gain the requested role if available."""
        user = ctx.message.author
        server = ctx.message.server
        add = None
        if not self.settings[server.id]["ENABLED"]:
            return

        if self._is_role_in_list(server, role):
            try:
                role = role.lower()
                r = [x for x in server.roles if x.name.lower() == role][0]
                if r:
                    add = r
            except IndexError:
                await self.bot.say("Role not found/not requestable!")
                return

        if add:
            await self.bot.add_roles(user, add)
            await self.bot.delete_message(ctx.message)
            


    @commands.command(name="optout", pass_context=True, no_pm=True)
    async def _optout(self, ctx, role: str):
        """Drop the optional role."""
        user = ctx.message.author
        server = ctx.message.server

        if not self.settings[server.id]["ENABLED"]:
            return

        if self._is_role_in_list(server, role):
            try:
                rem = role.lower()
                await self.bot.remove_roles(user, rem)
                await self.bot.delete_message(ctx.message)
            except IndexError:
                await self.bot.say("Role not found/not removable!")
                return


            

    @commands.group(no_pm=True, pass_context=True)
    async def optset(self, ctx):
        """Change various settings for Opt-In"""
        server = ctx.message.server
        if server.id not in self.settings.keys():
            self._set_default(server.id)
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @optset.command(no_pm=True, pass_context=True)
    @checks.admin_or_permissions(manage_roles=True)
    async def toggle(self, ctx, state: str):
        """Changes or displays the state of requesting roles"""
        trues = ["true", "on", "enabled", "enable", "1"]
        falses = ["false", "off", "disabled", "disable", "0"]
        server = ctx.message.server

        s = self.settings[server.id]["ENABLED"]

        if state.lower() in trues:
            s = True
        elif state.lower() in falses:
            s = False
        else:
            await self.bot.say("Current state: {}".format(str(s).lower()))
            return

        self.settings[server.id]["ENABLED"] = s
        dataIO.save_json(self.path, self.settings)
        await self.bot.say("Set toggle state to {}".format(str(s).lower()))

    @optset.command(no_pm=True, pass_context=True, name="list")
    async def _list(self, ctx):
        """Lists all requestable roles"""
        server = ctx.message.server
        try:
            roles = self.roles
        except KeyError:
            roles = []

        if roles:
            roles = "\n".join(["\t".join(r) for r in roles])
            await self.bot.say("""Requestable roles:\n{}""".format(roles))
        else:
            await self.bot.say("""Requestable roles:\n(none available)""")

def check_folders():
    if not os.path.exists("data/optin"):
        print("Creating data/optin folder...")
        os.makedirs("data/optin")


def check_files():
    f = "data/optin/settings.json"
    if not dataIO.is_valid_json(f):
        print("Creating default Opt-In's settings.json...")
        dataIO.save_json(f, {})


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(OptIn(bot))
