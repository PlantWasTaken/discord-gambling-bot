import random
import json
import yfinance as yf

text_to_emote = {
        "1" : ":one:",
        "2" : ":two:",
        "3" : ":three:",
        "4" : ":four:",
        "5" : ":five:",
        "6" : ":six:",
        "7" : ":seven:",
        "8" : ":eight:",
        "9" : ":nine:"
    }


def banking(id,result,v): #result is True for win, False for loss
    with open("banking.json", "r") as jsonFile:
        data = json.load(jsonFile)

    if(result == True):
        data[id]['bank'] = data[id]['bank']+v #add to user
        data['bank'] = data['bank']-v         #remove from bank
    else:
        data[id]['bank'] = data[id]['bank']-v #remove from user
        data['bank'] = data['bank']+v         #add to bank

    with open("banking.json", "w") as jsonFile:
        json.dump(data, jsonFile,indent=4)

def get_bal(id):
    round_all()

    with open("banking.json", "r") as jsonFile:
        data = json.load(jsonFile)

    return data[id]['bank']

def add_user(id):
    standard_user = {
        "bank": 1000,
        "stock": {
            "TSLA": 0,
            "AMZN": 0
        }
    }

    with open("banking.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data[id] = standard_user

    with open("banking.json", "w") as jsonFile:
        json.dump(data, jsonFile,indent=4)

def check_user(id,v):
    with open("banking.json", "r") as jsonFile:
        data = json.load(jsonFile)

    try: #checks to see if user is in system
        data[id]
    except KeyError: #if not add the user
        add_user(id)

    if(get_bal(id) <= v): #checks if user has balance
        return False
    else:
        return True
    
def coin(id,v):
    round_all() #rounds all prices before showing ot user
    
    #addds new user, if id not present also checks bet size
    if(check_user(id, v) == True): 
        pass #(user has been made) bet has been verified
    else:
        msg = "Not enough funds\n <@" + str(id)+ ">" + "your balance is: " + str(get_bal(id))
        return msg
    

    #1-49 = win 50-100 loss
    val = random.randint(1,1000)

    if(val <= 499):
        banking(id,True,v) #win
        msg = "You Won: " + str(v) + "\n <@" + str(id)+ ">" + "your new balance is: " + str(get_bal(id))
    else:
        banking(id,False,v) #loss
        msg = "You lost: " + str(v) + "\n <@" + str(id)+ ">" + "your new balance is: " + str(get_bal(id))
    
    return msg

def dice(id,v):
    round_all() #rounds all prices before showing ot user

    if(check_user(id, v) == True): 
        pass #(user has been made) bet has been verified
    else:
        msg = "Not enough funds\n <@" + str(id)+ ">" + "your balance is: " + str(get_bal(id))
        return msg

    house = [random.randint(1,5) for _ in range(5)]
    player = [random.randint(1,5) for _ in range(5)]

    #output format
    # House 1 2 3 4 5 sum: 15
    # @id 1 2 3 4 6 sum: 16
    # you won/lost - new balance
    house_to_emote = " ".join([text_to_emote[str(i)] for i in house])
    player_to_emote = " ".join([text_to_emote[str(i)] for i in player])
    
    if (sum(house) == sum(player)):
        banking(id,False,v) #loss
        msg1 = "House: " + house_to_emote +" Sum: " + str(sum(house)) + "\n"
        msg2 = "Player: " + player_to_emote +" Sum: " + str(sum(player)) + "\n"
        msg3 = "You lost: " + str(v) + " " + "<@" + str(id)+ ">" + " your new balance is: " + str(get_bal(id))

        msg = msg1+msg2+msg3
    
    elif(sum(house) > sum(player)):
        banking(id,False,v) #loss
        msg1 = "House: " + house_to_emote +" Sum: " + str(sum(house)) + "\n"
        msg2 = "Player: " + player_to_emote +" Sum: " + str(sum(player)) + "\n"
        msg3 = "You lost: " + str(v) + " " + "<@" + str(id)+ ">" + " your new balance is: " + str(get_bal(id))

        msg = msg1+msg2+msg3

    else:
        #win
        banking(id,True,v) #win
        msg1 = "House: " + house_to_emote +" Sum: " + str(sum(house)) + "\n"
        msg2 = "Player: " + player_to_emote +" Sum: " + str(sum(player)) + "\n"
        msg3 = "You Won: " + str(v) + " " + "<@" + str(id)+ ">" + " your new balance is: " + str(get_bal(id))

        msg = msg1+msg2+msg3


    return msg

def send(id,recipient_id,v):
    round_all() #rounds all prices before showing ot user
    if(v < 0):
        return "<@"+str(id)+">" + " You cant send a negative amount."
    
    if(check_user(id, v) == True): 
        pass #(user has been made) bet has been verified
    else:
        msg = "Not enough funds\n <@" + str(id)+ ">" + "your balance is: " + str(get_bal(id))
        return msg
    
    check_user(recipient_id,0)

    with open("banking.json", "r") as jsonFile:
        data = json.load(jsonFile)

    data[id]['bank'] = data[id]['bank']-v                 #remove from sender
    data[recipient_id]['bank'] = data[recipient_id]['bank']+v #add to recipient

    
    with open("banking.json", "w") as jsonFile:
        json.dump(data, jsonFile,indent=4)

    msg = "You sent: " + str(v) + " to: " + "<@"+str(recipient_id)+">"
    return msg

def price(id,ticker):
    try: #look up ticker
        yfticker = yf.Ticker(ticker)  #ticker exists
        price = yfticker.info
        msg = "<@"+str(id)+">"+" The asking price for " + ticker + " is: " + str(price['ask'])
        return msg
    except:
        return "<@"+str(id)+">" + " Ticker does not exist"
        
def buy_eq(id,ticker,v):
    if(v <= 0):
        return "<@"+str(id)+">" +" Buy more than 0 shares"

    with open("banking.json", "r") as jsonFile:
        data = json.load(jsonFile)

#check if ticker exists, if user doesnt own any add to their profile, if stock doesnt exist return error

    try: #look up ticker
        yfticker = yf.Ticker(ticker)  #ticker exists
        yfticker.info

    except:
        return "<@"+str(id)+">" +" Ticker does not exist"
    
    try:
        a = data[id]['stock'][ticker] #check if ticker is in profile
    except:
        data[id]['stock'][ticker] = 0 #add to their profile

    yfticker = yf.Ticker(ticker)  #ticker exists
    ask = float(yfticker.info['ask'])

    #check_user(id,ask*v)
    if(check_user(str(id), ask*v) == True): 
        pass #(user has been made) bet has been verified
    else:
        msg = "Not enough funds\n <@" + str(id)+ ">" + " You need: " + str(ask*v) +"\nYour balance is: " + str(get_bal(id))+"\n You can afford: "+ str(data[id]['bank']//ask)+ " shares."
        return msg

    total_price = ask*v
    data[id]['stock'][ticker] = data[id]['stock'][ticker]+v #buying shares
    data[id]['bank'] = data[id]['bank']-total_price #subtracting price

    with open("banking.json", "w") as jsonFile: #send changes
        json.dump(data, jsonFile,indent=4)

    round_all() #rounds all prices before showing ot user

    with open("banking.json", "r") as jsonFile: #get fresh data after changes
        data = json.load(jsonFile)

    msg = "<@"+str(id)+">"+" You bought "+str(v)+" shares of " + ticker + "\nSum: " + str(total_price) + "\nYour balance is: " + str(get_bal(id))
    return msg

def sell_eq(id,ticker,v):
    if(v <= 0):
        return "<@"+str(id)+">" +" Sell more than 0 shares"

    with open("banking.json", "r") as jsonFile:
        data = json.load(jsonFile)

    #check if ticker exists in user profile, if stock doesnt exist return error
    try: #look up ticker
        yfticker = yf.Ticker(ticker)  #ticker exists
        yfticker.info

    except:
        return "<@"+str(id)+">" +" Ticker does not exist"
    
    try:
        a = data[id]['stock'][ticker] #check if ticker is in profile
    except:
        return "<@"+str(id)+">" +" You dont own shares of " + str(ticker)

    if(data[id]['stock'][ticker] < v): #checks to see if user tries to sell more shares than owned
        return "You cannot sell " + str(v) + " shares.\n"+"<@"+str(id)+">" + " You own: " + str(data[id]['stock'][ticker]) + " " + ticker +" shares."

    yfticker = yf.Ticker(ticker)  #ticker exists
    ask = float(yfticker.info['ask'])

    total_price = ask*v
    data[id]['stock'][ticker] = data[id]['stock'][ticker]-v #selling shares
    data[id]['bank'] = data[id]['bank']+total_price #adding sum to bank

    with open("banking.json", "w") as jsonFile: #send changes
        json.dump(data, jsonFile,indent=4)

    round_all() #rounds all prices before showing ot user

    with open("banking.json", "r") as jsonFile: #get fresh data after changes
        data = json.load(jsonFile)

    msg = "<@"+str(id)+">"+" Sold "+str(v)+" shares of " + ticker + "\nSum: " + str(total_price) + "\nYour balance is: " + str(get_bal(id))
    return msg

def get_portfolio(id):
    with open("banking.json", "r") as jsonFile:
        data = json.load(jsonFile)

    tickers = []
    amount = []
    prices = []
    for i in data[id]['stock']: #getting all tickers
        tickers.append(i)

    for i in tickers: #getting amountof shares per ticker
        amount.append(int(data[id]['stock'][i]))

        yfticker = yf.Ticker(i)  #ticker exists
        ask = float(yfticker.info['ask'])
        prices.append(float(ask))

    round_all() #rounds all prices before showing ot user

    msg = "<@"+str(id)+">"+" You own\n" #calculating prices
    for i in range(len(amount)):
        if(amount[i] == 0):
            pass
        else:
            msg = msg + str(tickers[i])+" : "+str(amount[i])+" Total: "+str(amount[i]*prices[i])+"\n" #formatting prices
    
    sum_all = sum([amount[i]*prices[i] for i in range(len(tickers))])
    msg = msg + "Grand total: " + str(sum_all)

    return msg

def round_all():
    with open("banking.json", "r") as jsonFile:
        data = json.load(jsonFile)
    
    user_ids = []
    for i in data:
        user_ids.append(str(i))
    user_ids.pop(0) #removes bank

    for i in user_ids:
        data[i]['bank'] = round(data[i]['bank'], 2)
    
    with open("banking.json", "w") as jsonFile: #send changes
        json.dump(data, jsonFile,indent=4)
#coin("751324191923503105", 100)
#dice("751324191923503105", 100)
#print(buy_eq("972980724951040051", "TSLA", 9))
#get_portfolio("972980724951040051")
#round_all()
