import asyncio
import time
import discord
from discord.ext import commands
import youtube_dl
import os
import string
import secrets

"""
Code by github.com/NiklasWyld

NiklasWyld/ImmerzockBot is licensed under the

GNU General Public License v3.0

✅ Commercial use
✅ Modification
✅ Distribution
✅ Patent use
✅ Private use
----------------------
❌ Liability
❌ Warranty

Immerzock Bot is based on the Discord Libery 'discord.py'.
"""

intents = discord.Intents.all()
# Create a client with commands.Bot with parameters command_prefix, intents, help_command
client = commands.Bot(command_prefix='$', intents=intents, help_command=None)

# Method 'is_not_pinned' to return a true or false bool. For use in '$clear' command

def is_not_pinned(mess):
    return not mess.pinned

# Music Bot

# Play command with use of youtube_dl

@client.command()
async def play(ctx, url: str):
    # Check if ctx.author is on a voice channel
    if not ctx.author.voice:
        await ctx.author.send('You must be in a voice channel for this command!')
        return
    # File management
    if os.path.isfile('song.mp3'):
        try:
            os.remove('song.mp3')
        except PermissionError:
            await ctx.author.send('Wait for the already playing song to end!')
            return
    
    # Connect to channel
    voice_channel = ctx.author.voice.channel
    voice = ctx.channel.guild.voice_client
    if voice is None:
        voice = await voice_channel.connect()
    elif voice.channel != voice_channel:
        voice = await voice.move_to(voice_channel)
    
    # Download .mp3 file
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    [os.rename(file, 'song.mp3') for file in os.listdir('.') if file.endswith('.mp3')]
    if voice.is_playing:
        voice.stop()
    # Play the file
    voice.play(discord.FFmpegPCMAudio('song.mp3'))

# Join command    
    
@client.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.author.send('You are in no voice channel!')
        return
    voice_channel = ctx.author.voice.channel
    await voice_channel.connect()
    
# Leave command
    
@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.author.send('The bot is not in any channel!')

# Pause command        
        
@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.author.send('There is no music playing at the moment!')

# Resume command        
        
@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.author.send('No music was paused!')

# Stop command        
        
@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

# Commands

# Help Command with all features and methods
# Attention, many commands have been removed

@client.command()
async def help(ctx, member: discord.Member = None):
    embed = discord.Embed(title='Help menu', description='Help menu of Immerzock-Bot', color=0x00ff00)
    embed.add_field(name='Test', value='$test - Test the bot', inline=False)
    embed.set_thumbnail(
        url='url of any image')
    mess = await ctx.channel.send(embed=embed)
    await mess.add_reaction('👍')

# Create random code with secrets and string package

@client.command()
async def code(ctx):
    y = string.digits + string.ascii_uppercase
    x = int(ctx.message.content.split(' ')[1])
    await ctx.send(''.join(secrets.choice(y) for i in range(x)))

# Sends the current time    

@client.command()
async def time(ctx, amount: int = 1):
    for i in range(amount):
        await ctx.channel.send(time.strftime('%H: %M: %S'))

# Sends the current date

@client.command()
async def date(ctx):
    await ctx.channel.send(time.strftime('%d. %m. %y'))

# Components of owner 'NiklasWyld / niklaspeter123'

@client.command()
async def components(ctx, member: discord.Member = None):
    # Command disabled
    await ctx.send('Command disabled')

# Join-Message on 'on_member_join' event

@client.event
async def on_member_join(member):
    await member.send(f'Welcome to **{member.guild}**!')

# Another commands

@client.command()
async def whosonline(ctx):
    # Command is not online resp. not developed
    await ctx.channel.send(
        f'This command is currently unavailable. Try again later {ctx.author.mention}'
    )

# Creates an invite link to invite the bot to a Discord server.    

@client.command()
async def invite(ctx):
    await ctx.channel.send(
        f'https://discordapp.com/oauth2/authorize?&client_id=' + client.user.id + '&scope=bot&permissions=0'
    )

# Outputs the servers on which the bot is

@client.command()
@commands.is_owner()
async def server(ctx):
    embed = discord.Embed(title='Servers')
    for guild in client.guilds:
        await embed.add_field(name='A nice server', value=guild)

# Kick Command

@commands.has_permissions(kick_members=True)
@client.command()
async def kick(ctx, user: discord.Member, *, reason='No reason'):
    await user.kick(reason=reason)
    print(f'{ctx.author} has kicked {user.name}!')
    kick = discord.Embed(title=f':boot: Kicked {user.name}!', description=f'Reason: {reason}\nBy: {ctx.author.mention}')
    await ctx.message.delete()
    await ctx.channel.send(embed=kick)
    await user.send(embed=kick)

