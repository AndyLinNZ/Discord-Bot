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
    await ctx.send(f"Lmao {ctx.message.author} is a fag!")

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
    lst = ["heads", "tails"]
    answer = random.choice(lst)
    if answer == decision:
        message = f"The bot got {answer} you win {int(amount) * 2}!"
    else:
        message = f"The bot got {answer} you're dogshit lmao you lost everything!"
    await ctx.send(message)







client.run("NjgxNjgzNjA1ODIyNzY3MTg3.XlSICA.6CEl1PBSi1p-7SdCWm8Y340K9E8")