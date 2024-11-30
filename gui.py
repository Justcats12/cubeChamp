#! /usr/bin/python3
# gui.py

# Author: justcats12

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from classes import Event, Battle, Competitor, DNF



# constants
BUTTON_WIDTH = 25
SCREEN_GEOMETRY = "600x600"

# main window
root = tk.Tk()
root.title('cubeChamp')
root.geometry(SCREEN_GEOMETRY)

#
# Error message
#
def showError(title : str = "Error", description : str = "Unknown error occured"):
   messagebox.showerror(title, "Error: " + description)

#
# Homescreen
#
def homeScreen():
    home = tk.Frame(root)

    # moving functions
    def goNewEvent():
        home.destroy()
        newEventScreen().pack()
    def goLoadEvent():
        home.destroy()
        loadFromFileScreen().pack()

    # initialize elements
    homeLabel = tk.Label(home,  text="Home", padx=100)

    newEventButton = tk.Button(home, text="New event", width=BUTTON_WIDTH, command=goNewEvent)
    loadEventButton = tk.Button(home, text="Load event from file", width=BUTTON_WIDTH, command=goLoadEvent)

    quitButton = tk.Button(home, text='Quit', width=BUTTON_WIDTH, command=root.destroy)

    # pack elements
    homeLabel.pack()
    newEventButton.pack()
    loadEventButton.pack()
    quitButton.pack()

    return home


#
# New event Screen
#
def newEventScreen():
    newEvent = tk.Frame(root)

    # moving functions
    def goToCompetitorEntry():
        eventName = nameEntry.get()
        if eventName == None or eventName == "":
            showError("No event name", "Please input a name for the event")
        else:
            newEvent.destroy()
            competitorEntryScreen(eventName).pack()
    
    def goBack():
        newEvent.destroy()
        homeScreen().pack()
        

    # initialize elements
    newEventLabel = tk.Label(newEvent,  text="Create new event", padx=100)
    enterNameLabel = tk.Label(newEvent, text="Event name:")

    nameEntry = tk.Entry(newEvent)

    submitButton = tk.Button(newEvent, text="Submit", width=BUTTON_WIDTH, command=goToCompetitorEntry)
    backButton = tk.Button(newEvent, text="Back", width=BUTTON_WIDTH, command=goBack)

    # pack elements
    newEventLabel.pack()
    enterNameLabel.pack()
    nameEntry.pack()
    submitButton.pack()
    backButton.pack()
    
    return newEvent

#
# Load from file screen
#
def loadFromFileScreen():
    loadEvent = tk.Frame(root)

    # moving functions
    def submit():
        fileName = nameEntry.get()
        
        try:
            eventHomeScreen(event=Event(file=fileName)).pack()
            loadEvent.destroy()
        except:
            showError("File not found", "Could not find the file to the given path")
        
        
    
    def goBack():
        loadEvent.destroy()
        homeScreen().pack()

    # initialize elements
    newEventLabel = tk.Label(loadEvent,  text="Load event from file", padx=100)
    enterNameLabel = tk.Label(loadEvent, text="File path:")

    nameEntry = tk.Entry(loadEvent)

    submitButton = tk.Button(loadEvent, text="Submit", width=BUTTON_WIDTH, command=submit)

    backButton = tk.Button(loadEvent, text="Back", width=BUTTON_WIDTH, command=goBack)

    # pack elements
    newEventLabel.pack()
    enterNameLabel.pack()
    nameEntry.pack()
    submitButton.pack()
    backButton.pack()
    
    return loadEvent


