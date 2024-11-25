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
    pass

def doBattle(battle : Event):
    pass