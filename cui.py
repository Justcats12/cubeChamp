from classes import Event, Competitor, Battle

def home():
    print("---Home---")
    print("1) Start new comp")
    print("2) Load comp from file")
    print("3) Quit")

    ans = input("> ")

    match ans:
        case "1":
            newEvent()
        case "2":
            loadFromFile()
            
        case "3":
            exit(0)
        case _:
            home()

def newEvent():
    name = input("Event name: ")
    
    print("Input competitor names, press return without name to submit")
    competitors = []
    counter = 1
 
    competitorName = input(f"Name competitor {counter}: ")
    competitors.append(Competitor(competitorName))
    
    while competitorName != "":
        counter += 1
        competitorName = input(f"Name competitor {counter}: ")
        if competitorName != "":
            competitors.append(Competitor(competitorName))
            
    
    e = Event(name, competitors)
    doEvent(e)


def loadFromFile():
    fileName = input("File path: ")
    try:
        e = Event(file=fileName)
    except Exception():
        print("File not found")
        loadFromFile()
    doEvent(e)

def doEvent(event : Event):
    event.sortCompetitorsByRank()
    print(f"--- Event : {event.name} --- Top ---")
    for i in range(len(event.competitors)):
        print(f"{i+1}: {str(event.competitors[i])}")
    
    print("--- actions ---")
    print("1) Start battles")
    print("2) save & home")

    ans = input("> ")

    match ans:
        case "1":
            startbattles(event)
        case "2":
            fileName = input("Filename: ")
            event.saveToFile(fileName)
            home()

def startbattles(e : Event):
    e.startRound()
    for b in e.battles:
        doBattle(b)
    
    e.endRound()
    doEvent(e)


def doBattle(battle : Battle):
    print(f"--- {battle} ---")

    while not battle.hasWinner():
        time = input(f"Round {battle.round} {battle.getCurrentCompetitor().name}: ")
        
        if time == "":
            time = -1
        
        battle.playTurn(float(time))
    
    print(f"Winner is {battle.getWinner().name}")
    # --> startbattles


home()