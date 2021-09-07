import asyncio
import time
import discord
from discord.ext import commands
import youtube_dl
import os
import string
import secrets

# This code was written by github.com/NiklasWyld

my_secret = os.environ['token']

intents = discord.Intents.all()
client = discord.Client()
client = commands.Bot(command_prefix='$', intents=intents)
client.remove_command('help')
client.remove_command('game:')


def is_not_pinned(mess):
    return not mess.pinned


#MusikBot


@client.command()
async def play(ctx, url: str):
    if not ctx.author.voice:
        await ctx.author.send('Du musst in einen Sprach-Kanal für diesen Befehl sein!')
        return
    if os.path.isfile('song.mp3'):
        try:
            os.remove("song.mp3")
        except PermissionError:
            await ctx.author.send("Warte bis der bereits spielende Song endet!")
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
    voice.play(discord.FFmpegPCMAudio("song.mp3"))




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
        await ctx.author.send("Der Bot ist in keinen Kanal!")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.author.send("Zur Zeit spielt keine Musik!")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.author.send("Es wurde keine Musik pausiert!")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()


#Befehle


@client.command()
async def help(ctx, member: discord.Member = None):
    embed = discord.Embed(title="Hilfe-Menü", description="Help-Menu von Immerzock-Bot", color=0x00ff00)
    embed.add_field(name="Test", value="$test - Testet den Bot", inline=False)
    embed.add_field(name="Datum", value="$datum - Zeigt das Datum", inline=False)
    embed.add_field(name="Uhrzeit", value="$uhrzeit - Zeigt die Uhrzeit", inline=False)
    embed.add_field(name="Help", value="$help - Dieser Befehl", inline=False)
    embed.add_field(name="Bester-Rapper", value="$besterrapper - Zeigt besten Rapper", inline=False)
    embed.add_field(name="Komponenten", value="$komponenten - Zeigt Niklas`s Komponenten", inline=False)
    embed.add_field(name="Open-Source", value="$opensource - Zeigt Info zum Code des Bot´s", inline=False)
    embed.add_field(name="Username", value="$username - Zeigt deinen Username", inline=False)
    embed.add_field(name="User-Info", value="$userinfo (User) - Zeigt Userinfo", inline=False)
    embed.add_field(name="Clear", value="$clear (Zahl) - Löscht bestimmte Anzahl von Nachrichten **(ONLY ADMIN)**", inline=False)
    embed.add_field(name="Email", value="$email - Zeigt eine Email-Adresse für Fragen", inline=False)
    embed.add_field(name="Kick", value="$kick (Username) - Kickt den User **(ONLY ADMIN)**", inline=False)
    embed.add_field(name="Ban", value="$ban (Username) - Bannt den User **(ONLY ADMIN)**", inline=False)
    embed.add_field(name="Say", value="$say (Nachricht) - Wiederholt deine Nachricht", inline=False)
    embed.add_field(name="Weristonline", value="$weristonline - Zeigt wer online ist", inline=False)
    embed.add_field(name="Gamemode", value="$gamemode (1 - 0) - Wechselt den Gamemode", inline=False)
    embed.add_field(name="MusikBot", value="**Zur Zeit ist der Musikbot außer Betrieb! Wir arbeiten mit hochtouren!**", inline=False)
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/806062613716271144/849881814738927646/d04bff1caa1c75d82fd3d4e827cafc74.png")
    mess = await ctx.channel.send(embed=embed)
    await mess.add_reaction("👍")
    print(str(ctx.author) + " hat Help-Befehl ausgeführt")


#Game


@client.command()
async def spiel(ctx):
    return


