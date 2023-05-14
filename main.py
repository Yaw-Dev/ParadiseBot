import discord
import asyncio
import datetime
import os
import json
import re
import time
from discord.ext import commands

bot = commands.Bot(command_prefix=['=', '.'], intents=discord.Intents.all(), case_insensitive=True)
#------------------------

@bot.command(name='purge', aliases=['clear'], help="Deletes a specified ammount of messages on a channel. (max: 100)")
@commands.has_permissions(manage_messages=True)
@commands.cooldown(3, 25, commands.BucketType.channel)  
async def purge(ctx, amount: int):
    print("[@bot.command] Purge was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass

    me = ctx.guild.me
    if not me.guild_permissions.manage_messages:
        return await ctx.send("I do not have the necessary permissions to purge messages. (Manage Messages)")
    if not ctx.author.guild_permissions.manage_guild:
        await ctx.send('You cannot perform this action due to missing permissions. (Manage Messages)', delete_after=5)
        return

    if amount > 100:
        await ctx.send("You cannot delete more than 100 messages at a time.", delete_after=5)
        return
    
    messages = await ctx.channel.history(limit=amount).flatten()
    num_deleted = len(messages)
    now = datetime.datetime.utcnow()
    old_messages = [msg for msg in messages if (now - msg.created_at).days >= 14]

    if old_messages:
        await ctx.send("You cannot delete messages that are older than 14 days. Please try again with a smaller amount.", delete_after=5)
        return

    if num_deleted > 1:
        await ctx.channel.delete_messages(messages)
        await ctx.send(f'Successfully purged **{num_deleted}** message(s)', delete_after=5)
    else:
        await ctx.send("No messages were found to delete.", delete_after=5)
#------------------------

@bot.command(name="setslowmode", help="Allows the user to set a custom value for slowmode in the current channel. (Seconds)")
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 20, commands.BucketType.channel)
async def slowmode(ctx, seconds: int=None):
    print("[@bot.command] Setslowmode was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass

    me = ctx.guild.me
    if not me.guild_permissions.manage_messages:
        return await ctx.send("I do not have the necessary permissions to change the slowmode. (Manage Server)")
    if not ctx.author.guild_permissions.manage_guild:
        await ctx.send('You cannot perform this action due to missing permissions. (Manage Server)', delete_after=5)
        return
    
    if seconds is None:
        await ctx.send("Please input a time value in seconds. (eg: .setslowmode 2)", delete_after=5)
        return

    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f'Slowmode has been set to {seconds} second(s).')
#------------------------

