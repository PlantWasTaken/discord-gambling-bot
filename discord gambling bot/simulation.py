import random
import plotly.express as px

def coin():
    user = 10
    bank = 10
    u = []
    b = []
    s = []

    for i in range(100):
        val = random.randint(1,1000)
        if(val <= 499):
            user = user + 1
            bank = bank - 1

            u.append(user)
            b.append(bank)
            s.append(user+bank)
        else:
            user = user - 1
            bank = bank + 1

            u.append(user)
            b.append(bank)
            s.append(user+bank)

    fig = px.line(y=[b,u,s])
    fig.show()

def dice():
    user = 100
    bank = 100
    u = []
    b = []

    for i in range(100000):
        house = [random.randint(1,5) for _ in range(5)]
        player = [random.randint(1,5) for _ in range(5)]

        if (sum(house) == sum(player)):
            user = user - 1
            bank = bank + 1
        elif(sum(house) > sum(player)):
            user = user - 1
            bank = bank + 1
        else:
            user = user + 1
            bank = bank - 1
        
        u.append(user)
        b.append(bank)

    
    fig = px.line(y=[b,u])
    fig.show()

dice()