#
# enterplayername
#
def competitorEntryScreen(eventName : str, pCompetitors = []):
    competitorEntry = tk.Frame(root)
    # moving functions
    def addCompetitor():
        compName = nameEntry.get()
        if compName == None or len(compName) < 2:
            showError("Invalid competitor name", "Please input a name longer of 2 characters or longer")
        else:
            competitors = pCompetitors + [compName]
            competitorEntry.destroy()
            competitorEntryScreen(eventName, competitors).pack()
        
    def startEvent():
        try:
            competitors =  [Competitor(n) for n in pCompetitors]
            if len(competitors) < 2:
                showError("Not enough competitors", "There have to be at least 2 competitors")
            else:
                e = Event(eventName, competitors=competitors)
                competitorEntry.destroy()
                eventHomeScreen(e).pack()
        except:
            showError("Something went wrong", "Cloud not start event, please restart and try again")

    def goHome():
        competitorEntry.destroy()
        homeScreen().pack()

    # initialize elements
    addCompetitorLabel = tk.Label(competitorEntry,  text=f"Add competitor {len(pCompetitors)+1} for {eventName}", padx=100)
    enterNameLabel = tk.Label(competitorEntry, text="Competitor name:")

    nameEntry = tk.Entry(competitorEntry)

    addCompetitorButton = tk.Button(competitorEntry, text="Add competitor", width=BUTTON_WIDTH, command=addCompetitor)
    doneButton = tk.Button(competitorEntry, text="Done", width=BUTTON_WIDTH, command=startEvent)

    listFrame = tk.Frame(competitorEntry)
    scrollbar = tk.Scrollbar(listFrame)
    
    competitorList = tk.Listbox(listFrame, yscrollcommand=scrollbar.set)

    for competitor in pCompetitors:
        competitorList.insert(tk.END, competitor)
        
    cancelButton = tk.Button(competitorEntry, text="Cancel", width=BUTTON_WIDTH, command=goHome)

    # pack elements
    addCompetitorLabel.pack()
    enterNameLabel.pack()
    nameEntry.pack()
    addCompetitorButton.pack()
    doneButton.pack()
    competitorList.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listFrame.pack()
    # config scrollbar
    scrollbar.config(command=competitorList.yview)
    cancelButton.pack()

    return competitorEntry
#
# Event homescreen
#


def eventHomeScreen(event : Event):
    eventHome = tk.Frame(root)
    # sort competitors
    event.sortCompetitorsByRank()
    # moving functions
    def startBattles():
        e = event
        try:
            p = int(pointsEntry.get())
            eventHome.destroy()
            e.startRound(scoreToWin=p)
            battleSummaryScreen(e).pack()
        except:
            showError("Invalid points to win", "Please input a number in the points to win entry")
    
    def saveAndQuit():
        fileName = enterFileName.get()
        if fileName == None or fileName == "":
            showError("Invalid filename", "Please input a filename")
        else:
            try:
                event.saveToFile(fileName)
                eventHome.destroy()
                homeScreen().pack()
            except:
                showError("Could not save", "Could not save file, please double check the path")

    # initialize elements
    eventHomeLabel = tk.Label(eventHome,  text=f"Event {event.name}", padx=100)

    # ranking
    rankingLabel = tk.Label(eventHome, text="Current Ranking")

    listFrame = tk.Frame(eventHome)
    scrollbar = tk.Scrollbar(listFrame)
    
    competitorList = tk.Listbox(listFrame, yscrollcommand=scrollbar.set, width=60)

    for i in range(len(event.competitors)):
        cCompetitor = event.competitors[i]
        competitorList.insert(tk.END, f'{i+1}) {cCompetitor.name}: {cCompetitor.wins} wins ({round(cCompetitor.getMean(), 2)})')

    # points to win
    pointsLabel = tk.Label(eventHome, text="Insert points to win")
    pointsEntry = tk.Entry(eventHome)
    pointsEntry.insert(0, "3")

    # buttons
    startBattlesButton = tk.Button(eventHome, text='Start battles', width=BUTTON_WIDTH, command=startBattles)

    fileNameLabel = tk.Label(eventHome, text="Input file name")
    enterFileName = tk.Entry(eventHome)
    enterFileName.insert(0, f"events/{event.name}.event")
    saveandQuitButton = tk.Button(eventHome, text='Save and go home', width=BUTTON_WIDTH, command=saveAndQuit)

    homeAndDiscardButton = tk.Button(eventHome, text='Go home and discard', width=BUTTON_WIDTH, command= lambda : eventHome.destroy() or homeScreen().pack())

    # pack elements
    eventHomeLabel.pack()
    


    rankingLabel.pack()
    competitorList.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listFrame.pack()

    pointsLabel.pack()
    pointsEntry.pack()

    startBattlesButton.pack()

    fileNameLabel.pack()
    enterFileName.pack()
    saveandQuitButton.pack()
    homeAndDiscardButton.pack()

    return eventHome