@bot.command(name='invite', aliases=['inv', 'authurl'], help="Displays the Bot's OAuth URL (all perms)")
@commands.cooldown(2, 20, commands.BucketType.channel)  
async def invite(ctx):
    print("[@bot.command] Invite was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass
    auth_url = discord.utils.oauth_url(bot.user.id, permissions=discord.Permissions.all())
    await ctx.send(f'My OAuth URL:\n> {auth_url}')
#------------------------

@bot.command(name='support', aliases=['home'], help="Invite to the Bot's Support Server.")
@commands.cooldown(2, 20, commands.BucketType.channel)  
async def support(ctx):
    print("[@bot.command] Support was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass
    invite_url = f'https://discord.gg/KYRGHm3Ccy'
    await ctx.send(f'Need help? Join our support server: {invite_url}')
#------------------------

@bot.command(name='source', help="Gives out the github repo of the bot.")
@commands.cooldown(2, 20, commands.BucketType.channel)  
async def support(ctx):
    print("[@bot.command] Source was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass
    repourl = f'https://github.com/AWeirDKiD/ParadiseBot'
    await ctx.send(f'Yes! I am open source: {repourl}')
#------------------------

@bot.command(name="echo", help="Repeats whatever the user says.")
@commands.cooldown(3, 15, commands.BucketType.channel)  
async def echo(ctx, *, message: str):
    print("[@bot.command] Echo was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass
    await ctx.send(message)
#------------------------

@bot.command(name="serverinfo", help="Displays information about the server.")
@commands.cooldown(1, 15, commands.BucketType.channel)
async def serverinfo(ctx):
    print("[@bot.command] Serverinfo was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass

    embed = discord.Embed(title='Server Information', color=discord.Color.blue())
    embed.add_field(name='Server Name', value=ctx.guild.name)
    embed.add_field(name='Server Owner', value=ctx.guild.owner)
    embed.add_field(name='Creation Date', value=ctx.guild.created_at.strftime("%m/%d/%Y %I:%M %p"))
    embed.add_field(name='Member Count', value=ctx.guild.member_count)
    embed.add_field(name='Channel Count', value=len(ctx.guild.text_channels) + len(ctx.guild.voice_channels))
    embed.add_field(name='Role Count', value=len(ctx.guild.roles))
    embed.set_thumbnail(url=ctx.guild.icon_url)

    await ctx.send(embed=embed)
#------------------------

@bot.command(name="userinfo", help="Displays information about a user.")
@commands.cooldown(3, 15, commands.BucketType.channel)
async def userinfo(ctx, member: discord.Member = None):
    print("[@bot.command] Userinfo was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass

    if member is None:
        member = ctx.author

    embed = discord.Embed(title='User Information', color=discord.Color.blue())
    embed.add_field(name='Username', value=member.name)
    embed.add_field(name='Discriminator', value=member.discriminator)
    embed.add_field(name='User ID', value=member.id)
    embed.add_field(name='Creation Date', value=member.created_at.strftime("%m/%d/%Y %I:%M %p"))
    embed.add_field(name='Nickname', value=member.nick if member.nick else 'None')
    embed.add_field(name='Status', value=member.status)
    embed.add_field(name='Nitro Status', value='Yes ✅' if member.premium_since else 'No ❌')
    activity = member.activity
    if activity:
        activity_type = activity.type.name.capitalize()
        activity_name = activity.name
        activity_string = f"{activity_type} {activity_name}"
        embed.add_field(name='Activity', value=activity_string)
    else:
        embed.add_field(name='Activity', value='None')
    embed.add_field(name='Top Role', value=member.top_role)
    embed.set_thumbnail(url=member.avatar_url)

    await ctx.send(embed=embed)
#------------------------

start_time = time.time()
def uptime():
    current_time = time.time()
    uptime = current_time - start_time

    days = int(uptime // 86400)
    hours = int(uptime % 86400 // 3600)
    minutes = int(uptime % 3600 // 60)
    seconds = int(uptime % 60)

    uptime_str = "**Current Uptime:**"
    if days > 0:
        uptime_str += " " + str(days) + " days"
    if hours > 0:
        uptime_str += " " + str(hours) + " hours"
    if minutes > 0:
        uptime_str += " " + str(minutes) + " minutes"
    if seconds > 0:
        uptime_str += " " + str(seconds) + " seconds"

    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%d-%m-%Y %H:%M:%S')
    current_time_str = datetime.datetime.fromtimestamp(current_time).strftime('%d-%m-%Y %H:%M:%S')
    uptime_str += "\n\n**Start Date:** " + start_time_str + "\n**Current Date:** " + current_time_str
    return uptime_str


@bot.command(name='uptime', aliases=['awaketime'], help="Displays the bot's current uptime and start date.")
@commands.cooldown(2, 30, commands.BucketType.channel)
async def appuptime(ctx):
    print("[@bot.command] Uptime was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass
    uptime_str = uptime()
    embed = discord.Embed(title="Online Status", description=uptime_str, color=discord.Color.green())
    embed.set_thumbnail(url="https://raw.githubusercontent.com/AWeirDKiD/ParadiseBot/cb3778d1927340a9413cbb46a5781e89c87f8e86/assets/logo.png")
    await ctx.send(embed=embed)
#----------------------

@bot.command(name="nuke", aliases=["nukechannel"], help="Nukes the channel the command was executed on (acts as a cleanup tool).")
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1, 60, commands.BucketType.guild)  
async def nuke(ctx):
    print("[@bot.command] Nuke was executed")
    channel = ctx.channel
    member = ctx.author
    parent = channel.category
    position = channel.position
    await channel.delete()
    new_channel = await ctx.guild.create_text_channel(channel.name, category=parent, position=position)
    embed = discord.Embed()
    embed.add_field(name="Channel Nuked!", value=f"Requested by: {member.mention}")
    embed.set_image(url="https://i.imgur.com/7mLOXVT.gif")
    await new_channel.send(embed=embed)
#----------------------

@bot.command(name='warn', help="Gives out a warning to the specified user.")
@commands.has_permissions(manage_messages=True)
@commands.cooldown(3, 15, commands.BucketType.channel)  
async def warn(ctx, member: discord.Member = None, *, reason=None):
    print("[@bot.command] Warn was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass
    if not member:
        await ctx.send("Please specify a user to warn.", delete_after=5)
        return
    me = ctx.guild.me
    if member == ctx.author:
        return await ctx.send("You cannot warn yourself!")
    if member.top_role >= ctx.author.top_role:
        return await ctx.send("You cannot perform this action on this user due to role hierarchy.")
    if not me.guild_permissions.manage_roles:
        return await ctx.send("I do not have the necessary permissions to mute members. (Manage Roles)")
    if member.bot:
        return await ctx.send("I'm unable to warn a bot.")

    if not os.path.exists(f'data/warns/{ctx.guild.id}.json'):
        with open(f'data/warns/{ctx.guild.id}.json', 'w') as f:
            json.dump({}, f)
    
    with open(f'data/warns/{ctx.guild.id}.json', 'r') as f:
        warns = json.load(f)
    
    warns[str(member.id)] = warns.get(str(member.id), 0) + 1
    
    with open(f'data/warns/{ctx.guild.id}.json', 'w') as f:
        json.dump(warns, f)
    
    if warns[str(member.id)] >= 5:
        await member.ban(reason=f'Reached the maximum number of warns ({5})')
        await ctx.send(f'**{member}** has been banned for reaching the maximum number of warns ({5})')
    else:
        if reason:
            await ctx.send(f'**{member}** has been warned. They now have {warns[str(member.id)]} warnings. Reason: {reason}')
            await member.send(f"You have been warned in **{ctx.guild.name}** for *{reason}*. You now have {warns[str(member.id)]} warnings.")
        else:
            await ctx.send(f'**{member}** has been warned. They now have {warns[str(member.id)]} warnings.')
            await member.send(f"You have been warned in **{ctx.guild.name}**. You now have {warns[str(member.id)]} warnings.")


@bot.command(name='removewarn', aliases=['rw'], help="Removes a specified amount of warns from a User.")
@commands.has_permissions(manage_roles=True)
@commands.cooldown(3, 15, commands.BucketType.channel)  
async def removewarn(ctx, member: discord.Member = None, number: int=1):
    print("[@bot.command] Removewarn was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass
    if not member:
        await ctx.send("Please specify a user to remove warns from.", delete_after=5)
        return
    me = ctx.guild.me
    if not me.guild_permissions.manage_roles:
        return await ctx.send("I do not have the necessary permissions to warn members. (Manage Roles)")
    if member.top_role >= ctx.author.top_role:
        return await ctx.send("You cannot perform this action on this user due to role hierarchy.")

    if not os.path.exists(f'data/warns/{ctx.guild.id}.json'):
        await ctx.send("This server has no warns to remove.", delete_after=5)
        return
    
    me = ctx.guild.me
    if member.top_role >= me.top_role:
        return await ctx.send("I cannot perform this action on this user due to role hierarchy.")
    if member.top_role >= ctx.author.top_role:
        return await ctx.send("You cannot perform this action on this user due to role hierarchy.")
    if not member:
        await ctx.send("Please specify a user to remove warns from.", delete_after=5)
        return
    
    with open(f'data/warns/{ctx.guild.id}.json', 'r') as f:
        warns = json.load(f)
    
    if str(member.id) not in warns or warns[str(member.id)] == 0:
        await ctx.send("This member has no warns to remove.", delete_after=5)
        return
    
    removed = min(number, warns[str(member.id)])
    warns[str(member.id)] = max(0, warns[str(member.id)] - removed)

    with open(f'data/warns/{ctx.guild.id}.json', 'w') as f:
        json.dump(warns, f)
    
    await ctx.send(f'Removed {removed} warnings for **{member}**. They now have {warns[str(member.id)]} warns.', delete_after=5)


@bot.command(name='viewwarns', aliases=['vw', 'warns'], help="Displays the specified user's total Warns.")
@commands.has_permissions(manage_roles=True)
@commands.cooldown(3, 15, commands.BucketType.channel)  
async def viewwarns(ctx, member: discord.Member = None):
    print("[@bot.command] Viewwarns was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass
    if not member:
        await ctx.send("Please specify a user. (Error: Missing Arguments)", delete_after=5)
        return
    me = ctx.guild.me
    if member.top_role >= me.top_role:
        return await ctx.send("I cannot perform this action on this user due to role hierarchy.")
    if member.top_role >= ctx.author.top_role:
        return await ctx.send("You cannot perform this action on this user due to role hierarchy.")

    if not os.path.exists(f'data/warns/{ctx.guild.id}.json'):
        embed = discord.Embed(
            title="User Warnings",
            description="This server has no warns to view.",
            color=discord.Color.blue()
        )
        message = await ctx.send(embed=embed)
        await message.delete(delay=5)
        return
    
    with open(f'data/warns/{ctx.guild.id}.json', 'r') as f:
        warns = json.load(f)
    
    if str(member.id) not in warns or warns[str(member.id)] == 0:
        embed = discord.Embed(
            title="User Warnings",
            description=f"{member} has no warns.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        return
    
    embed = discord.Embed(
        title="User Warnings",
        description=f'{member} has {warns[str(member.id)]} warn(s).',
        color=discord.Color.red()
    )
    await ctx.send(embed=embed)


@bot.command(name='clearwarns', aliases=['cw'], help="Removes all warns from a user.")
@commands.has_permissions(manage_roles=True)
@commands.cooldown(3, 15, commands.BucketType.channel)  
async def clearwarns(ctx, member: discord.Member = None):
    print("[@bot.command] Clearwarns was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass
    if not member:
        await ctx.send("Please specify a user to clear warns from.", delete_after=5)
        return
    me = ctx.guild.me
    if member.top_role >= me.top_role:
        return await ctx.send("I cannot perform this action on this user due to role hierarchy.")
    if member.top_role >= ctx.author.top_role:
        return await ctx.send("You cannot perform this action on this user due to role hierarchy.")

    if not os.path.exists(f'data/warns/{ctx.guild.id}.json'):
        await ctx.send("This server has no warns to clear.", delete_after=5)
        return
    
    with open(f'data/warns/{ctx.guild.id}.json', 'r') as f:
        warns = json.load(f)
    
    if str(member.id) not in warns or warns[str(member.id)] == 0:
        await ctx.send("This member has no warns to clear.", delete_after=5)
        return
    
    del warns[str(member.id)]
    
    with open(f'data/warns/{ctx.guild.id}.json', 'w') as f:
        json.dump(warns, f)
    
    await ctx.send(f'Cleared all warnings for **{member}**.', delete_after=5)
#------------------------

@bot.command(name='ban', help="Bans the specified user from the server.")
@commands.has_permissions(ban_members=True)
@commands.cooldown(3, 15, commands.BucketType.channel)  
async def ban(ctx, member: discord.Member = None, *, reason=None):
    print("[@bot.command] Ban was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass
    if not member:
        await ctx.send("Please specify a user to ban.")
        return
    me = ctx.guild.me
    if not me.guild_permissions.ban_members:
        return await ctx.send("I do not have the necessary permissions to ban members.")
    if member == ctx.author:
        return await ctx.send("You cannot ban yourself!")
    if member.top_role >= me.top_role:
        return await ctx.send("I cannot perform this action on this user due to role hierarchy.")
    if member.top_role >= ctx.author.top_role:
        return await ctx.send("You cannot perform this action on this user due to role hierarchy.")

    await member.ban(reason=reason)
    await ctx.send(f'**{member}** has been banned.')
    if reason:
        await member.send(f"You have been banned from **{ctx.guild.name}** for *{reason}*.")
    else:
        await member.send(f"You have been banned from **{ctx.guild.name}**.")


@bot.command(name='unban', help="Unbans the specified user from the server.")
@commands.has_permissions(ban_members=True)
@commands.cooldown(3, 15, commands.BucketType.channel)  
async def unban(ctx, *, user: discord.User = None):
    print("[@bot.command] Unban was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass
    if not user:
        await ctx.send("Please specify a user to unban.", delete_after=5)
        return
    me = ctx.guild.me
    if not me.guild_permissions.ban_members:
        return await ctx.send("I do not have the necessary permissions to unban members. (Ban Members)")

    try:
        await ctx.guild.unban(user)
        await ctx.send(f'**{user}** has been unbanned.', delete_after=5)
    except discord.errors.NotFound:
        await ctx.send(f'**{user}** is not banned in this guild.', delete_after=5)
#------------------------

@bot.command(name='kick', aliases=['k'], help="Kicks the specified user from the server.")
@commands.has_permissions(kick_members=True)
@commands.cooldown(3, 15, commands.BucketType.channel)  
async def kick(ctx, member: discord.Member = None, *, reason=None):
    print("[@bot.command] Kick was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass
    if not member:
        await ctx.send("Please specify a user to kick", delete_after=5)
        return
    me = ctx.guild.me
    if not me.guild_permissions.kick_members:
        return await ctx.send("I do not have the permission to kick members.")
    if member == ctx.author:
        return await ctx.send("You cannot kick yourself!")
    if member.top_role >= me.top_role:
        return await ctx.send("I cannot kick members with the same or higher role than mine.")
    if member.top_role >= ctx.author.top_role:
        return await ctx.send("You cannot perform this action on this user due to role hierarchy.")
    
    await member.kick(reason=reason)
    await ctx.send(f'**{member}** has been kicked from the server.')
    if reason:
        await member.send(f"You have been Kicked from **{ctx.guild.name}** for *{reason}*.")
    else:
        await member.send(f"You have been Kicked from **{ctx.guild.name}**.")
#------------------------

@bot.command(name='mute', aliases=['m'], help="Mutes the specified user for a specified amount of time. (Default: 1 hour)")
@commands.has_permissions(manage_messages=True)
@commands.cooldown(3, 15, commands.BucketType.channel)  
async def mute(ctx, member: discord.Member = None, duration: str = None, *, reason=None):
    print("[@bot.command] Mute was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass
    if not member:
        await ctx.send("Please specify a user to mute.", delete_after=5)
        return
    me = ctx.guild.me
    if not me.guild_permissions.manage_roles:
        return await ctx.send("I do not have the necessary permissions to mute members. (Manage Roles)")
    if member == ctx.author:
        return await ctx.send("You cannot mute yourself!")
    if member.top_role >= ctx.author.top_role:
        return await ctx.send("You cannot perform this action on this user due to role hierarchy.")
    if member.bot:
        return await ctx.send("I'm unable to mute a bot.")
    
    mute_role = discord.utils.get(ctx.guild.roles, name='Muted')

    if mute_role is None:
        mute_role = await ctx.guild.create_role(name='Muted', permissions=discord.Permissions.none())
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, send_messages=False)

    if mute_role in member.roles:
        await ctx.send(f'**{member}** is already muted.', delete_after=5)
        return

    if duration is None:
        await ctx.send('No duration specified. Please specify a duration, such as "1 hour" or "3 days".', delete_after=7)
        return
    
    duration_regex = re.compile(r'(?P<value>\d+)\s*(?P<unit>\w+)?')
    match = duration_regex.match(duration)
    if not match:
        await ctx.send('Invalid duration specified. Please specify a duration, such as "1 hour" or "3 days".', delete_after=7)
        return
    
    value = int(match.group('value'))
    unit = match.group('unit')
    
    if unit:
        if unit[0] in ('s', 'S'):
            pass
        elif unit[0] in ('m', 'M'):
            value *= 60
        elif unit[0] in ('h', 'H'):
            value *= 3600
        elif unit[0] in ('d', 'D'):
            value *= 86400
        else:
            await ctx.send('Invalid duration specified. Please use a valid duration, such as "1 hour" or "3 days".')
            return
    else:
        value *= 86400
    
    await member.add_roles(mute_role)
    if reason:
        await ctx.send(f'**{member}** has been muted for **{duration}**. Reason: *{reason}*')
    else:
        await ctx.send(f'**{member}** has been muted for **{duration}**.')
    
    await asyncio.sleep(value)
    
    await member.remove_roles(mute_role)
    await ctx.send(f'**{member}** has been unmuted.', delete_after=5)


@bot.command(name='unmute', aliases=['um'], help="Unmutes the specified user.")
@commands.has_permissions(manage_roles=True)
@commands.cooldown(3, 15, commands.BucketType.channel)  
async def unmute(ctx, member: discord.Member = None):
    print("[@bot.command] Unmute was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass
    if not member:
        await ctx.send("Please specify a user to unmute.")
        return
    me = ctx.guild.me
    if not me.guild_permissions.manage_roles:
        return await ctx.send("I do not have the necessary permissions to unmute members. (Manage Roles)")
    if member.top_role >= ctx.author.top_role:
        return await ctx.send("You cannot perform this action on this user due to role hierarchy.")

    mute_role = discord.utils.get(ctx.guild.roles, name='Muted')

    if mute_role not in member.roles:
        await ctx.send(f'**{member}** is not muted.', delete_after=5)
        return
    
    await member.remove_roles(mute_role)
    await ctx.send(f'**{member}** has been unmuted.', delete_after=5)
#------------------------

@bot.command(name='filesay', aliases=['fs'])
@commands.is_owner()
async def filesay(ctx, file_name: str):
    print("[@bot.command] Filesay was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass
    try:
        with open(file_name, 'r') as f:
            file_contents = f.read()
    except FileNotFoundError:
        await ctx.send('The specified file was not found.')
        return

    await ctx.send(file_contents)
#------------------------

@bot.command(name='avatar', aliases=['av'], help="Displays the specified user's Avatar in chat.")
@commands.cooldown(3, 25, commands.BucketType.channel)  
async def avatar(ctx, *, user: discord.Member = None):
    print("[@bot.command] Avatar was executed")
    try:
        await ctx.message.delete()
    except discord.Forbidden as e:
        pass
    
    if user is None:
        user = ctx.author
    avatar_url = user.avatar_url
    await ctx.send(avatar_url)
#------------------------

@bot.event
@commands.cooldown(2, 30, commands.BucketType.channel)  
async def on_ready():
    print("Bot Started")
    botactivity = discord.Activity(type=discord.ActivityType.playing, name="Welcome to Paradise")
    await bot.change_presence(activity=botactivity, status=discord.Status.do_not_disturb)
    print("RPC Connected")
    print("")
#------------------------

@bot.event
async def on_raw_reaction_add(event):
    with open('data/configs/verification.json', 'r') as f:
        data = json.load(f)
    guild = bot.get_guild(event.guild_id)
    if str(guild.id) not in data:
        return 
    if event.message_id != data[str(guild.id)]["verification_message"]:
        return
    verification_role = guild.get_role(data[str(guild.id)]["verification_role"])
    member = guild.get_member(event.user_id)
    await member.add_roles(verification_role)


@bot.command(name='setverify', aliases=['setverification'], help="Use this command to configure the Verification Channel and Message for your server.")
@commands.cooldown(2, 20, commands.BucketType.channel)
@commands.has_permissions(manage_roles=True)
async def setverification(ctx, channel: discord.TextChannel, role: discord.Role, *, message: str):
    print("[@bot.command] Setverify was executed")

    me = ctx.guild.me
    if not me.guild_permissions.manage_roles:
        return await ctx.send("I do not have the necessary permissions to verify members. (Manage Roles)")
    if not ctx.author.guild_permissions.manage_guild:
        await ctx.send('You cannot perform this action due to missing permissions. (Manage Server)', delete_after=5)
        return

    message = await channel.send(message)

    await message.add_reaction('✅')

    with open('data/configs/verification.json', 'r') as f:
        data = json.load(f)
    data[str(ctx.guild.id)] = {
        'verification_channel': channel.id,
        'verification_role': role.id,
        'verification_message': message.id
    }
    with open('data/configs/verification.json', 'w') as f:
        json.dump(data, f)

    await ctx.send('Verification channel, role, and message have been set.', delete_after=5)
#-----------------------

@bot.command(name='setwelcome', aliases=['cfgwelcome'], help="Use this command to configure the Welcome Channel and Message of your server.")
@commands.cooldown(1, 20, commands.BucketType.guild)
@commands.has_permissions(manage_channels=True)
async def setwelcomemessage(ctx, channel: discord.TextChannel = None, *, message):
    print("[@bot.command] Setwelcomemessage was executed")

    if not ctx.author.guild_permissions.manage_guild:
        await ctx.send('You cannot perform this action due to missing permissions. (Manage Server)', delete_after=5)
        return
    if channel is None:
        await ctx.send('Please specify a welcome channel. Syntax: =setwelcome #channel <message>', delete_after=5)
        return

    server_id = str(ctx.guild.id)
    config[server_id] = message

    welcome_channel_id = str(channel.id)
    config[f'{server_id}_channel'] = welcome_channel_id

    with open('data/configs/welcome_messages.json', 'w') as f:
        json.dump(config, f)

    await ctx.send(f'Welcome message for this server has been set to: {message} (sent to {channel.mention})')


with open('data/configs/welcome_messages.json', 'r') as f:
    config = json.load(f)
#-----------------------

@bot.command(name="agecheck", help="Turns `Account Age Checker` On or Off. Syntax: =agechecker on/off",)
@commands.cooldown(1, 20, commands.BucketType.guild)
@commands.has_permissions(manage_guild=True)
async def agecheck(ctx, option=None):
    print("[@bot.command] agecheck was executed")
    
    if option is None:
        await ctx.send("Please specify an option (`on`, `off`, or `status`).")
        return
    me = ctx.guild.me
    if not me.guild_permissions.manage_roles:
        return await ctx.send("I do not have the necessary permissions to kick members.")
    if not ctx.author.guild_permissions.manage_guild:
        await ctx.send('You cannot perform this action due to missing permissions. (Manage Server)', delete_after=5)
        return

    server_id = str(ctx.guild.id)
    with open("data/configs/agecheck.json", "r") as f:
        config = json.load(f)
    if server_id not in config:
        config[server_id] = {"enabled": False}
    current_state = config[server_id]["enabled"]
    
    if option in ["on", "enable"]:
        if current_state:
            await ctx.send("Account Age Checker is already enabled.")
        else:
            config[server_id]["enabled"] = True
            await ctx.send("Account Age Checker has been enabled.")
    elif option in ["off", "disable"]:
        if not current_state:
            await ctx.send("Account Age Checker is already disabled.")
        else:
            config[server_id]["enabled"] = False
            await ctx.send("Account Age Checker has been disabled.")
    elif option in ["status", "show"]:
        if current_state:
            await ctx.send("Account Age Checker is currently **enabled**.")
        else:
            await ctx.send("Account Age Checker is currently **disabled**.")
    else:
        await ctx.send("Invalid option. Please use `on` or `off`.")
    with open("data/configs/agecheck.json", "w") as f:
        json.dump(config, f)
#-----------------------

@bot.event
async def on_member_join(member):
    server_id = str(member.guild.id)

    with open("data/configs/welcome_messages.json", "r") as f:
        config = json.load(f)
    welcome_message = config.get(server_id, "Welcome to the server!")
    welcome_channel_id = config.get(f"{server_id}_channel")

    with open("data/configs/agecheck.json", "r") as f:
        config = json.load(f)
    if server_id in config and config[server_id]["enabled"]:
        acc_age = (datetime.datetime.now() - member.created_at).days
        if acc_age < 7:
            try:
                if acc_age <= 1:
                    await member.send(f"You have been automatically kicked from **{member.guild.name}** due to your account being too young. (Current account age: {acc_age} day)")
                else:
                    await member.send(f"You have been automatically kicked from **{member.guild.name}** due to your account being too young. (Current account age: {acc_age} days)")
            except discord.Forbidden:
                pass
            await member.kick(reason="Auto Kick | Account too young.")
            return

    if welcome_channel_id is None:
        return
    channel = member.guild.get_channel(int(welcome_channel_id))
    await channel.send(f"{member.mention} {welcome_message}")
#-----------------------

async def check_invite(message):
    invite_pattern = re.compile("(.gg\/.+)")
    match = invite_pattern.search(message.content)

    if match:
        author_highest_role = message.author.roles[-1]
        bot_highest_role = message.guild.me.roles[-1]
        if author_highest_role >= bot_highest_role:
            return

        with open("data/configs/invfilter.json", "r") as config_file:
            config = json.load(config_file)

        server_id = str(message.guild.id)
        if server_id not in config or not config[server_id]["enabled"]:
            return

        try:
            await message.delete()
            if isinstance(message.channel, discord.TextChannel):
                await message.channel.send(f"{message.author.mention} Your message was removed for potentially containing a discord invite.")
        except (discord.errors.NotFound, discord.errors.Forbidden):
            pass


@bot.command(name="invfilter", aliases=["invitefilter"], help="Turns `Invite Filter` On or Off. Syntax: =invfilter on/off")
@commands.cooldown(1, 20, commands.BucketType.guild)
@commands.has_permissions(manage_guild=True)
async def invfilter(ctx, option=None):
    print("[@bot.command] invfilter was executed")
    
    if option is None:
        await ctx.send("Please specify an option (`on`, `off`, or `status`).")
        return
    me = ctx.guild.me
    if not me.guild_permissions.manage_roles:
        return await ctx.send("I do not have the necessary permissions to delete messages. (Manage Messages)")
    if not ctx.author.guild_permissions.manage_guild:
        await ctx.send('You cannot perform this action due to missing permissions. (Manage Server)', delete_after=5)
        return
    
    server_id = str(ctx.guild.id)
    with open("data/configs/invfilter.json", "r") as f:
        config = json.load(f)
    if server_id not in config:
        config[server_id] = {"enabled": False}
    current_state = config[server_id]["enabled"]
    
    if option in ["on", "enable"]:
        if current_state:
            await ctx.send("Invite Filter is already enabled.")
        else:
            config[server_id]["enabled"] = True
            await ctx.send("Invite Filter has been enabled.")
    elif option in ["off", "disable"]:
        if not current_state:
            await ctx.send("Invite Filter is already disabled.")
        else:
            config[server_id]["enabled"] = False
            await ctx.send("Invite Filter has been disabled.")
    elif option in ["status", "show"]:
        if current_state:
            await ctx.send("Invite Filter is currently **enabled**.")
        else:
            await ctx.send("Invite Filter is currently **disabled**.")
    else:
        await ctx.send("Invalid option. Please use `on`, `off`, or `status`.")
    with open("data/configs/invfilter.json", "w") as f:
        json.dump(config, f)


@bot.event
async def on_message(message):
    await check_invite(message)
    await bot.process_commands(message)
#------------------------

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown) and not isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()
        await ctx.send(f'You are being rate limited. Please try again in {error.retry_after:.1f} seconds.', delete_after=5)

bot.run('YOUR_TOKEN_HERE')
