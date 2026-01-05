from discord.ext import commands
import asyncio
import random

from utils import log, lang, generate_random_string, random_cooldown
import config_selfbot


class RaidCommands(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.is_spamming: bool = False

    @commands.command()
    async def kickall(self, ctx: commands.Context):
        if ctx.author.guild_permissions.kick_members:
            members = ctx.guild.members
            
            await ctx.message.edit(lang.text('raid_in_process'))

            log.separate_text("KICK ALL")

            for member in members:
                if ctx.guild.me.top_role > member.top_role:
                    await member.kick(reason=f"{config_selfbot.kick_reason} {generate_random_string(6)}")
                    log.success(f"@{member.name}({member.id}")
                    await asyncio.sleep(random_cooldown(0.4, 1.1))

            log.separate("KICK ALL")

            await ctx.message.edit(lang.text('raid_kick_all_success'), delete_after=config_selfbot.deltime)
        else:
            await ctx.message.edit(lang.text('raid_error_permisssion'), delete_after=config_selfbot.deltime)

    @commands.command()
    async def banall(self, ctx: commands.Context):
        if ctx.author.guild_permissions.ban_members:
            members = ctx.guild.members

            await ctx.message.edit(lang.text('raid_in_process'))

            log.separate_text("BAN ALL")

            for member in members:
                if ctx.guild.me.top_role > member.top_role:
                    await member.ban(reason=f"{config_selfbot.ban_reason}. {generate_random_string(6)}")
                    log.success(f"@{member.name}({member.id}")
                    await asyncio.sleep(random_cooldown(0.4, 1.1))

            log.separate("BAN ALL")

            await ctx.message.edit(lang.text('raid_ban_all_success'), delete_after=config_selfbot.deltime)
        else:
            await ctx.message.edit(lang.text('raid_error_permisssion'), delete_after=config_selfbot.deltime)

    @commands.command()
    async def spam(self, ctx: commands.Context):
        message_split = ctx.message.content.split()
        content = ctx.message.content.replace(f"{message_split[0]} {message_split[1]} ", "")

        try:
            count = int(message_split[1]) - 1
        except Exception:
            await ctx.message.edit(f"{lang.text('spam_invalid')}!", delete_after=config_selfbot.deltime)
            return
        
        if count >= 100:
            await ctx.message.edit(lang.text('spam_too_much'), delete_after=config_selfbot.deltime)
            return

        try:
            message_split[2]
        except Exception:
            await ctx.message.edit(lang.text('raid_dm_all_fail'), delete_after=config_selfbot.deltime)
            return

        if not self.is_spamming:
            self.is_spamming = True

            await ctx.message.edit(content)

            for i in range(count):
                await ctx.channel.send(content)
                await asyncio.sleep(random_cooldown(0.4, 1.2))
            self.is_spamming = False
        else:
            await ctx.message.edit(lang.text('spam_cooldown'), delete_after=config_selfbot.deltime)

    @commands.command()
    async def flood(self, ctx: commands.Context):
        flood_spam = '_ _\n' * 44
        await ctx.message.edit(flood_spam)
        for i in range(2):
            await ctx.channel.send(flood_spam)
            await asyncio.sleep(0.5)

    # TODO:
    # Add: `nuke` command that will delete all channel and all roles.

    @commands.command()
    async def exe(self, ctx: commands.Context):
        """Auto-respond to a mentioned user with random messages"""
        try:
            # Get mentions
            if not ctx.message.mentions:
                await ctx.message.edit(lang.text('raid_error_permisssion'), delete_after=config_selfbot.deltime)
                return
            
            target_user = ctx.message.mentions[0]
            
            # Parse messages from command
            message_split = ctx.message.content.split()
            # Remove command and mention from the split
            messages_str = ctx.message.content.replace(f"{message_split[0]} {message_split[1]} ", "")
            
            # Split messages by comma
            messages = [msg.strip() for msg in messages_str.split(",")]
            
            if len(messages) < 1:
                await ctx.message.edit("Please provide at least one message!", delete_after=config_selfbot.deltime)
                return
            
            # Store the auto-response
            if not hasattr(self.bot, 'exe_responses'):
                self.bot.exe_responses = {}
            
            self.bot.exe_responses[target_user.id] = messages
            
            await ctx.message.edit(f"✅ Auto-response set for {target_user.mention}!\nMessages: {len(messages)}", delete_after=config_selfbot.deltime)
            log.success(f"Exe command activated for user {target_user.name}({target_user.id}) with {len(messages)} messages")
            
        except Exception as e:
            await ctx.message.edit(f"Error: {str(e)}", delete_after=config_selfbot.deltime)
            log.error(f"Error in exe command: {e}")
