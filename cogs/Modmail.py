# Importing Modules
import discord
import time
import asyncio
from datetime import datetime
from discord.ext import tasks, commands
from tinydb import TinyDB, Query
import os, shutil



class Modmail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # Modmail Command.
    @commands.command()
    async def md(self, ctx, reason=None):
        db = TinyDB(f'db/{ctx.guild.id}/config.json')
        query = Query()
        search = db.search(query.guild_id == ctx.guild.id)
        if len(search) == 0:
            msg = await ctx.channel.send("Needed configuration!")
            await msg.delete(delay=30)
        if len(search) != 0:
            try:
                embed = discord.Embed(title="__**Mod Mail**__",
                                      description=f"Your request has been sent to the mods , if they don't respond within 24 hours then your request has been closed.",
                                      colour=0x42f2f5, timestamp=datetime.utcnow())
                embed.set_author(name=f'{self.bot.user.name}',
                                 icon_url=f'{self.bot.user.avatar_url}')
                embed.set_footer(icon_url=f'{self.bot.user.avatar_url}', text='t!help')
                msg1 = await ctx.author.send(embed=embed)
            except:
                await ctx.channel.send("It seems that your DMS are closed , open them and try again!")
            else:
                for items in search:
                    role2 = items['role2_id']
                    role5 = ctx.guild.get_role(role2)
                    li = role5.members
                    if ctx.author not in li:
                        await ctx.author.add_roles(role5)
                        cat = ctx.guild.get_channel(items['category_id'])
                        role = ctx.guild.get_role(items['role_id'])
                        overwrites = {
                            role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False)
                        }
                        channel = await ctx.guild.create_text_channel(name=ctx.author.name, overwrites=overwrites, category=cat, reason=reason)

                        embed2 = discord.Embed(title="__**Mod Mail**__",
                                              description=f"{ctx.author.mention} has requested a mod mail, open it by reacting with ?? or close it with ??.",
                                              colour=0x42f2f5, timestamp=datetime.utcnow())
                        embed.add_field(name="**Reason**", value=f"{reason}")
                        embed2.set_author(name=f'{self.bot.user.name}',
                                         icon_url=f'{self.bot.user.avatar_url}')
                        embed2.set_footer(icon_url=f'{self.bot.user.avatar_url}', text='t!help')
                        msg2 = await channel.send(embed=embed2)
                        await msg2.add_reaction('??')
                        await msg2.add_reaction('??')
                        def reaction_check(reaction, user):
                            return (str(reaction.emoji) == '??' or str(reaction.emoji) == '??') and user != self.bot.user
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=86400, check=reaction_check)
                        except asyncio.TimeoutError:
                            await msg1.delete()
                            await msg2.delete()
                            embed9 = discord.Embed(title='__**Mod Mail**__',
                                                   description="Your request has been declined automatically since nobody opened it within 24 hours.",
                                                   colour=0xf59c42, timestamp=datetime.utcnow())
                            msg3 = await ctx.author.send(embed9=embed9)
                            await ctx.author.remove_roles(role5)
                            await asyncio.sleep(3600)
                            await channel.delete()
                            await msg3.delete()

                        else:
                            await msg1.delete()
                            await msg2.delete()
                            if str(reaction.emoji) == '??' and user != self.bot.user:
                                embed1 = discord.Embed(title='__**Mod Mail**__', description="Your request has been accepted now anything you type here is gonna be delivered to the mods.", colour=0xa7f542, timestamp=datetime.utcnow())
                                embed1.set_footer(icon_url=f'{self.bot.user.avatar_url}', text='t!help')
                                embed1.set_author(name=f'{self.bot.user.name}',
                                                  icon_url=f'{self.bot.user.avatar_url}')
                                msg4 = await ctx.author.send(embed=embed1)
                                embed3 = discord.Embed(title='__**Mod Mail**__', description="You have opened this request now anything you type here is gonna be delivered to the request owner.to close the request just type. ?close", colour=0xa7f542, timestamp=datetime.utcnow())
                                embed3.set_footer(icon_url=f'{self.bot.user.avatar_url}', text='t!help')
                                embed3.set_author(name=f'{self.bot.user.name}',
                                                  icon_url=f'{self.bot.user.avatar_url}')
                                msg5 = await channel.send(embed=embed3)
                                while True:
                                    def mod_checl(m):
                                        return m.channel == channel or m.channel == msg1.channel and m.author != self.bot.user

                                    mod = await self.bot.wait_for('message', check=mod_checl)
                                    if mod.channel == channel and mod.content.startswith('?close') != True:
                                        embed_5 = discord.Embed(description=f"{mod.content}", colour=0xf59042, timestamp=datetime.utcnow())
                                        embed_5.set_footer(icon_url=f'{self.bot.user.avatar_url}', text='t!help')
                                        embed_5.set_author(name=f'{mod.author}',
                                                          icon_url=f'{mod.author.avatar_url}')
                                        await ctx.author.send(embed=embed_5)
                                    if mod.channel == msg1.channel:
                                        embed_5 = discord.Embed( description=f"{mod.content}",
                                                                colour=0xf54266, timestamp=datetime.utcnow())
                                        embed_5.set_footer(icon_url=f'{self.bot.user.avatar_url}', text='t!help')
                                        embed_5.set_author(name=f'{mod.author}',
                                                           icon_url=f'{mod.author.avatar_url}')
                                        await channel.send(embed=embed_5)
                                    if mod.channel == channel and mod.content.startswith('?close') == True:
                                        embed6 = discord.Embed(title='__**Mod Mail**__',
                                                               description="Your request has been closed .",
                                                               colour=0xf54242, timestamp=datetime.utcnow())
                                        embed6.set_footer(icon_url=f'{self.bot.user.avatar_url}', text='t!help')
                                        embed6.set_author(name=f'{self.bot.user.name}',
                                                          icon_url=f'{self.bot.user.avatar_url}')
                                        await ctx.author.send(embed=embed6)
                                        await channel.delete()
                                        await ctx.author.remove_roles(role5)
                                        break

                            if str(reaction.emoji) == '??'and user != self.bot.user:
                                embed7 = discord.Embed(title='__**Mod Mail**__',
                                                       description="Your request has been declined.",
                                                       colour=0xf54242, timestamp=datetime.utcnow())
                                embed7.set_footer(icon_url=f'{self.bot.user.avatar_url}', text='t!help')
                                embed7.set_author(name=f'{self.bot.user.name}',
                                                  icon_url=f'{self.bot.user.avatar_url}')
                                await ctx.author.send(embed=embed7)
                                await ctx.author.remove_roles(role5)
                                await channel.delete()
                    if ctx.author in li:
                        msg9 = await ctx.channel.send("OOps, it seems you already have opened a mod mail!")
                        await msg9.delete(delay=30)

    # Handling Errors.		
    @md.error
    async def _md(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            msg1 = await ctx.send('<:stop:587970807909842944> Missing requirement!')
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
    bot.add_cog(Modmail(bot))