@client.listen('on_message')
async def on_message(message):
    if message.channel.id == 842091120276275232:
        if message.content.startswith("$spiel"):
            await message.channel.send("Das spiel startet jetzt!")
            await message.channel.send("Du musst immer mit **game: (Argument)** antworten!")
            await asyncio.sleep(1)
            await message.channel.send("Junge oder Mädchen")
            print(str(message.author) + " hat Spiel-Befehl ausgeführt")
        if message.content.startswith("game: Junge"):
            await message.channel.send("Tanzen\r\n"
                                       "Spielen\r\n"
                                       "Küssen\r\n"
                                       "Liebesbrief schreiben")
        if message.content.startswith("game: Mädchen"):
            await message.channel.send("Tanzen\r\n"
                                       "Spielen\r\n"
                                       "Küssen\r\n"
                                       "Liebesbrief schreiben")
        if message.content.startswith("game: Tanzen"):
            await message.channel.send("J=Junge M=Mädchen\r\n"
                                       "1-7(J)oder(M)")
        if message.content.startswith("game: Spielen"):
            await message.channel.send("J=Junge M=Mädchen\r\n"
                                       "1-7(J)oder(M)")
        if message.content.startswith("game: Küssen"):
            await message.channel.send("J=Junge M=Mädchen\r\n"
                                       "1-7(J)oder(M)")
        if message.content.startswith("game: Liebesbrief schreiben"):
            await message.channel.send("J=Junge M=Mädchen\r\n"
                                       "1-7(J)oder(M)")
        if message.content.startswith("game: 1(J)"):
            await message.channel.send("Benedikt")
        if message.content.startswith("game: 2(J)"):
            await message.channel.send("Niklas")
        if message.content.startswith("game: 3(J)"):
            await message.channel.send("Sebastian")
        if message.content.startswith("game: 4(J)"):
            await message.channel.send("Kai")
        if message.content.startswith("game: 5(J)"):
            await message.channel.send("Dein Vada")
        if message.content.startswith("game: 6(J)"):
            await message.channel.send("Johannes")
        if message.content.startswith("game: 7(J)"):
            await message.channel.send("Herr Felli")
        if message.content.startswith("game: 1(M)"):
            await message.channel.send("Albina")
        if message.content.startswith("game: 2(M)"):
            await message.channel.send("Deine Mudda")
        if message.content.startswith("game: 3(M)"):
            await message.channel.send("Annika")
        if message.content.startswith("game: 4(M)"):
            await message.channel.send("Hanna")
        if message.content.startswith("game: 5(M)"):
            await message.channel.send("Annika Fink")
        if message.content.startswith("game: 6(M)"):
            await message.channel.send("Frau Rothammi")
        if message.content.startswith("game: 7(M)"):
            await message.channel.send("Frau Magrafi")
    if not message.channel.id == 842091120276275232:
        return


#Game(Ende)


@client.command()
async def code(ctx):
    y = string.digits + string.ascii_uppercase
    x = int(ctx.message.content.split(" ")[1])
    await ctx.send(''.join(secrets.choice(y) for i in range(x)))


@client.command()
async def uhrzeit(ctx):
    await ctx.channel.send(time.strftime("%H: %M: %S"))
    print(str(ctx.author) + "hat Uhrzeit-Befehl ausgeführt")


@client.command()
async def datum(ctx):
    await ctx.channel.send(time.strftime("%d. %m. %y"))
    print(str(ctx.author) + " hat Datum-Befehl ausgeführt")


@client.command()
async def besterrapper(ctx):
    await ctx.channel.send("Natürlich Peep!!!")
    print(str(ctx.author) + " hat Bester-Rapper-Befehl ausgeführt")


