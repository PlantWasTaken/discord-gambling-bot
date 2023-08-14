import discord
from discord import app_commands
from discord.ext import commands
import yfinance as yf
from games import coin, get_bal, dice, send_money, price,buy_eq,sell_eq,get_portfolio,add_funds,baccarat

token = 'MTE0MDQwNDIwNTkxMjMzNDQ4OQ.GmpE-L.-fA6x7TVFCcwYhVHRwfMIj3_1Mj6Oz_alTfPBk'

client = discord.Client(intents = discord.Intents.all())

bot = commands.Bot(command_prefix='$',intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is ready")
    try:
        synced = await bot.tree.sync()
        print(len(synced))
    except Exception as e:
        print(e)

@bot.tree.command(name = "sendmoney")
@app_commands.describe(name = "Reciver of moneys")
@app_commands.describe(val = "Amount of moneys")
async def send(interaction: discord.Interaction, name:str, val:float):

    sender_id = interaction.user.id

    recipient_id =str(name[2:len(name)-1])

    result = send_money(str(sender_id),recipient_id,val)

    await interaction.response.send_message(result)


@bot.tree.command(name = "coin")
@app_commands.describe(val = "Bet")
async def play_coin(interaction: discord.Interaction, val:float):
    sender_id = interaction.user.id

    result = coin(str(sender_id),val)

    await interaction.response.send_message(result)


@bot.tree.command(name = "bal")
@app_commands.describe(user = "balance of user")
async def bal(interaction: discord.Interaction, user: str=None):
    if(user == None):
        discord_id = interaction.user.id
    else:
        discord_id = str(user[2:len(user)-1])
    
    bal = get_bal(str(discord_id))

    await interaction.response.send_message(f'{"<@"+str(discord_id)+">"} your balance is: {bal}')


@bot.tree.command(name = "dice")
@app_commands.describe(val = "Bet")
async def play_dice(interaction: discord.Interaction, val:float):
    sender_id = interaction.user.id

    result = dice(str(sender_id),val)

    await interaction.response.send_message(result)


@bot.tree.command(name = "stockprice")
@app_commands.describe(ticker = "stock ticker")
async def get_ticker_price(interaction: discord.Interaction, ticker:str):
    sender_id = interaction.user.id

    try:
        result = price(str(sender_id),ticker)
        await interaction.response.send_message(result)
    except Exception as e:
        await interaction.response.send_message(f'{"<@"+str(id)+">"} Please provide a ticker.')


@bot.tree.command(name = "buyshares")
@app_commands.describe(ticker = "Ticker (all capital letters)")
@app_commands.describe(amount = "How many shares")
async def user_buy_eq(interaction: discord.Interaction, ticker:str,amount:int):
    sender_id = interaction.user.id
    result = buy_eq(str(sender_id),ticker,amount)
    await interaction.response.send_message(result)

@bot.tree.command(name = "sellshares")
@app_commands.describe(ticker = "Ticker (all capital letters)")
@app_commands.describe(amount = "How many shares")
async def user_sell_eq(interaction: discord.Interaction, ticker:str,amount:int):
    sender_id = interaction.user.id
    result = sell_eq(str(sender_id),ticker,amount)
    await interaction.response.send_message(result)

@bot.tree.command(name = "portfolio")
@app_commands.describe(user = "Portfolio of user")
async def bal(interaction: discord.Interaction, user: str=None):
    if(user == None):
        discord_id = interaction.user.id
    else:
        discord_id = str(user[2:len(user)-1])
    
    portf = get_portfolio(str(discord_id))
    await interaction.response.send_message(portf)

@bot.tree.command(name = "addfunds")
@app_commands.describe(amount = "How much to add to account")
async def user_add_funds(interaction: discord.Interaction,amount:float):

    sender_id = interaction.user.id
    result = add_funds(str(sender_id),amount)

    await interaction.response.send_message(result)


@bot.tree.command(name = "baccarat")
@app_commands.describe(val = "bet")
@app_commands.describe(bet = "Who do you want to bet on")
@app_commands.choices(bet=[
    app_commands.Choice(name='bank', value=0),
    app_commands.Choice(name='player', value=1),
    app_commands.Choice(name='tie', value=2)
])
async def play_baccarat(interaction: discord.Interaction, val: float, bet: app_commands.Choice[int]):
    sender_id = interaction.user.id
    #print(val,bet.value)
    result = baccarat(str(sender_id),val,bet.value)
    await interaction.response.send_message(result)


if __name__ == "__main__":
    bot.run(token)
