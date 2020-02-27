import discord
from vars import token
import random
import sqlite3
from discord.ext import commands, tasks
import os
from insults import lst_of_insults
from itertools import cycle
import typing
import youtube_dl
from discord.utils import get
import os

client = commands.Bot(command_prefix = "now ")
status = cycle(["Simp Mania", "Danil", "Simpsons"])
players = {}

@client.event
async def hivin(ctx):
    await ctx.send("Lmao Hivin simps for Y_ _ _ y so hard")

@client.event
async def on_ready():
    change_status.start()
    # await client.change_presence(status=discord.Status.idle, activity=discord.Game("Simp Mania"))
    print("Bot is ready.")

@client.event
async def on_member_join(member):
    print(f"{member} has joined a server.")

@client.event
async def on_member_remove(member):
    print(f"{member} has left a server.")

@tasks.loop(seconds=30)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

@client.command()
async def gay(ctx):
    member_name, member_discriminator = str(ctx.message.author).split("#")
    await ctx.send(f"Lmao {member_name} is a fag!")

@client.command(aliases=["8ball"])
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

@client.command()
async def clear(ctx, amount=5):
    if amount > 100:
        amount = 100
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"Deleted {amount} messages.")

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    if reason == None:
        print(f"I kicked {member} for no reason.")
    else:
        print(f"I kicked {member} for {reason}")

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason)
    await ctx.send(f"Banned {member.mention}")

# @client.command(aliases = ["dc"])
# async def disconnect(ctx, member : discord.Member):
#     await member.disconnect()


@client.command(aliases=["bal"])
async def balance(ctx):
    userId = ctx.message.author.id
    username = ctx.message.author
    bal = show_balance(userId, username)
    id = f"<@{userId}>"
    await ctx.send(f"{id} your balance: ${bal}")

def show_balance(userId, username):
    connection = sqlite3.connect("./test.db")

    cursor = connection.cursor()
    sql = "SELECT * from userData where id = ?"
    cursor.execute(sql, (userId,))
    data = cursor.fetchone()
    connection.commit()
    connection.close()
    return data[2]

@client.command()
async def add(ctx, amount):
    userId = ctx.message.author.id
    stupid = ["Are you fucking stupid?", "You're actually brain damaged", "Shut up dumbass", f"Wait your iq is {amount}???"]
    username = ctx.message.author
    if int(amount) > 10000:
        amount = 10000
    if int(amount) > 0:
        insert(userId, username, amount)
    else:
        await ctx.send(f"{random.choice(stupid)}")



def insert(userId, username, amount):
    connection = sqlite3.connect("./test.db")

    cursor = connection.cursor()
    sql = "SELECT * from userData where id = ?"
    cursor.execute(sql, (userId,))
    data = cursor.fetchone()
    print(data)
    if data is None:
        cursor.execute("insert into userData values (?, ?, ?)", (str(userId), str(username), amount))
    else:
        cursor.execute("UPDATE userData set balance = balance + ? where id = ?",(amount, str(userId)))
    connection.commit()
    connection.close()

@client.command(aliases=["gamble","flip","coinflip"])
async def bet(ctx, amount, decision):
    userId = ctx.message.author.id
    lst = ["heads", "tails"]
    answer = random.choice(lst)
    message = bet_money(userId, amount, answer, decision)
    await ctx.send(message)

def bet_money(userId, amount, answer, decision):
    connection = sqlite3.connect("./test.db")

    cursor = connection.cursor()
    sql = "SELECT * from userData where id = ?"
    cursor.execute(sql, (userId,))
    data = cursor.fetchone()
    try:
        amount = int(amount)
        if data[2] >= amount and data is not None:
            if amount > 0:
                if answer == decision:
                    message = f"The bot got {answer} you win ${amount}!"
                    cursor.execute("UPDATE userData set balance = balance + ? where id = ?",(amount, str(userId)))
            
                else:
                    message = f"The bot got {answer} you're dogshit lmao you lost ${amount} dumbass!"
                    cursor.execute("UPDATE userData set balance = balance - ? where id = ?",(amount, str(userId)))
            else:
                message = "You cant bet your IQ dumb fuck!"
        else:
            message = "You're such a fucking idiot you dumbass you have no money you simp."
    except TypeError:
        message = "Type a whole number you fuckwit. Stop simping."

    connection.commit()
    connection.close()
    return message

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.member_discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return

@client.command()
async def insult(ctx, *, member : discord.Member):
    # lst = [f"{member.mention} is such a fucking simp", f"{member.mention} has coronavirus go die in a hole", f"Stop simping {member.mention}"]
    insult = random.choice(lst_of_insults)
    await ctx.send(f"{member.mention} {insult}")


@client.command()
async def simp(ctx, member : typing.Optional[discord.Member]):
    if member == None:
        member = ctx.message.author
    else:
        member = member
    num = random.randint(0, 100)
    await ctx.send(f"{member.mention}'s Simp level: {num}%")

@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")
    
    await ctx.send(f"Joined {channel}")

    # await voice.disconnect()

    # if voice and voice.is_connected():
    #     await voice.move_to(channel)
    # else:
    #     voice = await channel.connect()
    



@client.command()
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Remove old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("Error: Music playing")
        return

    await ctx.send("Getting everything ready now")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        "format":"bestaudio/best",
        "postprocessors": [{
            "key":"FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading song now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Rename File: {file}")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")


    # channel = ctx.message.author.voice.channel
    # await channel.connect()
    # guild = ctx.message.guild
    # voice_client = guild.voice_client
    # player = await voice_client.create_ytdl_player(url)
    # players[guild.id] = player
    # player.start()


@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Dont think I am in a channel")
        # await ctx.voice_client.disconnect()

@client.command()
async def howgay(ctx, member : typing.Optional[discord.Member]):
    if member == None:
        member = ctx.message.author
    else:
        member = member
    num = random.randint(0, 100)
    await ctx.send(f"{member.mention}'s Gay level: {num}%")

client.run(token)