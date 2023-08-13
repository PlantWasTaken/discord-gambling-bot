import discord
from discord.ext import commands
import yfinance as yf
from games import coin, get_bal, dice, send, price,buy_eq,sell_eq,get_portfolio

token = ''

client = discord.Client(intents = discord.Intents.all())

channel = 1069711820698419322

bot = commands.Bot(command_prefix='$',intents = discord.Intents.all())


@bot.command(name = "send")
async def test(ctx):
    id = ctx.message.author.id
    val = ctx.message.content.split()[1:]

    recipient_id = str(val[0][2:len(val[0])-1])
    val = int(val[1])

    result = send(str(id),str(recipient_id),val)

    await ctx.send(result)

@bot.command(name = "coin")
async def test(ctx):
    id = ctx.message.author.id
    val = ctx.message.content.split()[1:][0]

    result = coin(str(id),int(val))

    await ctx.send(result)

@bot.command(name = "bal")
async def test(ctx):
    id = ctx.message.author.id

    try:
        val = ctx.message.content.split()[1:][0] #fetched id of user pinged
        if(len(val) != 0):
            id = str(int(val[2:len(val)-1]))
    except:
        pass

    bal = get_bal(str(id))

    await ctx.send("<@"+str(id)+"> Your balance is: " + str(bal))

@bot.command(name = "dice")
async def test(ctx):
    id = ctx.message.author.id
    val = ctx.message.content.split()[1:][0]

    result = dice(str(id),int(val))

    await ctx.send(result)

@bot.command(name = "price")
async def test(ctx):
    id = ctx.message.author.id
    ticker = ctx.message.content.split()[1:][0]
    try:
        result = price(str(id),str(ticker))

        await ctx.send(result)
    except:
        await ctx.send("<@"+str(id)+"> Please provide a ticker.")

@bot.command(name = "buy")
async def test(ctx):
    id = ctx.message.author.id
    msg = ctx.message.content.split()[1:]

    ticker = msg[0]
    amount = int(msg[1])

    result = buy_eq(str(id),ticker,amount)
    await ctx.send(result)

@bot.command(name = "sell")
async def test(ctx):
    id = ctx.message.author.id
    msg = ctx.message.content.split()[1:]

    ticker = msg[0]
    amount = int(msg[1])

    result = sell_eq(str(id),ticker,amount)
    await ctx.send(result)

@bot.command(name = "portfolio")
async def test(ctx):
    id = ctx.message.author.id

    try:
        val = ctx.message.content.split()[1:][0] #fetched id of user pinged
        if(len(val) != 0):
            id = str(int(val[2:len(val)-1]))
    except:
        pass

    portf = get_portfolio(str(id))
    await ctx.send(portf)

if __name__ == "__main__":
    bot.run(token)