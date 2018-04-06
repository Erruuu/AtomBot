import discord
from discord.ext import commands
from discord.ext.commands import context

import asyncio

class Mod:
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.command()
    async def prune(self, ctx, amount:int):
        await ctx.message.delete()
        messages = []
        async for m in ctx.channel.history(limit=amount):
            messages.append(m)
        await ctx.channel.delete_messages(messages)
        c = await ctx.channel.send(f"Deleted {amount} messages from {ctx.channel.name}")
        await asyncio.sleep(5)
        await c.delete()


def setup(bot):
    print("Loaded!")
    bot.add_cog(Mod(bot))