#
# Battles summary screen
#

def battleSummaryScreen(event : Event):
    battleSummary = tk.Frame(root)
    
    # get battling lists
    battles = event.battles
    battleStrings = [str(b) for b in battles]
    
    # battle selecting 
    selectedBattle = [battleFocusScreen(battles[0], battleSummary, lambda : updateFrame())]
    
    def on_select(event):
        selected_item = combo_box.get()
        index = battleStrings.index(selected_item)
        b = battles[index]

        selectedBattle[0].destroy()
        selectedBattle.pop()
        selectedBattle.append(battleFocusScreen(b, battleSummary, lambda : updateFrame()))
        selectedBattle[0].pack()
        

    def updateFrame():
        if all([b.hasWinner() for b in battles]):
            endButton.config(state=tk.NORMAL)
        on_select(None)

    def endBattles():
        event.endRound()
        battleSummary.destroy()
        eventHomeScreen(event=event).pack()
    
    # initialize elements
    battleSummaryLabel = tk.Label(battleSummary,  text=f"Event {event.name} battles", padx=100)
    

    # combo box for selecting battles
    combo_box = ttk.Combobox(battleSummary, values=battleStrings, width=200)
    combo_box.set(battleStrings[0])

    # button for ending the battles
    endButton = tk.Button(battleSummary, text='End battles', width=BUTTON_WIDTH, state=tk.DISABLED, pady=10, command=endBattles) 


    # pack elements
    battleSummaryLabel.pack()
    combo_box.pack()
    endButton.pack()
    selectedBattle[0].pack()
   

    # config
    combo_box.bind("<<ComboboxSelected>>", on_select)


    return battleSummary


#
# Battle focus screen
#
def battleFocusScreen(battle : Battle, root=root, updateFunction = None):
    battleFocus = tk.Frame(root)

    # submit time function
    def submitTime():
        userInput = timeInput.get()
        if userInput.upper() == "DNF":
            userInput = DNF
        try:
            userInput = float(userInput)

            battle.playTurn(userInput)
            updateFunction()
        except:
            showError("Invalid time", "Please input a float")
    # if there is a winner
    if battle.hasWinner():
        battleWonLabel = tk.Label(battleFocus, text=f"{battle.getWinner().name} won this battle")

        battleWonLabel.pack()
        return battleFocus


    # no winner
    # initialize elements
    battleFocusLabel = tk.Label(battleFocus,  text=f"{str(battle)}", padx=100)
    battleRoundLabel = tk.Label(battleFocus, text=f"Round {battle.round}", pady=10)
    # display score element
    scoreString = f"Scores: {" -- ".join([f'{battle.competitors[c].name}: {battle.scores[c]}' for c in range(len(battle.competitors))])}"
    battleScoreLabel = tk.Label(battleFocus, text=scoreString)

    # time input
    timeInputLabel = tk.Label(battleFocus, text=f"Input time for {battle.getCurrentCompetitor().name}:")
    timeInput = tk.Entry(battleFocus)

    # submit button, disable if there is a winner
    submitButton = tk.Button(battleFocus, text='Submit time', width=BUTTON_WIDTH, state={True: tk.DISABLED, False: tk.NORMAL}[battle.hasWinner()], command=submitTime)

    # previous times:
    previousTimesString = f"Previous: {', '.join([f'{battle.competitors[i].name}: {battle.solvesThisRound[i]}' for i in range(len(battle.solvesThisRound))])}"
    previousTimesLabel = tk.Label(battleFocus, text=previousTimesString)

    # pack elements
    battleFocusLabel.pack()
    battleRoundLabel.pack()
    battleScoreLabel.pack()
    timeInputLabel.pack()
    timeInput.pack()
    submitButton.pack()
    previousTimesLabel.pack()

    
    return battleFocus


# startup code
homeScreen().pack()
root.mainloop()