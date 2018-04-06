import discord
from discord.ext import commands

import sql
import asyncio
import re

from discord.ext.commands import formatter

class Utility:
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

        self.db = sql.MySQL()

        self._mentions_transforms = {
            '@everyone': '@\u200beveryone',
            '@here': '@\u200bhere'
        }

        self._mention_pattern = re.compile('|'.join(self._mentions_transforms.keys()))

    def is_owner(ctx):
        return ctx.message.author.id == "356268554494148608"

    @commands.command()
    async def help(self, ctx):
        await ctx.channel.send(embed=discord.Embed(
            title="Help",
            description="[Support Server](https://discord.gg/8fj9VQu)\n"
                        "[Official Site](http://atom.erruuu.com/)",
            color=ctx.author.color
        ))

    # -----BOT OWNER ONLY-----
    @commands.command(hidden=True)
    @commands.is_owner()
    async def set_name(self, ctx, name:str):
        await self.bot.user.edit(username=name)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def set_status(self, ctx, status:str):
        await self.bot.change_presence(game=discord.Game(name=status, type=1))
        with open("./status.txt", "w") as f:
            f.truncate()
            f.write(status)
            f.close

    @commands.command(pass_context=True, hidden=True)
    @commands.is_owner()
    async def send_msg(self, ctx, *, message:str):
        await ctx.channel.send(message)
        await ctx.message.delete()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def edit_msg(self, ctx, id:int, *, new:str):
        await self.bot.get_channel(id).edit(new)
        await ctx.message.delete()

    @commands.command(hidden=True)
    @commands.check(is_owner)
    async def msg_owners(self, message:str):
        for s in self.bot.guilds:
            await s.owner.send(message)


def setup(bot):
    print("Loaded!")
    bot.add_cog(Utility(bot))
