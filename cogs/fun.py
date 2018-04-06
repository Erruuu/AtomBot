import discord
from discord.ext import commands
from discord.ext.commands import context

import asyncio
import os
import colorsys

from imgurpython import ImgurClient

import random

class Fun:
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

        self.imgur = ImgurClient('a7a517a27f5cb30', '8587bb31ad9b16494ac4f1b5318bf224f65fd043')

    @commands.cooldown(2,7)
    @commands.command(name="flip", pass_context=True, aliases=["coin"])
    async def flip(self, ctx):
        """Flip a coin"""
        await ctx.channel.send(embed=discord.Embed(
            color = ctx.author.color,
            description = "**{0}** flipped a coin and got **{1}**".format(ctx.author.display_name, ["Heads", "Tails"][random.randint(0,1)])
        ))

    @commands.cooldown(2,7)
    @commands.command(name="roll", pass_context=True, aliases=["dice"])
    async def roll(self, ctx):
        await ctx.channel.send(embed=discord.Embed(
            color = ctx.author.color,
            description = "**{0}** rolled a die and got **{1}**".format(ctx.author.display_name, str(random.randint(1,6)))
        ))

    @commands.cooldown(2,7)
    @commands.command(name="8ball", pass_context=True)
    async def ball(self, ctx):
        lines = ["It is certain",
                 "It is decidedly so",
                 "Without a doubt",
                 "Yes definitely",
                 "You may rely on it",
                 "As I see it, yes",
                 "Most likely",
                 "Outlook good",
                 "Yes",
                 "Signs point to yes",
                 "Reply hazy try again",
                 "Ask again later",
                 "Better not tell you now",
                 "Cannot predict now",
                 "Concentrate and ask again",
                 "Don't count on it",
                 "My reply is no",
                 "My sources say no",
                 "Outlook not so good",
                 "Very doubtful"]
        response = random.randint(0, len(lines)-1)
        if response < 10:
            col = 0x00ff00
        elif response < 15:
            col = 0xffff00
        else:
            col = 0xff0000
        await ctx.channel.send(embed=discord.Embed(
            color=col,
            description=lines[response]
        ))

    @commands.cooldown(3,10)
    @commands.command(name="kill", pass_context=True)
    async def kill(self, ctx, member: discord.Member):
        if member == self.bot.user:
            await ctx.channel.send("You can't kill me! I am invincible! Muahahahaha")
            return

        blocked = {'362990084527489026': 'No! She is too amazing to die!!!', '356268554494148608': "No point, he'll end up killing himself anyway ¯\_(ツ)_/¯"}

        if str(member.id) in blocked.keys():
            await ctx.channel.send(blocked[str(member.id)])
            return

        if member == ctx.message.author:
            lines = ["{0} took the easy way out",
                     "{0} drank bleach",
                     "{0} took 'hang in there' way too literally",
                     "{0} jumped in front of a bus",
                     "{0} took too many acid pills",
                     "{0} ate a tide pod"]
        else:
            lines = ["{0} put bleach in {1}'s IV drip",
                     "{0} spiked {1}'s drink with cyanide",
                     "{1} fell victim to {0}'s cunning plan >:D",
                     "{1} got bitch slapped to the moon by {0}",
                     "{0} succeeded where {1}'s parents' abortion clinic failed",
                     "{1} spotted {0} and dropped dead in fear"]

        await ctx.channel.send(embed=discord.Embed(
            color=ctx.author.color,
            description=lines[random.randint(0, len(lines) - 1)].format("**"+ctx.author.display_name+"**", "**"+member.display_name+"**"))
        )

    @commands.cooldown(2,15)
    @commands.command(name="hug", pass_context=True)
    async def hug(self, ctx, member: discord.Member, id: int=None):
        gifs = self.imgur.get_album_images('jVkSq')

        if id is None:
            id = random.randint(0,len(gifs)-1)

        await ctx.channel.send(embed=discord.Embed(
            description="**{0}** hugged **{1}**".format(ctx.author.display_name, member.display_name),
            color=member.color
        ).set_image(
            url=gifs[id].link
        ).set_footer(
            text="ID: {0}".format(id)
        ))

    @commands.cooldown(2,10)
    @commands.command(name="ship", pass_context=True)
    async def ship(self, ctx, m1: str, m2: str):
        rating = abs(hash(m1) - hash(m2)) % 101
        bar = ("█"*int(rating/10))+(" ​"*int(10-(rating/10)))
        hex = "0x{:02x}{:02x}{:02x}".format(int(255-(255*(rating/100))),int(255*(rating/100)),0)

        await ctx.channel.send("💕 **MATCHMAKING** 💕\n"
                                    "🔻 {0}\n"
                                    "🔺 {1}".format(m1, m2),
                               embed=discord.Embed(
            description="**{0}%** `{1}`".format(rating, bar),
            color=int(hex, 16)
        ))

def setup(bot):
    print("Loaded!")
    bot.add_cog(Fun(bot))
