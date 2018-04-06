import discord
from discord.ext import commands

from . import utils

import random

class Nsfw:
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.is_nsfw()
    @commands.command(pass_context=True)
    async def e621(self, ctx, *, tags: str):
        tags = tags.replace(' ', '_')
        tags = tags.replace(',_', ' ')

        url = 'https://e621.net/post/index.json'
        params = {'limit': 320,
                  'tags': tags}

        msg = await ctx.channel.send(embed=discord.Embed(
            description="Searching...",
            color=ctx.author.color
        ))

        data = await utils.request(url, payload=params)

        if data is None:
            await msg.edit(embed=discord.Embed(
                title="ERROR",
                description="I had trouble connecting, try again later",
                color=0xff0000
            ))
            return

        try:
            result = data[random.SystemRandom().randint(0, len(data) - 1)]
            for i in result:
                print(i)
            await msg.edit(embed=discord.Embed(
                description=f"Score: {result['score']}",
                color=ctx.author.color
            ).set_image(
                url=result['file_url']
            ))
        except (ValueError, KeyError):
            await msg.edit(embed=discord.Embed(
                description="No image found with given tags 3;",
                color=0xff0000
            ))
            return


def setup(bot):
    print("Loaded!")
    bot.add_cog(Nsfw(bot))
