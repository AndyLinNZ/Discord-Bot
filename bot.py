import discord
import random
import sqlite3
from discord.ext import commands

client = commands.Bot(command_prefix = "now ")

@client.event
async def on_ready():
    print("Bot is ready.")

@client.event
async def on_member_join(member):
    print(f"{member} has joined a server.")

@client.event
async def on_member_remove(member):
    print(f"{member} has left a server.")


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

@client.command()
async def gay(ctx):
    await ctx.send(f"Lmao you're a fag!")

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
        print(f"I kicked {member} for {reason})

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason)

# @client.command(aliases = ["dc"])
# async def disconnect(ctx, member : discord.Member):
#     await member.disconnect()


@client.command(aliases=["bal"])
async def balance(ctx):
    userId = ctx.message.author.id
    username = ctx.message.author
    print(username)

@client.command()
async def add(ctx, amount):
    userId = ctx.message.author.id
    print(str(userId) + "")
    print(type(str(userId) + ""))
    username = ctx.message.author
    insert(userId, username, amount)



def insert(userId, username, amount):
    connection = sqlite3.connect("./test.db")

    cursor = connection.cursor()
    sql = "SELECT * from userInfo where id = ?"
    cursor.execute(sql, str(userId))
    data = cursor.fetchone()
    print(data)
    # cursor.execute("insert into userInfo values (?, ?, ?)", (str(userId), str(username), amount))
    connection.commit()
    connection.close()





client.run("NjgxNjgzNjA1ODIyNzY3MTg3.XlSICA.6CEl1PBSi1p-7SdCWm8Y340K9E8")