import discord
import asyncio
import datetime
import os
import json
import re
import time
from discord.ext import commands


bot = commands.Bot(command_prefix=['=', '?', '.'], intents=discord.Intents.all(), case_insensitive=True)
#------------------------

@bot.command(name='purge', aliases=['clear'], help="Deletes a specified ammount of messages on a channel. (max: 100)")
@commands.has_permissions(manage_messages=True)
@commands.cooldown(3, 25, commands.BucketType.channel)  
async def purge(ctx, amount: int):
    print("[@bot.command] Purge was executed")
    await ctx.message.delete()

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

@bot.command(name='invite', aliases=['inv', 'authurl'], help="Displays the bot's OAuth URL (all perms)")
@commands.cooldown(3, 20, commands.BucketType.channel)  
async def invite(ctx):
    print("[@bot.command] Invite was executed")
    await ctx.message.delete()
    auth_url = discord.utils.oauth_url(bot.user.id, permissions=discord.Permissions.all())
    await ctx.send(f'My OAuth URL:\n> {auth_url}')
#------------------------

@bot.command(name='support', aliases=['home'], help="Invite to the Bot's Support Server.")
@commands.cooldown(3, 20, commands.BucketType.channel)  
async def support(ctx):
    print("[@bot.command] Support was executed")
    await ctx.message.delete()
    invite_url = f'https://discord.gg/kWvj4JsWbW'
    await ctx.send(f'Need help? Join our support server: {invite_url}')
#------------------------

@bot.command(name='source', help="Gives out the github repo of the bot.")
@commands.cooldown(3, 20, commands.BucketType.channel)  
async def support(ctx):
    print("[@bot.command] Source was executed")
    await ctx.message.delete()
    repourl = f'https://github.com/AWeirDKiD/ParadiseBot'
    await ctx.send(f'Yes! I am open source: {repourl}')
#------------------------

@bot.command(name="echo", help="Repeats whatever the user says.")
@commands.cooldown(3, 15, commands.BucketType.channel)  
async def echo(ctx, *, message: str):
    print("[@bot.command] Echo was executed")
    await ctx.message.delete()
    await ctx.send(message)
#------------------------