# Ban Command

@commands.has_permissions(ban_members=True)
@client.command()
async def ban(ctx, user: discord.Member, *, reason='Keine Reason'):
    await user.ban(reason=reason)
    print(f'{ctx.author} has banned {user.name}!')
    ban = discord.Embed(title=f':boot: Banned {user.name}!', description=f'Reason: {reason}\nBy: {ctx.author.mention}')
    await ctx.message.delete()
    await ctx.channel.send(embed=ban)
    await user.send(embed=ban)

# Command to test the bot

@client.command()
async def test(ctx):
    await ctx.channel.send('Test successful!')

# Sends the user name of the ctx.author

@client.command()
async def username(ctx):
    await ctx.channel.send(str(ctx.author))

# Say command with arg 'message' as string

@client.command()
async def say(ctx, *, message: str = None):
    if message is not None:
        embed = discord.Embed(title=f'{ctx.author.name}`s message', color=0x010101)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name='Message:', value=message)
        await ctx.channel.send(embed=embed)

    else:
        await ctx.message.delete()
        await ctx.channel.send(f'> {ctx.author.mention} please enter a valid message!')

# Open Source Command with link to this repo

@client.command()
async def opensource(ctx):
    await ctx.channel.send('Open Source (GitHub): https://github.com/NiklasWyld/ImmerzockBot')

# Contact Command with email by questions or bugs

@client.command()
async def email(ctx):
    await ctx.channel.send('You can send me questions and concerns to this email:\r\n'
                           'immerzock.management@gmail.com\r\n'
                           '**SPAM WILL BE BLOCKED**')

# Get id of bot and send it

@client.command()
async def getid(ctx):
    await ctx.channel.send(f'Heres the id of me: {client.user.id}')

# Part of verify command (only owner / one use)

@client.command()
@commands.is_owner()
async def botverify(ctx):
    await ctx.channel.send(
        'Enter **$verification** in the chat and follow the instructions below to get access to the server!'
    )

# Gamemode
# Removes gamemode command

@client.command()
async def gamemode(ctx, *, gm):
    if not gm:
        await ctx.send('Which game mode do you want? **1** - **0**')
    elif gm == '1':
        await ctx.send('Gamemode was successfully changed to 1!')
    elif gm == '0'
        await ctx.send('Gamemode was successfully changed to 0!')

# Commands with discord.Embed

@client.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member if member else ctx.author
    embed = discord.Embed(title=f'Userinfo for {member.display_name}',
                          description=f'This is a user info for the member {member.mention}',
                          color=0x22a7f0)
    embed.add_field(name='Server joined', value=member.joined_at.strftime('%d/%m/%Y, %H:%M:%S'),
                    inline=True)
    embed.add_field(name='Discord joined', value=member.created_at.strftime('%d/%m/%Y, %H:%M:%S'),
                    inline=True)
    rollen = ''
    for role in member.roles:
        if not role.is_default():
            rollen += '{} \r\n'.format(role.mention)
    if rollen:
        embed.add_field(name='Roles', value=rollen, inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text='Thats an great userinfo')
    mess = await ctx.channel.send(embed=embed)
    await mess.add_reaction('👌')

# Clear command

@client.command()
async def clear(ctx):
    embed = discord.Embed(title=f'{str(limit)} Messages were deleted by {ctx.author}!', colour=discord.Colour.magenta())
    if not ctx.author.permissions_in(ctx.channel).manage_messages:
        await ctx.respond(embed=self.no_perms, delete_after=10)
    elif ctx.author.permissions_in(ctx.channel).manage_messages:
        await ctx.channel.purge(limit=limit, before=msg)
        await ctx.respond(embed=embed, delete_after=5)

# Shutdown

@client.command()
@commands.is_owner()
async def shutdown(ctx):
    print('Bot will shutdown')
    await client.close()

# On Ready method

@client.event
async def on_ready():
    print(f'Status: Online as {client.user}!')
    client.loop.create_task(status_task())

# status_task() method to change status every 10 seconds
    
async def status_task():
    while True:
        await client.change_presence(activity=discord.Game('Immerzock Bot'), status=discord.Status.online)
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Game('$help'), status=discord.Status.online)
        await asyncio.sleep(10)

# Start Bot (client) 
# 'TOKEN' is only a example and not defined

client.run(TOKEN)
