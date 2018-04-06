import discord
from discord.ext import commands
from discord.ext.commands import context

import asyncio

from googletrans import Translator
from googletrans import LANGUAGES

import time
import datetime

class Misc:
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

        self.translator = Translator()

    @commands.group(pass_context=True, name="info")
    async def info(self, ctx, sub):
        if sub is None:
            await self.bot.send_message(ctx.message.channel, "Usage: *blah ill sort this later*")

    @commands.command(name="ping", pass_context=True)
    @commands.cooldown(3, 5)
    async def ping(self, ctx):
        ptime = time.time()
        tmp = await ctx.channel.send(embed=discord.Embed(
            title="Pong!",
            description="Time taken: --",
            color=0x2ecc71
        ))
        ping = time.time() - ptime
        await tmp.edit(embed=discord.Embed(
            title="Pong!",
            description="Time taken: {0:.01f}ms".format(ping),
            color=0x2ecc71
        ))

    @commands.group(pass_context=True)
    async def info(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.invoke(self._info_server)
            return


    @info.command(pass_context=True, name="user", aliases=["u", "member", "m"])
    async def _info_user(self, ctx, *, member:discord.Member=None):
        if member is None:
            member = ctx.author
        await ctx.channel.send(embed=discord.Embed(
            color=member.color
        ).set_author(
            name="{0}#{1}".format(member.name, member.discriminator),
            icon_url=member.avatar_url
        ).set_thumbnail(
            url=member.avatar_url
        ).add_field(
            name="User ID",
            value=member.id,
            inline=True
        ).add_field(
            name="Nickname",
            value=member.display_name,
            inline=True
        ).add_field(
            name="Role",
            value=member.top_role,
            inline=True
        ).add_field(
            name="Status",
            value=member.status,
            inline=True
        ).add_field(
            name="Account Created",
            value=member.created_at.strftime("%A, %B %d, %Y @ %H:%M UTC"),
            inline=False
        ).add_field(
            name="Joined Server",
            value=member.joined_at.strftime("%A, %B %d, %Y @ %H:%M UTC"),
            inline=False
        ))

    @info.command(pass_context=True, name="server", aliases=["s", "guild", "g"])
    async def _info_server(self, ctx, server:discord.Guild=None):
        if server is None:
            server = ctx.guild
        await ctx.channel.send(embed=discord.Embed(
            color=ctx.message.author.color
        ).set_author(
            name="{0}".format(server.name),
            icon_url=server.icon_url
        ).set_thumbnail(
            url=server.icon_url
        ).add_field(
            name="Server ID",
            value=server.id,
            inline=True
        ).add_field(
            name="Region",
            value=server.region,
            inline=True
        ).add_field(
            name="Owner",
            value=server.owner.name,
            inline=True
        ).add_field(
            name="Members",
            value=str(server.member_count),
            inline=True
        ).add_field(
            name = "Server Created",
            value = server.created_at.strftime("%A, %B %d, %Y @ %H:%M UTC"),
            inline = False
        ))

    @info.command(pass_context=True, name="role", aliases=["r"])
    async def _info_role(self, ctx, role:discord.Role):
        perms = ["create_instant_invite",
                 "kick_members",
                 "ban_members",
                 "administrator",
                 "manage_channels",
                 "manage_server",
                 "add_reactions",
                 "read_messages",
                 "send_messages",
                 "send_tts_messages",
                 "manage_messages",
                 "embed_links",
                 "attach_files",
                 "read_message_history",
                 "mention_everyone",
                 "external_emojis",
                 "connect",
                 "speak",
                 "mute_members",
                 "deafen_members",
                 "move_members",
                 "use_voice_activation",
                 "change_nickname",
                 "manage_nicknames",
                 "manage_roles",
                 "manage_webhooks",
                 "manage_emojis"]
        rperms = []
        for p in perms:
            if eval("role.permissions." + p + " == 1"):
                rperms.append(p)
        await ctx.channel.send(embed=discord.Embed(
            color=role.color
        ).set_author(
            name=role.name
        ).add_field(
            name="Role ID",
            value=role.id,
            inline=True
        ).add_field(
            name="Position",
            value=str(role.position),
            inline=True
        ).add_field(
            name="Displayed Separately",
            value=str(role.hoist),
            inline=True
        ).add_field(
            name="Role Created",
            value=role.created_at.strftime("%A, %B %d, %Y @ %H:%M UTC"),
            inline=False
        ).add_field(
            name="Permissions",
            value=" - ".join(rperms),
            inline=False
        ))

    @info.command(pass_context=True, name="emoji", aliases=["e"])
    async def _info_emoji(self, ctx, emoji:discord.Emoji=None):
        await ctx.channel.send(embed=discord.Embed(
            color=ctx.author.color
        ).set_author(
            name=":{0}:".format(emoji.name),
            icon_url=emoji.url
        ).set_thumbnail(
            url=emoji.url
        ).add_field(
            name="Emoji ID",
            value=emoji.id,
            inline=True
        ).add_field(
            name="Server",
            value=emoji.guild.name,
            inline=True
        ).add_field(
            name="Emoji Created",
            value=emoji.created_at.strftime("%A, %B %d, %Y @ %H:%M UTC"),
            inline=False
        ))

    @commands.command(pass_context=True)
    async def suggest(self, ctx, *, suggestion:str):
        ch = discord.utils.find(lambda c: c.name == 'suggestions', ctx.guild.channels)
        if ch is None:
            await ctx.channel.send(embed=discord.Embed(
                title="Error!",
                description="#Suggestions channel could not be found",
                color=0xff0000
            ))
            return

        msg = await ch.send(embed=discord.Embed(
            description=suggestion,
            color=ctx.author.color
        ).set_author(
            name="Suggestion by {0}".format(ctx.author.name),
            icon_url=ctx.author.avatar_url
        ))

        await msg.add_reaction('\U0001F44D')
        await msg.add_reaction('\U0001F44E')

        await ctx.channel.send(embed=discord.Embed(
            description="Your suggestion has been posted!",
            color=0x00ff00
        ))

    @commands.command(pass_context=True, name="feedback", aliases=['complain'], usage=">feedback <message>")
    async def feedback(self, ctx, *, msg:str):
        await self.bot.get_channel(406953807700951050).send(embed=discord.Embed(
            description=msg,
            color=ctx.author.color
        ).set_author(
            name=f'{ctx.author.name}#{ctx.author.discriminator} <{ctx.author.id}>',
            icon_url=ctx.message.author.avatar_url
        ).set_footer(
            text=f'{ctx.guild.name} <{ctx.guild.id}>',
            icon_url=ctx.guild.icon_url
        ))

    @feedback.error
    async def _feedback_error(self, ctx, error):
        if isinstance(error, commands.userInputError):
            await ctx.send()

    @commands.command(pass_context=True, name="translate")
    async def translate(self, ctx, to:str, *, msg:str):
        if to not in LANGUAGES:
            await ctx.channel.send(embed=discord.Embed(
                title="ERROR",
                description="Invalid target language provided",
                color=0xff0000
            ))
        translated = self.translator.translate(msg, dest=to)
        await ctx.channel.send(embed=discord.Embed(
            color=ctx.author.color
        ).add_field(
            name=f"Original ({LANGUAGES.get(translated.src).title()})",
            value=msg,
            inline=False
        ).add_field(
            name=f"Translated ({LANGUAGES.get(translated.dest).title()})",
            value=(translated.text if translated.pronunciation is None else f"{translated.text}\n*({translated.pronunciation})*"),
            inline=False
        ))

def setup(bot):
    print("Loaded!")
    bot.add_cog(Misc(bot))
