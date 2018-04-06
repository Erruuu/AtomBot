import discord
from discord.ext import commands
from discord.ext.commands import context

import time
import sql
import random
import asyncio


class Econ:
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

        self.db = sql.MySQL()

    @commands.command(pass_context=True)
    async def bal(self, ctx, *, member:discord.Member = None):
        if member is None:
            member = ctx.author

        await ctx.channel.send(embed=discord.Embed(
            title=f"{member.display_name}'s balance",
            description=f"${self.db.userGet(member)['Money']}",
            color=ctx.author.color
        ))

    @commands.command(pass_context=True)
    async def daily(self, ctx):
        last = self.db.userGet(ctx.author)['LDaily']
        since = time.time()-last
        if since > 86400:
            await ctx.channel.send(embed=discord.Embed(
                description="You have received your daily $200!",
                color=0x00ff00
            ))
            self.db.addMoney(ctx.author, 200)
            self.db.updateDaily(ctx.author)
        else:
            m, s = divmod(int(86400-since), 60)
            h, m = divmod(m, 60)
            await ctx.channel.send(embed=discord.Embed(
                description=f"You can't claim your daily $200 for another **%dh %02dm %02ds**" % (h, m, s),
                color=0xff0000
            ))

    @commands.command(pass_context=True)
    async def donate(self, ctx, amt:int, rec:discord.Member=None):
        snd = ctx.author
        if not self.db.userGet(snd)['Money'] >= amt:
            await ctx.channel.send(embed=discord.Embed(
                description="You do not have enough money. Check your balance using `>bal`",
                color=0xff0000
            ))
            return
        confCode = random.randint(11111,99999)
        conf = await ctx.channel.send(embed=discord.Embed(
            title="Confirm Donation",
            description=f"Type confirmation code `{str(confCode)}` to complete the donation",
            color=0xffff00
        ))

        def check(m):
            return (m.content == str(confCode)) and (m.author == snd)

        try:
            await self.bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            await conf.edit(embed=discord.Embed(
                description="Confirmation not sent, donation canceled",
                color=0xff0000
            ))
            return
        else:
            await conf.delete()
            await ctx.channel.send(embed=discord.Embed(
                title="Donation sent!",
                description=f"${str(amt)} has been removed from your balance and added to {rec.display_name}'s balance",
                color=0x00ff00
            ))

        self.db.addMoney(rec, amt)
        self.db.delMoney(snd, amt)

    @commands.command(pass_context=True)
    async def level(self, ctx, user:discord.Member=None):
        if user is None:
            user = ctx.author

        level = self.db.userGet(user)['Level']
        xp = self.db.userGet(user)['XP']
        toNext = (level*150)-xp

        bar = ("█"*int(xp/level/15))+(" ​"*int(10-(xp/level/15)))

        await ctx.channel.send(embed=discord.Embed(
            title=f"Level: {str(level)}",
            description=f"{str(xp)} `{bar}` {str(level*150)}",
            color=user.color
        ))


    # ADMIN
    @commands.command(pass_context=True)
    @commands.is_owner()
    async def add_money(self, ctx, amt:int, user:discord.Member=None):
        if user is None:
            user = ctx.author
        self.db.addMoney(user, amt)
        await ctx.channel.send(f"${str(amt)} has been added to {user.display_name}'s balance")

    @commands.command(pass_context=True)
    @commands.is_owner()
    async def add_xp(self, ctx, amt:int, user:discord.Member=None):
        if user is None:
            user = ctx.author
        await self.db.addXP(ctx.message, amt, user=user)
        await ctx.channel.send(f"{str(amt)}xp has been added to {user.display_name}")


def setup(bot):
    print("Loaded!")
    bot.add_cog(Econ(bot))