@client.command()
async def komponenten(ctx, member: discord.Member = None):
    embed = discord.Embed(title="Komponenten", description="Komponenten von Niklas", color=0x00ff00)
    embed.add_field(name="Tastartur", value="https://www.mediamarkt.de/de/product/_razer-razer-ornata-v2-2668151.html",
                    inline=False)
    embed.add_field(name="Maus",
                    value="https://www.expert.de/shop/unsere-produkte/gaming-freizeit/pc-gaming-zubehor/gaming-mause/17620013236-m65-rgb-elite-schwarz-gaming-maus.html",
                    inline=False)
    embed.add_field(name="Monitor-1",
                    value="https://www.amazon.de/AOC-G2590VXQ-DisplayPort-Reaktionszeit-1920x1080/dp/B078S36XWV/ref=sr_1_1?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=AOC+2590G4&qid=1618155834&sr=8-1",
                    inline=False)
    embed.add_field(name="Monitor-2",
                    value="https://www.expert.de/shop/unsere-produkte/computer-zubehor/monitore-beamer/monitore/17160011033-r240y-monitor.html?branch_id=2237090&adword=shopping_op&gclid=CjwKCAjwvMqDBhB8EiwA2iSmPLZ9JMVa83v3PHuPFvp36Vddpp1uowm8HHS7gIAtAgESqozYFrA5nxoCtEEQAvD_BwE",
                    inline=False)
    embed.add_field(name="Stream Deck Mini",
                    value="https://www.amazon.de/Elgato-Stream-Deck-personaliserbaren-einstellbaren/dp/B07DYRS1WH/ref=sr_1_2_sspa?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=32ENOGQ9W9LES&dchild=1&keywords=streamdeck&qid=1618155919&sprefix=strea%2Caps%2C199&sr=8-2-spons&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzN0wyM0JYMFoyWFEwJmVuY3J5cHRlZElkPUEwOTAzMjg0M1VVODUxNUxZMEtLViZlbmNyeXB0ZWRBZElkPUEwNTIxMDM0MjRUSU1OTllLUTVXVyZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU&th=1",
                    inline=False)
    embed.add_field(name="Mikrofon",
                    value="https://www.expert.de/shop/unsere-produkte/gaming-freizeit/pc-gaming-zubehor/sonstiges-gaming-zubehor/17670019410-gaming-mikrofon-stream-400-plus.html",
                    inline=False)
    mess = await ctx.channel.send(embed=embed)
    await mess.add_reaction("👍")
    print(str(ctx.author) + " hat Komponenten-Befehl ausgeführt")

#Join-Message


@client.event
async def on_member_join(member):
    await member.send(f"Willkommen auf **{member.guild}**!")
    print(f"{member.name} ist auf {member.guild} gejoint")


#Andere Befehle


@client.command()
async def weristonline(ctx):
  ctx.channel.send(f"Dieser Befehl ist zur Zeit nicht verfügbar. Versuch es später nochmal {ctx.author.mention}")


@client.command()
async def invite(ctx):
  await ctx.channel.send(f"https://discordapp.com/oauth2/authorize?&client_id=" + client.user.id + "&scope=bot&permissions=0")


@client.command()
@commands.is_owner()
async def server(ctx):
    for guild in client.guilds:
        print(str(guild.name))


