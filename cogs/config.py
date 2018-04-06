import discord
from discord.ext import commands
from . import utility

import sql

class Config:
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

        self.db = sql.MySQL()

    @commands.group()
    async def prefix(self, ctx):
        if ctx.invoked_subcommand is not None:
            return
        prefix = self.db.serverGet(ctx.guild)['Prefix']
        await ctx.channel.send(f"Prefix for {ctx.guild.name} is `{prefix}`")

    @prefix.command(name="set")
    @commands.has_permissions(administrator=True)
    async def _prefix_set(self, ctx, new:int=None):
        if new is None:
            await ctx.invoke(self._prefix_reset)
            return
        self.db.serverSet(ctx.guild, 'Prefix', f"'{new}'")
        await ctx.channel.send(f"The prefix for {ctx.guild.name} has been set to `{new}`")

    @prefix.command(name="reset")
    @commands.has_permissions(administrator=True)
    async def _prefix_reset(self, ctx):
        self.db.serverSet(ctx.guild, 'Prefix', "'!'")
        await ctx.channel.send(f"The prefix for {ctx.guild.name} has been reset to `!`")

    @commands.command()
    async def welcome(self, ctx):
        if not await self.db.serverGet(ctx.guild)['WelcomeMsg'] is None:
            await ctx.channel.send(f"Current welcome message:\n{self.db.serverGet(ctx.guild)['WelcomeMsg']}\n"
                                   f"In: <#{self.sb.serverGet(ctx.guild)['WelcomeChannel']}>\n\n"
                                   f"Would you like to edit this? [Y/N]")
            await self.bot.wait





def setup(bot):
    print("Loaded!")
    bot.add_cog(Config(bot))