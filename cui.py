#! /usr/bin/python3
# cui.py

# Author: justcats12

from classes import Event, Competitor, Battle, DNF

def home():
    """Homescreen where you can start a new comp or load on old one"""
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
    """create and start a new event"""
    # ask for event name
    name = input("Event name: ")
    # ask for competitor names
    print("Input competitor names, press return without name to submit")
    competitors = []
    counter = 1
    # ask for first competitor
    competitorName = input(f"Name competitor {counter}: ")
    competitors.append(Competitor(competitorName))
    # ask for other competitors
    while competitorName != "":
        counter += 1
        competitorName = input(f"Name competitor {counter}: ")
        if competitorName != "":
            competitors.append(Competitor(competitorName))
            
    # initialize event
    e = Event(name, competitors)
    doEvent(e)


def loadFromFile():
    # ask for file path
    fileName = input("File path: ")
    # load file
    try:
        e = Event(file=fileName)
    # try again if file not found
    except Exception():
        print("File not found")
        loadFromFile()
    # start the event
    doEvent(e)

def doEvent(event : Event):
    # sort competitors by rank
    event.sortCompetitorsByRank()
    # display ranking
    print(f"--- Event : {event.name} --- Top ---")
    for i in range(len(event.competitors)):
        print(f"{i+1}: {str(event.competitors[i])}")
    # print actions
    print("--- actions ---")
    print("1) Start battles")
    print("2) save & home")
    # ask user for action
    ans = input("> ")

    match ans:
        case "1":
            # start round
            startbattles(event)
        case "2":
            # ask for file name
            fileName = input("Filename: ")
            # write to file
            event.saveToFile(fileName)
            home()

def startbattles(e : Event):
    # call startround to initialize the battles
    e.startRound()
    # do each battle in the event.battles list
    for b in e.battles:
        doBattle(b)
    # wrap round up and get ready for the next
    e.endRound()
    doEvent(e)


def doBattle(battle : Battle):
    print(f"--- {battle} ---")
    # keep asking for times until there's a winner
    while not battle.hasWinner():
        # ask for time
        time = input(f"Round {battle.round} {battle.getCurrentCompetitor().name}: ")
        # set no inputed time to DNF
        if time == "":
            time = DNF
        # enter time into battle object, adding it to the competitor and round
        battle.playTurn(float(time))
    # display the winner
    print(f"Winner is {battle.getWinner().name}")
    # --> startbattles


home()