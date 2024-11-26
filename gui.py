#! /usr/bin/python3
# gui.py

# Author: justcats12

import tkinter as tk

# main window
root = tk.Tk()
root.title('cubeChamp')
root.geometry("600x400")


#
# Homescreen
#
def homeScreen():
    home = tk.Frame(root)

    # moving functions
    def goNewEvent():
        home.destroy()
        newEventScreen().pack()

    # initialize elements
    homeLabel = tk.Label(home,  text="Home", padx=100)

    newEventButton = tk.Button(home, text="New event", width=25, command=goNewEvent)
    loadEventButton = tk.Button(home, text="Load event from file", width=25)

    quitButton = tk.Button(home, text='Quit', width=25, command=root.destroy)

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
        newEvent.destroy()
        competitorEntryScreen(eventName).pack()
        

    # initialize elements
    newEventLabel = tk.Label(newEvent,  text="Create new event", padx=100)
    enterNameLabel = tk.Label(newEvent, text="Event name:")

    nameEntry = tk.Entry(newEvent)

    submitButton = tk.Button(newEvent, text="Submit", width=25, command=goToCompetitorEntry)

    # pack elements
    newEventLabel.pack()
    enterNameLabel.pack()
    nameEntry.pack()
    submitButton.pack()
    
    return newEvent

#
# enterplayername
#
def competitorEntryScreen(eventName : str, pCompetitors = []):
    competitorEntry = tk.Frame(root)
    # moving functions
    def addCompetitor():
        
        competitors = pCompetitors + [nameEntry.get()]
        competitorEntry.destroy()
        competitorEntryScreen(eventName, competitors).pack()

    # initialize elements
    addCompetitorLabel = tk.Label(competitorEntry,  text=f"Add competitor {len(pCompetitors)+1} for {eventName}", padx=100)
    enterNameLabel = tk.Label(competitorEntry, text="Competitor name:")

    nameEntry = tk.Entry(competitorEntry)

    addCompetitorButton = tk.Button(competitorEntry, text="Add competitor", width=25, command=addCompetitor)
    doneButton = tk.Button(competitorEntry, text="Done", width=25)

    listFrame = tk.Frame(competitorEntry)
    scrollbar = tk.Scrollbar(listFrame)
    
    competitorList = tk.Listbox(listFrame, yscrollcommand=scrollbar.set)

    for competitor in pCompetitors:
        competitorList.insert(tk.END, competitor)
        
    

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

    return competitorEntry


# startup code
homeScreen().pack()
root.mainloop()