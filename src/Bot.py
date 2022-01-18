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

The complete code is written in German. Also how the Discord Bot is based on German.

Comments are in English though

Immerzock Bot is based on the Discord Libery 'discord.py'.
"""

intents = discord.Intents.all()
client = commands.Bot(command_prefix='$', intents=intents)
client.remove_command('help')
client.remove_command('game:')

# Method 'is_not_pinned' to return a true or false bool. For use in '$clear' command

def is_not_pinned(mess):
    return not mess.pinned

# Music Bot

@client.command()
async def play(ctx, url: str):
    if not ctx.author.voice:
        await ctx.author.send('Du musst in einen Sprach-Kanal für diesen Befehl sein!')
        return
    if os.path.isfile('song.mp3'):
        try:
            os.remove('song.mp3')
        except PermissionError:
            await ctx.author.send('Warte bis der bereits spielende Song endet!')
            return

    voice_channel = ctx.author.voice.channel
    voice = ctx.channel.guild.voice_client
    if voice is None:
        voice = await voice_channel.connect()
    elif voice.channel != voice_channel:
        voice = await voice.move_to(voice_channel)

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
    voice.play(discord.FFmpegPCMAudio('song.mp3'))

@client.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.author.send('Du bist in keinen Sprach-Kanal!')
        return
    voice_channel = ctx.author.voice.channel
    await voice_channel.connect()
    await asyncio.sleep(300)
    await ctx.author.send('Du hast zu lange nicht mit den Bot interargiert! Deshalb habe ich den Channel verlassen!')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        return

@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.author.send('Der Bot ist in keinen Kanal!')

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.author.send('Zur Zeit spielt keine Musik!')

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.author.send('Es wurde keine Musik pausiert!')

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

# Commands

# Help Command with all features and methods

@client.command()
async def help(ctx, member: discord.Member = None):
    embed = discord.Embed(title='Hilfe-Menü', description='Help-Menu von Immerzock-Bot', color=0x00ff00)
    embed.add_field(name='Test', value='$test - Testet den Bot', inline=False)
    embed.add_field(name='Datum', value='$datum - Zeigt das Datum', inline=False)
    embed.add_field(name='Uhrzeit', value='$uhrzeit - Zeigt die Uhrzeit', inline=False)
    embed.add_field(name='Help', value='$help - Dieser Befehl', inline=False)
    embed.add_field(name='Komponenten', value='$komponenten - Zeigt Niklas`s Komponenten', inline=False)
    embed.add_field(name='Open-Source', value='$opensource - Zeigt Info zum Code des Bot´s', inline=False)
    embed.add_field(name='Username', value='$username - Zeigt deinen Username', inline=False)
    embed.add_field(name='User-Info', value='$userinfo (User) - Zeigt Userinfo', inline=False)
    embed.add_field(name='Clear', value='$clear (Zahl) - Löscht bestimmte Anzahl von Nachrichten **(ONLY ADMIN)**',
                    inline=False)
    embed.add_field(name='Email', value='$email - Zeigt eine Email-Adresse für Fragen', inline=False)
    embed.add_field(name='Kick', value='$kick (Username) - Kickt den User **(ONLY ADMIN)**', inline=False)
    embed.add_field(name='Ban', value='$ban (Username) - Bannt den User **(ONLY ADMIN)**', inline=False)
    embed.add_field(name='Say', value='$say (Nachricht) - Wiederholt deine Nachricht', inline=False)
    embed.add_field(name='Weristonline', value='$weristonline - Zeigt wer online ist', inline=False)
    embed.add_field(name='Gamemode', value='$gamemode (1 - 0) - Wechselt den Gamemode', inline=False)
    embed.add_field(name='MusikBot', value='**Zur Zeit ist der Musikbot außer Betrieb! Wir arbeiten mit hochtouren!**',
                    inline=False)
    embed.set_thumbnail(
        url='https://cdn.discordapp.com/attachments/806062613716271144/849881814738927646/d04bff1caa1c75d82fd3d4e827cafc74.png')
    mess = await ctx.channel.send(embed=embed)
    await mess.add_reaction('👍')
    print(str(ctx.author) + ' hat Help-Befehl ausgeführt')

# Game

# Disable error message of '$spiel' command on call 

@client.command()
async def spiel(ctx):
    return

# Game (end)

# Create random code with secrets and string package

@client.command()
async def code(ctx):
    y = string.digits + string.ascii_uppercase
    x = int(ctx.message.content.split(' ')[1])
    await ctx.send(''.join(secrets.choice(y) for i in range(x)))

# Show the current time    

@client.command()
async def uhrzeit(ctx):
    await ctx.channel.send(time.strftime('%H: %M: %S'))
    print(str(ctx.author) + 'hat Uhrzeit-Befehl ausgeführt')

# Show the current date

@client.command()
async def datum(ctx):
    await ctx.channel.send(time.strftime('%d. %m. %y'))
    print(str(ctx.author) + ' hat Datum-Befehl ausgeführt')

# Components of owner 'NiklasWyld / niklaspeter123'

@client.command()
async def komponenten(ctx, member: discord.Member = None):
    # Command disabled
    return await ctx.send('Error')

# Join-Message on 'on_member_join' event

@client.event
async def on_member_join(member):
    await member.send(f'Willkommen auf **{member.guild}**!')
    print(f'{member.name} ist auf {member.guild} gejoint')

# Another commands

@client.command()
async def weristonline(ctx):
    # Command is not online resp. not developed
    await ctx.channel.send(
        f'Dieser Befehl ist zur Zeit nicht verfügbar. Versuch es später nochmal {ctx.author.mention}'
    )

# Creates an invite link to invite the bot to a Discord server.    

@client.command()
async def invite(ctx):
    await ctx.channel.send(
        f'https://discordapp.com/oauth2/authorize?&client_id=' + client.user.id + '&scope=bot&permissions=0'
    )

# Outputs the servers on which the bot is for the owner 

@client.command()
@commands.is_owner()
async def server(ctx):
    for guild in client.guilds:
        print(str(guild.name))

# Kick Command

@commands.has_permissions(kick_members=True)
@client.command()
async def kick(ctx, user: discord.Member, *, reason='Keine Reason'):
    await user.kick(reason=reason)
    print(f'{ctx.author} hat {user.name} gekickt!')
    kick = discord.Embed(title=f':boot: Kicked {user.name}!', description=f'Reason: {reason}\nBy: {ctx.author.mention}')
    await ctx.message.delete()
    await ctx.channel.send(embed=kick)
    await user.send(embed=kick)

# Ban Command

@commands.has_permissions(ban_members=True)
@client.command()
async def ban(ctx, user: discord.Member, *, reason='Keine Reason'):
    await user.ban(reason=reason)
    print(f'{ctx.author} hat {user.name} gebannt!')
    ban = discord.Embed(title=f':boot: Banned {user.name}!', description=f'Reason: {reason}\nBy: {ctx.author.mention}')
    await ctx.message.delete()
    await ctx.channel.send(embed=ban)
    await user.send(embed=ban)

# Command to test the bot

@client.command()
async def test(ctx):
    await ctx.channel.send('Test erfolgreich!')
    print(str(ctx.author) + ' hat Test durchgeführt')

# Sends the user name of the ctx.author

@client.command()
async def username(ctx):
    await ctx.channel.send(str(ctx.author))
    print(str(ctx.author) + ' hat Username-Befehl ausgeführt')

# Say command with arg 'message' as string

@client.command()
async def say(ctx, *, message: str = None):
    if message is not None:
        await ctx.channel.send('Nachricht:', value=message)
        embed = discord.Embed(title=f'{ctx.author.name}`s message', color=0x010101)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name='Nachricht:', value=message)
        await ctx.message.delete()
        await ctx.channel.send(embed=embed)

    else:
        await ctx.message.delete()
        await ctx.channel.send(f'> {ctx.author.mention} bitte gib eine gültige Nachricht ein!')

# Open Source Command with link to this repo

@client.command()
async def opensource(ctx):
    await ctx.channel.send('Open Source (GitHub): https://github.com/NiklasWyld/ImmerzockBot')
    print(str(ctx.author) + ' hat Opensource-Befehl ausgeführt')

# Contact Command with email by questions or bugs

@client.command()
async def email(ctx):
    await ctx.channel.send('Unter dieser Email könnt ihr mir Fragen und Anliegen schreiben:\r\n'
                           'immerzock.management@gmail.com\r\n'
                           '**SPAM WIRD BLOCKIERT**')
    print(str(ctx.author) + ' hat Email-Befehl ausgeführt')

# Get id of bot for the owner

@client.command()
async def getid(ctx):
    await ctx.channel.send(f'{ctx.author.mention} das wird nur den Owner angezeigt', delete_after=5)
    print(f'ID: {client.user}')
    print(f'{ctx.author} hat GetID-Befehl ausgeführt')

# Part of verify command (only owner / one use)

@client.command()
@commands.is_owner()
async def botverify(ctx):
    await ctx.channel.send(
        'Gib **$Verifizierung** in den Chat ein, und befolge die folgenden Anweisungen um Zugriff auf den Server zu erhalten!'
    )

# Gamemode
# Removes gamemode command

@client.command()
async def gamemode(ctx, *, gm):
    if not gm:
        await csend.send('Welchen Gamemode willst du? **1** - **0**')
    elif gm == '1':
        await csend.send('Gamemode was successfully changed to 1!')
        print(str(message.author) + ' hat Gamemode-Befehl ausgeführt')
    elif gm == '0'
        await csend.send('Gamemode was successfully changed to 0!')
        print(str(message.author) + ' hat Gamemode-Befehl ausgeführt')

# Commands with discord.Embed

@client.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member if member else ctx.author
    embed = discord.Embed(title=f'Userinfo für {member.display_name}',
                          description=f'Dies ist eine Userinfo für den Member {member.mention}',
                          color=0x22a7f0)
    embed.add_field(name='Server beigetreten', value=member.joined_at.strftime('%d/%m/%Y, %H:%M:%S'),
                    inline=True)
    embed.add_field(name='Discord beigetreten', value=member.created_at.strftime('%d/%m/%Y, %H:%M:%S'),
                    inline=True)
    rollen = ''
    for role in member.roles:
        if not role.is_default():
            rollen += '{} \r\n'.format(role.mention)
    if rollen:
        embed.add_field(name='Rollen', value=rollen, inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text='Das ist die Userinfo!')
    mess = await ctx.channel.send(embed=embed)
    await mess.add_reaction('👌')
    print(str(ctx.author) + ' hat Userinfo-Befehl ausgeführt')

# Clear command

@client.command()
async def clear(ctx):
    embed = discord.Embed(title=f'{str(limit)} Nachrichten wurden gelöscht von {ctx.author}!', colour=discord.Colour.magenta())
    if not ctx.author.permissions_in(ctx.channel).manage_messages:
        await ctx.respond(embed=self.no_perms, delete_after=10)
    elif ctx.author.permissions_in(ctx.channel).manage_messages:
        await ctx.channel.purge(limit=limit, before=msg)
        await ctx.respond(embed=embed, delete_after=5)

# Shutdown

@client.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.channel.send('Bot wird heruntergefahren...\r\n'
                           'Das kann einige Minuten beanspruchen...')
    await client.close()
    print(str(ctx.author) + ' hat Bot beendet')

# On Ready method

@client.event
async def on_ready():
    print(f'Status: Online als {client.user}!')
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
