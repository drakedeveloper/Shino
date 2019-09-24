# Importing Modules
import discord
import time
import asyncio
from datetime import datetime
from discord.ext import tasks, commands
from tinydb import TinyDB, Query
import os, shutil



class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Making necessary folders after joining a guild.	
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            os.mkdir(f'db/{guild.id}')
        except OSError:
            shutil.rmtree(f'db/{guild.id}')
            os.mkdir(f'db/{guild.id}')
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        shutil.rmtree(f'db/{guild.id}')

    # Config Command	
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def config(self, ctx):
        db = TinyDB(f'db/{ctx.guild.id}/config.json')
        query = Query
        embed_1 = discord.Embed(title="__**Configuration**__", description=f"Hello, {ctx.author.mention} to config the modmail option you need to provide me some options.", colour=0xbf3444, timestamp=datetime.utcnow())
        embed_1.add_field(name="*Categories*", value="First of all you need to provide me a name for the modmail category, type help for more information about how this system works.")
        embed_1.add_field(name="*Action*", value="Please right after this message send me the name that you wish the category to be named to.")
        embed_1.set_author(name=f'{self.bot.user.name}',  icon_url=f'{self.bot.user.avatar_url}')
        embed_1.set_footer(icon_url=f'{self.bot.user.avatar_url}', text='?help')
        msg1 = await ctx.channel.send(embed=embed_1)
        def cat_name_check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            cat_name = await self.bot.wait_for('message', check=cat_name_check, timeout=60)
        except asyncio.TimeoutError as error:
            await msg1.delete()
            er_msg_1 = await ctx.channel.send("It seems you're out of time please try again!")
            await er_msg_1.delete(delay=30)
        else:
            cat = await ctx.guild.create_category(name=cat_name.content, reason='Needed for the bot')
            await msg1.delete()
            embed_2 = discord.Embed(title="__**Configuration**__",
                                    description=f"Hello again, {ctx.author.mention} to config the modmail option there's one more thing to do.",
                                    colour=0xbf3444, timestamp=datetime.utcnow())
            embed_2.add_field(name="*Role*",
                              value="You need to provide me with the name of the role that you wish to accept the modmail requests and i'll make it for you.")
            embed_2.add_field(name="*Action*",
                              value="Please right after this message send me the name that you wish the role to be named to.")
            embed_2.set_author(name=f'{self.bot.user.name}',
                               icon_url=f'{self.bot.user.avatar_url}')
            embed_2.set_footer(icon_url=f'{self.bot.user.avatar_url}', text='?help')
            msg2 = await ctx.channel.send(embed=embed_2)
            def role_name_check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                role_name = await self.bot.wait_for('message', check=role_name_check, timeout=60)
            except asyncio.TimeoutError as error_2:
                await msg2.delete()
                er_msg_2 = await ctx.channel.send("It seems you're out of time please try again!")
                await er_msg_2.delete(delay=30)
            else:
                await msg2.delete()
                role = await ctx.guild.create_role(name=role_name.content, reason='Needed for the bot')
                role2 = await ctx.guild.create_role(name='Modmail user', reason='Needed for the bot')
                embed_3 = discord.Embed(title="__**Configuration**__",
                                        description=f"Alright now everything is done with the configuration and all is left is that i'm going to create a necessary role for my system you can change it's color or name later.",
                                        colour=0xbf3444, timestamp=datetime.utcnow())
                embed_3.add_field(name="*Category*",
                                  value="• You **can't**, delete a category made by the bot, what you can do is only rename it and position it.")
                embed_3.add_field(name="*Role*",
                                  value="• You **can't**, delete a role by the bot, what you can do is only rename it and position it and change the colour.")
                embed_3.set_author(name=f'{self.bot.user.name}',
                                   icon_url=f'{self.bot.user.avatar_url}')
                embed_3.set_footer(icon_url=f'{self.bot.user.avatar_url}', text='?help')
                msg3 = await ctx.channel.send(embed=embed_3)
                db.insert({'category_id': cat.id, 'role_id':role.id, 'guild_id': ctx.guild.id, 'role2_id': role2.id})

    @commands.command()
    async def help(self, ctx, command=None):
        if command == None:
            embed = discord.Embed(title="__**Help**__",
                                            description=f"You requested help about my commands.",
                                            colour=0xbf3444, timestamp=datetime.utcnow())
            embed.add_field(name="*?config*",
                                      value="• This command can only be used by an admin to make the necessary configuration in order for the bot to run correctly.`?help config` for more help about the command")
            embed.add_field(name="*?md*",
                                      value="• This command can be used by anyone to request the help of a mod, type `?help md` for more help about the command.")
            embed.set_author(name=f'{self.bot.user.name}',
                                       icon_url=f'{self.bot.user.avatar_url}')
            embed.set_footer(icon_url=f'{self.bot.user.avatar_url}', text='?help')
            await ctx.author.send(embed=embed)
            msg = await ctx.channel.send("I sent you a private message!")
            await msg.delete(delay=30)
        if str(command).lower() == 'md':
            embed1 = discord.Embed(title="__**Help**__",
                                  description=f"You requested help about my modmail command.",
                                  colour=0xbf3444, timestamp=datetime.utcnow())
            embed1.add_field(name="*?md*",
                            value="• This command can be used by anyone to request the help of a mod, when someone uses this command it will check if he has Modmail User role, if he has it means that he already have a modmail request, and if he doesn't, a channel in the specified category will be created, until one of the mods react to open it or close it, it will remain for 24 hours.")
            embed1.set_author(name=f'{self.bot.user.name}',
                             icon_url=f'{self.bot.user.avatar_url}')
            embed1.set_footer(icon_url=f'{self.bot.user.avatar_url}', text='?help')
            await ctx.author.send(embed=embed1)
            msg1 = await ctx.channel.send("I sent you a private message!")
            await msg1.delete(delay=30)
        if str(command).lower() == '?config':
            embed1 = discord.Embed(title="__**Help**__",
                                  description=f"You requested help about my config command.",
                                  colour=0xbf3444, timestamp=datetime.utcnow())
            embed1.add_field(name="*?modmail*",
                            value="• This command can be used only by an administrator to configure the necessary category and roles in order for me to work.")
            embed1.set_author(name=f'{self.bot.user.name}',
                             icon_url=f'{self.bot.user.avatar_url}')
            embed1.set_footer(icon_url=f'{self.bot.user.avatar_url}', text='?help')
            await ctx.author.send(embed=embed1)
            msg1 = await ctx.channel.send("I sent you a private message!")
            await msg1.delete(delay=30)


    #Handling Errors. 
    @config.error
    async def _config(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            msg1 = await ctx.send('<:stop:587970807909842944> Missing requiremen?')
            await msg1.delete(delay=5)
        if isinstance(error, commands.MissingRole):
            msg = await ctx.send('<:stop:587970807909842944> Ops! you can not use that command!')
            await msg.delete(delay=5)
        if isinstance(error, commands.BadArgument):
            msg2 = await ctx.send(
                '<:stop:587970807909842944> Something is wrong, try again!')
            await msg2.delete(delay=5)

        if isinstance(error, commands.CommandOnCooldown):
            msg9 = 'This command is ratelimited, please try again in {:.2f}seconds'.format(error.retry_after)
            msg6 = await ctx.send(msg9)
            await msg6.delete(delay=5)
        if isinstance(error, commands.MissingPermissions):
            msg1 = await ctx.send('<:stop:587970807909842944> Missing permission!')
            await msg1.delete(delay=5)

    @help.error
    async def _help(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            msg1 = await ctx.send('<:stop:587970807909842944> Missing requiremen?')
            await msg1.delete(delay=5)
        if isinstance(error, commands.MissingRole):
            msg = await ctx.send('<:stop:587970807909842944> Ops! you can not use that command!')
            await msg.delete(delay=5)
        if isinstance(error, commands.BadArgument):
            msg2 = await ctx.send(
                '<:stop:587970807909842944> Something is wrong, try again!')
            await msg2.delete(delay=5)

        if isinstance(error, commands.CommandOnCooldown):
            msg9 = 'This command is ratelimited, please try again in {:.2f}seconds'.format(error.retry_after)
            msg6 = await ctx.send(msg9)
            await msg6.delete(delay=5)
        if isinstance(error, commands.MissingPermissions):
            msg1 = await ctx.send('<:stop:587970807909842944> Missing permission!')
            await msg1.delete(delay=5)

def setup(bot):
    bot.add_cog(Config(bot))