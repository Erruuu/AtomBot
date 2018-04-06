import discord
from discord.ext import commands

import sql

import asyncio

import traceback
import sys
import random

extensions = (
    'cogs.utility',
    'cogs.misc',
    'cogs.fun',
    'cogs.nsfw',
    'cogs.econ',
    'cogs.config',
    'cogs.mod'
)


class Atom(commands.Bot):
    def __init__(self, *args, **kwargs):
        self.token = "MzU4MzU0NTYwMDY4MDkxOTA0.DMzrUQ.p6D3fnE8nhkpJx9D8ZfZjFqrpYk"
        super().__init__(command_prefix=self.get_pre, owner_id=356268554494148608)

        self.db = sql.MySQL()

        self.run()

    async def get_pre(self, bot, message):
        return self.db.serverGet(message.guild)['Prefix']

    async def on_ready(self):
        self.remove_command("help")
        for ext in extensions:
            self.load_extension(ext)

        print("Ready!")

        status = ['>help', 'atom.erruuu.com']

        while True:
            for s in status:
                await self.change_presence(game=discord.Game(name=s, type=1))
                await asyncio.sleep(30)

    async def on_message(self, message):
        if not message.author.bot:
            if not self.db.userExists(message.author):
                print(f"Adding user {message.author.display_name} to the database")
                self.db.createUser(message.author)

            if not self.db.serverExists(message.guild):
                print(f"Adding server {message.guild.name} to the database")
                self.db.createServer(message.guild)

            await self.db.addXP(message, random.randint(1, 3))

        await self.process_commands(message)

    async def on_guild_join(self, guild):
        await guild.owner.send(f"**Hey, {guild.owner.name}! Thanks for adding me to your guild!**\n"
                                              "I am still in development so except issues here and there. To get started please use the `>help` command.\n\n"
                                              "**PLEASE MAKE SURE YOU GIVE ME THE 'EMBED LINKS' PERMISSION**\n"
                                              "It is required for most of my commands since they use \embeds. Otherwise the commands just wont work.\n\n"
                                              "If you would like to follow the development process or make a suggestion/complaint you can do so in my guild\n"
                                              "https://discord.gg/kNBWTpV")
        if not self.db.serverExists(guild):
            print(f"Adding server {message.guild.name} to the database")
            self.db.createServer(guild)

    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.UserInputError)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.channel.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.channel.send(f'Slow down, <@{ctx.author.id}>!')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.author.send(f'{ctx.command} ca ad n not be used in Private Messages.')
            except:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                return await ctx.channel.send('I could not find that member. Please try again.')

        elif isinstance(error, commands.CheckFailure):
            print(error.message)

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def run(self):
        super().run(self.token)

Atom()