start_time = time.time()
def uptime():
  current_time = time.time()
  uptime = current_time - start_time
  start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
  current_time_str = datetime.datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
  uptime_str = "**Uptime:** " + str(int(uptime // 86400)) + " days, " + str(int(uptime % 86400 // 3600)) + " hours, " + str(int(uptime % 3600 // 60)) + " minutes, " + str(int(uptime % 60)) + " seconds" + "\n\n**Start Date:** " + start_time_str + "\n**Current Date:** " + current_time_str
  return uptime_str
  
@bot.command(name='uptime', aliases=['awaketime'], help="Displays the bot's current uptime and start date.")
@commands.cooldown(2, 30, commands.BucketType.channel)
async def appuptime(ctx):
  print("[@bot.command] Uptime was executed")
  await ctx.message.delete()
  await ctx.send(uptime())
#----------------------

@bot.command(name="nuke", aliases=["nukechannel"], help="Nukes the channel the command was executed on (acts as a cleanup tool)")
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1, 20, commands.BucketType.channel)  
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

@bot.command(name='warn', aliases=['w'], help="Warns a user (Used for moderation).")
@commands.has_permissions(manage_roles=True)
@commands.cooldown(3, 15, commands.BucketType.channel)  
async def warn(ctx, member: discord.Member, *, reason=None):
    print("[@bot.command] Warn was executed")
    await ctx.message.delete()
    if not os.path.exists(f'data/warns/{ctx.guild.id}.json'):
        with open(f'data/warns/{ctx.guild.id}.json', 'w') as f:
            json.dump({}, f)
    
    with open(f'data/warns/{ctx.guild.id}.json', 'r') as f:
        warns = json.load(f)
    
    warns[str(member.id)] = warns.get(str(member.id), 0) + 1
    
    with open(f'data/warns/{ctx.guild.id}.json', 'w') as f:
        json.dump(warns, f)
    
    if warns[str(member.id)] >= 10:
        await member.ban(reason=f'Reached the maximum number of warns ({10})')
        await ctx.send(f'**{member}** has been banned for reaching the maximum number of warns ({10})')
    else:
        if reason:
            await ctx.send(f'**{member}** has been warned. They now have {warns[str(member.id)]} warnings. Reason: {reason}')
        else:
            await ctx.send(f'**{member}** has been warned. They now have {warns[str(member.id)]} warnings.')


@bot.command(name='removewarn', aliases=['rw'], help="Removes a specified ammount of warns from a User.")
@commands.has_permissions(manage_roles=True)
@commands.cooldown(3, 15, commands.BucketType.channel)  
async def removewarn(ctx, member: discord.Member, number: int):
    print("[@bot.command] Removewarn was executed")
    await ctx.message.delete()
    if not os.path.exists(f'data/warns/{ctx.guild.id}.json'):
        await ctx.send("This server has no warns to remove.", delete_after=5)
        return
    
    with open(f'data/warns/{ctx.guild.id}.json', 'r') as f:
        warns = json.load(f)
    
    if str(member.id) not in warns:
        await ctx.send("This member has no warns to remove.", delete_after=5)
        return
    
    warns[str(member.id)] = max(0, warns[str(member.id)] - number)

    with open(f'data/warns/{ctx.guild.id}.json', 'w') as f:
        json.dump(warns, f)
    
    await ctx.send(f'Removed {number} warnings for **{member}**. They now have {warns[str(member.id)]} warns.', delete_after=5)


@bot.command(name='viewwarns', aliases=['vw', 'warns'], help="Disaplays the specified user's total Warns.")
@commands.has_permissions(manage_roles=True)
@commands.cooldown(3, 20, commands.BucketType.channel)  
async def viewwarns(ctx, member: discord.Member):
    print("[@bot.command] Viewwarns was executed")
    await ctx.message.delete()
    if not os.path.exists(f'data/warns/{ctx.guild.id}.json'):
        await ctx.send("This server has no warns to view.", delete_after=5)
        return
    
    with open(f'data/warns/{ctx.guild.id}.json', 'r') as f:
        warns = json.load(f)
    
    if str(member.id) not in warns:
        await ctx.send("This member has no warns.", delete_after=5)
        return
    
    await ctx.send(f'**User Warnings:**\n> {member} has {warns[str(member.id)]} warns.')


@bot.command(name='clearwarns', aliases=['cw'], help="Removes ALL warns from a user.")
@commands.has_permissions(manage_roles=True)
@commands.cooldown(2, 15, commands.BucketType.channel)  
async def clearwarns(ctx, member: discord.Member):
    print("[@bot.command] Clearwarns was executed")
    await ctx.message.delete()
    if not os.path.exists(f'data/warns/{ctx.guild.id}.json'):
        await ctx.send("This server has no warns to clear.", delete_after=5)
        return
    
    with open(f'data/warns/{ctx.guild.id}.json', 'r') as f:
        warns = json.load(f)
    
    if str(member.id) not in warns:
        await ctx.send("This member has no warns to clear.", delete_after=5)
        return
    
    del warns[str(member.id)]
    
    with open(f'data/warns/{ctx.guild.id}.json', 'w') as f:
        json.dump(warns, f)
    
    await ctx.send(f'Cleared all warnings for **{member}**.', delete_after=5)
#------------------------

@bot.command(name='ban', aliases=['b'], help="Bans the specified user from the server.")
@commands.has_permissions(ban_members=True)
@commands.cooldown(3, 15, commands.BucketType.channel)  
async def ban(ctx, member: discord.Member, *, reason=None):
    print("[@bot.command] Ban was executed")
    await ctx.message.delete()
    await member.ban(reason=reason)
    await ctx.send(f'**{member}** has been banned.')

@bot.command(name='unban', help="Unbans the specified user from the server.")
@commands.has_permissions(ban_members=True)
@commands.cooldown(3, 15, commands.BucketType.channel)  
async def unban(ctx, *, user: discord.User):
    print("[@bot.command] Unban was executed")
    await ctx.message.delete()
    try:
        await ctx.guild.unban(user)
        await ctx.send(f'**{user}** has been unbanned.', delete_after=5)
    except discord.errors.NotFound:
        await ctx.send(f'**{user}** is not banned in this guild.', delete_after=5)
#------------------------

@bot.command(name='kick', aliases=['k'], help="Kicks the specified user from the server.")
@commands.has_permissions(kick_members=True)
@commands.cooldown(3, 15, commands.BucketType.channel)  
async def kick(ctx, member: discord.Member, *, reason=None):
    print("[@bot.command] Kick was executed")
    await ctx.message.delete()
    await member.kick(reason=reason)
    await ctx.send(f'**{member}** has been kicked from the server.')
#------------------------

@bot.command(name='mute', aliases=['m'], help="Mutes the specified user for a specified amount of time. (Default: 1 hour)")
@commands.has_permissions(manage_messages=True)
@commands.cooldown(3, 15, commands.BucketType.channel)  
async def mute(ctx, member: discord.Member, duration: str = None, *, reason=None):
    print("[@bot.command] Mute was executed")
    await ctx.message.delete()

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
        await ctx.send(f'**{member}** has been muted for **{duration}**. Reason: {reason}', delete_after=10)
    else:
        await ctx.send(f'**{member}** has been muted for **{duration}**.', delete_after=5)
    
    await asyncio.sleep(value)
    
    await member.remove_roles(mute_role)
    await ctx.send(f'**{member}** has been unmuted.', delete_after=5)


@bot.command(name='unmute', aliases=['um'], help="Unmutes the specified user.")
@commands.has_permissions(manage_roles=True)
@commands.cooldown(3, 15, commands.BucketType.channel)  
async def unmute(ctx, member: discord.Member):
    print("[@bot.command] Unmute was executed")
    await ctx.message.delete()

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
    await ctx.message.delete()
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
    await ctx.message.delete()
    print("[@bot.command] Avatar was executed")
    
    if user is None:
        user = ctx.author
    avatar_url = user.avatar
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
async def setverification(ctx, channel: discord.TextChannel, role: discord.Role, *, message: str):
    if not ctx.author.guild_permissions.manage_guild:
        await ctx.send('You do not have the "Manage Server" permission.', delete_after=5)
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
async def setwelcomemessage(ctx, channel: discord.TextChannel = None, *, message):
    await ctx.message.delete()
    print("[@bot.command] Setwelcomemessage was executed")

    if channel is None:
        await ctx.send('Please specify a welcome channel. Syntax: =setwelcome #channel-name message', delete_after=5)
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

@bot.event
async def on_member_join(member):
    server_id = str(member.guild.id)
    welcome_message = config.get(server_id, 'Welcome to the server!')
    welcome_channel_id = config.get(f'{server_id}_channel')

    if welcome_channel_id is None:
        return

    channel = member.guild.get_channel(int(welcome_channel_id))

    await channel.send(f'{member.mention} {welcome_message}')
#------------------------

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown) and not isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()
        await ctx.send(f'You are being rate limited. Please try again in {error.retry_after:.1f} seconds.', delete_after=5)

bot.run('YOUR_TOKEN_HERE')