@commands.has_permissions(kick_members=True)
@client.command()
async def kick(ctx, user: discord.Member, *, reason="Keine Reason"):
        await user.kick(reason=reason)
        print(f'{ctx.author} hat {user.name} gekickt!')
        kick = discord.Embed(title=f":boot: Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.message.delete()
        await ctx.channel.send(embed=kick)
        await user.send(embed=kick)


@commands.has_permissions(ban_members=True)
@client.command()
async def ban(ctx, user: discord.Member, *, reason="Keine Reason"):
        await user.ban(reason=reason)
        print(f'{ctx.author} hat {user.name} gebannt!')
        ban = discord.Embed(title=f":boot: Banned {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.message.delete()
        await ctx.channel.send(embed=ban)
        await user.send(embed=ban)


@client.command()
async def test(ctx):
    await ctx.channel.send("Test erfolgreich!")
    print(str(ctx.author) + " hat Test durchgeführt")


@client.command()
async def username(ctx):
    await ctx.channel.send(str(ctx.author))
    print(str(ctx.author) + " hat Username-Befehl ausgeführt")


@client.command()
async def say(ctx, *, message: str = None):
    if message is not None:
        await ctx.channel.send("Nachricht:", value=message)
        embed = discord.Embed(title=f'{ctx.author.name}`s message', color=0x010101)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name='Nachricht:', value=message)
        await ctx.message.delete()
        await ctx.channel.send(embed=embed)

    else:
        await ctx.message.delete()
        await ctx.channel.send(f'> {ctx.author.mention} bitte gib eine gültige Nachricht ein!')


@client.command()
async def opensource(ctx):
    await ctx.channel.send("Dieser Bot ist nicht Opensource!\r\n"
                           "Aber auf **GitHub** könnt ihr viel Code zum kopieren und einfügen finden!\r\n"
                           "GitHub: https://github.com/NiklasWyld/BotTutorial")
    print(str(ctx.author) + " hat Opensource-Befehl ausgeführt")


@client.command()
async def email(ctx):
    await ctx.channel.send("Unter dieser Email könnt ihr mir Fragen und Anliegen schreiben:\r\n"
                           "immerzock.management@gmail.com\r\n"
                           "**SPAM WIRD BLOCKIERT**")
    print(str(ctx.author) + " hat Email-Befehl ausgeführt")


@client.command()
async def getid(ctx):
    await ctx.channel.send(f'{ctx.author.mention} das wird nur den Owner angezeigt')
    print(f'ID: {client.user}')
    print(f'{ctx.author} hat GetID-Befehl ausgeführt')
    await asyncio.sleep(1)
    await ctx.channel.purge(limit=2)


@client.command()
@commands.is_owner()
async def botverify(ctx):
    await ctx.channel.send(
        "Gib **$Verifizierung** in den Chat ein, und befolge die folgenden Anweisungen um Zugriff auf den Server zu erhalten!")


# Verifizierung


@client.listen('on_message')
async def on_message(message):
    if message.author.bot:
        return
    if message.channel.id == 876772133437603886:
        if not message.content.startswith("$Verifizierung"):
            await message.channel.purge(limit=1)
        if message.content.startswith("$Verifizierung"):
            await asyncio.sleep(5)
            await message.channel.purge(limit=1)


@client.command()
async def Verifizierung(ctx, member: discord.Member = None):
    if not ctx.channel.id == 876772133437603886:
        return
    if ctx.channel.id == 876772133437603886:
        member = member if member else ctx.author
    welcome_channel_id = 876772133437603886
    welcome_channel = client.get_channel(welcome_channel_id)
    msg = await welcome_channel.send(embed=discord.Embed(title="Verifizierung",
                                                         description=f"{member.mention} Reagiere auf diese Nachricht mit einen Daumen nach oben! Somit bekommst du Zugriff auf den Server.",
                                                         color=discord.Color.red()))
    await msg.add_reaction('👍')

    def _check(r, u):
        return str(r.emoji) == '👍' and r.message == msg and u == member

    try:
        r, u = await client.wait_for('reaction_add', check=_check, timeout=60)
        role = discord.utils.get(ctx.guild.roles, name="Community")
        await u.add_roles(role, reason="Verifizierung")
        await msg.delete()
        print(str(ctx.author) + " hat sich verifiziert!")
    except asyncio.TimeoutError:
        await msg.edit(embed=discord.Embed(title="⛔Verifizierung abgebrochen⛔",
                                           description=f"{member.mention} Deine Antwort hat zu lange gedauert versuche es nitte erneut.",
                                           color=discord.Color.red()), delete_after=60)


#Gamemode


@client.command()
async def gamemode(ctx):
    return


@client.listen('on_message')
async def on_message(message):
    csend = message.channel
    if message.content.startswith("$gamemode"):
        await csend.send("Welchen Gamemode willst du? **1** - **0**")
    if message.content.startswith("$gamemode 1"):
        await csend.send("Gamemode was successfully changed to 1!")
        print(str(message.author) + " hat Gamemode-Befehl ausgeführt")
    if message.content.startswith("$gamemode 0"):
        await csend.send("Gamemode was successfully changed to 0!")
        print(str(message.author) + " hat Gamemode-Befehl ausgeführt")


#Embeds


@client.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member if member else ctx.author
    embed = discord.Embed(title=f"Userinfo für {member.display_name}",
                          description=f"Dies ist eine Userinfo für den Member {member.mention}",
                          color=0x22a7f0)
    embed.add_field(name="Server beigetreten", value=member.joined_at.strftime("%d/%m/%Y, %H:%M:%S"),
                    inline=True)
    embed.add_field(name="Discord beigetreten", value=member.created_at.strftime("%d/%m/%Y, %H:%M:%S"),
                    inline=True)
    rollen = ""
    for role in member.roles:
        if not role.is_default():
            rollen += "{} \r\n".format(role.mention)
    if rollen:
        embed.add_field(name="Rollen", value=rollen, inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text="Das ist die Userinfo!")
    mess = await ctx.channel.send(embed=embed)
    await mess.add_reaction("👌")
    print(str(ctx.author) + " hat Userinfo-Befehl ausgeführt")


@client.command()
async def clear(ctx):
    if not ctx.author.permissions_in(ctx.channel).manage_messages:
        await ctx.channel.send(str(ctx.author) + " du hast nicht die nötigen Rechte!")
    if ctx.author.permissions_in(ctx.channel).manage_messages:
        args = ctx.message.content.split(" ", maxsplit=1)
        if len(args) == 2:
            if args[1].isdigit():
                count = int(args[1]) + 1
                deleted = await ctx.channel.purge(limit=count, check=is_not_pinned)
                await ctx.channel.send("{} Nachrichten gelöscht.".format(len(deleted) - 1))
                await asyncio.sleep(1)
                await ctx.channel.purge(limit=1)
            print(str(ctx.author) + " hat Clear-Befehl ausgeführt")


#Shutdown


@client.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.channel.send("Bot wird heruntergefahren...\r\n"
                           "Das kann einige Minuten beanspruchen...")
    await ctx.bot.logout()
    print(str(ctx.author) + " hat Bot beendet")


#admin-login-logout


list = '586193546017505281 677935302190432287'
nutzer = 'Fuchs.Bene Wild.Niklas'
kennung = '!AdminImmerzock?loginservice Wild2020'


@client.command()
async def login(ctx):
  if ctx.channel.id == 877238528994582598:
      if f"{ctx.author.id}" in list:
            await ctx.send("Wird eingeloggt...")
            Rolle = discord.utils.get(ctx.message.author.guild.roles, name="Admin")
            await ctx.author.add_roles(Rolle)
            await ctx.send("Eingeloggt! Bitte logge dich später wieder aus mit '$logout'")
            await asyncio.sleep(10)
            await ctx.channel.purge(limit=3)
      if f"{ctx.author.id}" not in list:
          await ctx.send("Ungültiger Login!")
  if not ctx.channel.id == 877238528994582598:
      return


@client.command()
async def logout(ctx):
    if ctx.channel.id == 877238528994582598:
        if f"{ctx.author.id}" in list:
            await ctx.send("Wird ausgeloggt...")
            Rolle = discord.utils.get(ctx.message.author.guild.roles, name="Admin")
            await ctx.author.remove_roles(Rolle)
            await ctx.send("Ausgeloggt! Du kannst dich später wieder einloggen mit '$login'")
        if f"{ctx.author.id}" not in list:
            await ctx.send("Ungültiger Logout!")
    if not ctx.channel.id == 877238528994582598:
        return


#Status


@client.event
async def on_ready():
    print(f'Status: Online als {client.user}!')
    client.loop.create_task(status_task())


async def status_task():
    while True:
        await client.change_presence(activity=discord.Game("Immerzock Bot"), status=discord.Status.online)
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Game("$help"), status=discord.Status.online)
        await asyncio.sleep(10)


client.run(my_secret)