#! /usr/bin/python3
# classes.py

# Author: justcats12

#############
# VARIABLES #
#############

DNF = -1

####################
# Competitor class #
####################

class Competitor():
    def __init__(self, name : str, solves = [], competed = [], wins = 0):
        # initate class with name, no solves and no wins
        self.name : str = name
        self.solves : list = solves.copy()
        self.wins : int = wins
        # set to check who competitor already competed with
        self.competed : list = competed.copy()
    
    def __str__(self):
        # tostring
        # make the s dissapear if there is only one win
        s = ["s", ""][int(self.wins == 1)]
        
        # check if mean is DNF and set it to the word if it is
        mean = round(self.getMean(),2)
        if mean == DNF:
            mean = "DNF"
        # return a readable string with valuable information for humans
        return f"Competitor {self.name} with {self.wins} win{s} and a mean of {mean}"
    
    def __repr__(self):
        return f"Competitor(name={self.name}, wins={self.wins}, solves={self.solves}, competed={self.competed})"
    
    def getMean(self):
        """Get the mean of the solves of the cuber"""
        if len(self.solves) == 0:
            return DNF
        meanList = []
        # get the worst time of the solves
        worstTime = max(self.solves)
        # replace the DNFs with the worst time of the solves
        for solve in self.solves:
            if solve == DNF:
                meanList.append(worstTime)
            else:
                meanList.append(solve)
        # return the mean of meanList
        return sum(meanList)/len(meanList)

    def __eq__(self, other):
        """Competitors are the same if they have the same name, when signing up please use distinct names"""
        return self.name == other.name

    def __lt__(self, other):
        # compare function
        if self.wins != other.wins:
            return self.wins < other.wins
        # always less then when average is DNF
        if self.getMean() == DNF:
            return True
        # else compare mean
        return self.getMean() > other.getMean()
    
    def addsolve(self, time: float):
        """Add a solve to the competitor's solves"""
        # check if solve is DNF
        if time == DNF:
            self.solves.append(DNF)
        # add time if positive
        elif time >= 0:
            self.solves.append(time)
        # throw exception if negative
        else:
            raise Exception("Time must either be -1 for DNF or a positive number")
    
    def removeSolve(self, time: float):
        """Remove a solve from the competitor's solves"""
        if time not in self.solves:
            raise Exception("Competitor does not have this time in their solves")
        
        self.solves.remove(time)
    
    def win(self, amount = 1):
        """Give the competitor a win"""
        self.wins += amount
    
    def addCompeted(self, clist : list):
        """ add user to the competed with of the user"""
        for c in clist:
            # checks if the competitor itself is in the list
            if c.name != self.name:
                #print(self.name, c.name)
                self.competed.append(c.name)


    
# LACK OF COMPETITOR
LOC = Competitor("No competitor", solves=[DNF], wins=-99)
"""
Lack of competitor (LOC) is an artificial competitor added when there is an uneven amount of competitors. \n
They do a DNF every turn automatically.
The competitor who plays against LOC is allowed 3 solves to improve/set their mean
"""
    
################
# Battle class #
################

class Battle():
    def __init__(self, competitors : list[Competitor], scoreToWin = 3):

        # set the competitor list
        self.competitors = competitors
        # give each competitor a score of 0
        self.scores = [0 for _ in competitors]
        # set the score needed to win
        self.scoreToWin = scoreToWin
        # set turn on 0 and the list of times to an empty list
        self.turn = 0
        self.solvesThisRound = []

        # start at round 1
        self.round = 1

        # add competitors to eachother's competing list
        for c in competitors:
            c.addCompeted(competitors)
    def __str__(self):
        return f"Battle between {" and ".join([c.name for c in self.competitors])}"
    def __repr__(self):
        return f"Battle(competitors={self.competitors}, scores={self.scores}, scoreToWin={self.scoreToWin}, round={self.round})"

    def nextRound(self):
        """End the current round and go the next"""
        # determine winner
        
        # if everyone DNFed continue to the next round
        if not all([i == DNF for i in self.solvesThisRound]):

            # get the best time that is not a DNF
            bestTimeFindingList = self.solvesThisRound.copy()
            while DNF in bestTimeFindingList:
                bestTimeFindingList.remove(DNF)
            bestTime = min(bestTimeFindingList)

            # check every competitor if they got the best time (assumes there's no duplicates)
            for i in range(len(self.solvesThisRound)):
                if self.solvesThisRound[i] == bestTime:
                    self.scores[i] += 1
                    break

        # check if there's a winner and let them win
        if self.hasWinner():
            self.getWinner().win()
        else:
        # else resets the round
            self.round += 1
            self.turn = 0
            self.solvesThisRound = []
    
    def hasWinner(self):
        """Returns True if there is a winner"""
        return self.scoreToWin in self.scores
    def getWinner(self):
        """ Return the winner if there is one, throws exception otherwise"""
        for i in range(len(self.competitors)):
            if self.scores[i] >= self.scoreToWin:
                return self.competitors[i]
        
        raise Exception(f"Could not find a winner in round {self.round}")
    
    def getCurrentCompetitor(self):
        """Returns the competitor who's turn it is"""
        return self.competitors[self.turn]

    def playTurn(self, time : float):
        """Sets the time by the current competitor and goes to the next turn. \n
        If this was the last turn it resets the round"""
        
        # check for LOC:
        if self.getCurrentCompetitor() == LOC:
            self.solvesThisRound.append(DNF)
        else:
        # add the time to the competitor's solve and to the times in the current round
            self.getCurrentCompetitor().addsolve(time)
            self.solvesThisRound.append(time)

        # go to the next turn or next round if this was the last turn
        self.turn += 1
        if self.turn >= len(self.competitors):
            self.nextRound()
        

    
###############
# Event class #
###############

class Event():
    def __init__(self, name : str = "",competitors : list[Competitor] = [], file : str = None):
        
        # if not loaded from file the name and competitors
        self.name = name
        self.competitors :  list[Competitor] = competitors.copy()
        # add LOC if odd amount of competitors
        if len(self.competitors)%2 != 0:
            self.competitors.append(LOC)
        # start on round 1
        self.round = 1

        # list used for matchups
        self.matchups = []
        self.battles : list[Battle]= []

        # if file was given load from file instead
        if file != None:
            self.loadFromFile(file)
    def __str__(self):
        return f"Event {self.name} at round {self.round} with competitors: {', '.join([c.name for c in self.competitors])}"
    #
    # Saving and loading
    #
    def loadFromFile(self, fileName : str):
        """Load the event from a file"""

        # open the file and read the lines into "file"
        f = open(fileName, 'r')
        file = f.readlines()
        f.close()
        # check if file is long enough
        assert len(file) >= 4, "The given file is unreadable"
        
        # get the name
        self.name = file[0].strip().split("=")[1]
        # get the round
        self.round = int(file[1].strip().split("=")[1])

        # get the competitors
        for c in file[3:]:
            # split the parts of the line
            splits = c.strip().split(":")
            # get name and solves
            compName = splits[0]
                #check if there are any
            if splits[1] != "":
                solves = [float(i) for i in splits[1].split(" ")]
            else:
                solves = []

            if splits[2] != "":
                compCompeted = splits[2].split("%%")
            else:
                compCompeted = []
            
            wins = int(splits[3])
            # add them to the list
            self.competitors.append(Competitor(compName, solves=solves, competed=compCompeted, wins=wins))

    def saveToFile(self, fileName : str):
        """Save the event to the given filename"""
        # set up the lines
        # start with an empty list
        lines = []
        # add name and round
        lines.append(f"NAME={self.name}")
        lines.append(f"ROUND={self.round}")

        # add competitors
        lines.append("COMPETITORS")

        for c in self.competitors:
            # get solves as string, seperated by spaces
            solvesAsString = " ".join([str(i) for i in c.solves])
            competedAsString= "%%".join([str(i) for i in c.competed])
            # add the name and solves to the list (to write to the file)
            lines.append(f"{c.name}:{solvesAsString}:{competedAsString}:{c.wins}")

        # add newlines to each line
        lines = [i + "\n" for i in lines]
        # open file writing mode and write the lines
        f = open(fileName, 'w')
        f.writelines(lines)
        f.close()
    #
    # Matchmaking
    #
    def sortCompetitorsByRank(self):
        """Sort competitors by how good they are, first by amount of wins (more wins = better) and then by their mean (lower mean = better)"""
        # best person will be first in the list
        self.competitors.sort(reverse=True)
    
    def createMatchups(self, sortFirst = True):
        """Create match ups based on the order of the competitors list
        
        Sorts the competitors by their wins and mean unless sortFirst is set to False"""
        if sortFirst:

        # sort competitors
            self.sortCompetitorsByRank()
        # set to see who's already been matched up
        taken = []
        # go over competitors from the start
        for i in range(len(self.competitors)):
            c1 = self.competitors[i]
            # check if competitor is matched up already, if so continue
            if c1.name in taken:
                continue
            # break at last competitor
            if i == len(self.competitors) -1:
                break
            # check if competitor has competed against the next
            for j in range(i+1, len(self.competitors)):
                c2 = self.competitors[j]
                # check if c2 is taken
                if c2.name in taken:
                    continue
                # if yes, move on to the next
                if c2.name in c1.competed:
                    continue
                # if none of the above conditions are true match them up
                self.matchups.append([c1, c2])
                taken += [c1.name, c2.name]
                break
        
        if len(self.competitors) == len(taken):
            return
        
        # if not everyone has found a competitor repeat the process for everyone who isn't competing yet and match them up with the next unconditionally
        for i in range(len(self.competitors)):
            
            c1 = self.competitors[i]
            # check if competitor is matched up already, if so continue
            if c1.name in taken:
                continue
            # check if competitor has competed against the next
            for j in range(i+1, len(self.competitors)):
                c2 = self.competitors[j]
                # check if c2 is taken
                if c2.name in taken:
                    continue
                # if none of the above conditions are true match them up
                self.matchups.append([c1, c2])
                taken += [c1.name, c2.name]
                break

    def startRound(self, doMatchups = True, scoreToWin=3):
        """
        Creates matchups and creates a new battle for every matchup that is stored in the battles list
        
        You can set doMatchups to False to not do the matchups, so you can do them yourself and alter them if you need to.

        The score to win is 3 by default but can be altered by setting scoreToWin
        """
        # check if previous round has ended
        if len(self.battles) > 0:
            raise Exception("Previous round hasn't ended")
        
        if doMatchups:
            self.createMatchups()

        # make a battle for every matchup
        for m in self.matchups:
            self.battles.append(Battle(m, scoreToWin=scoreToWin))
    
    def endRound(self, forced = False):
        """
        Checks if all battles have a winner and clears out the battle list

        You can override the check for winners by setting forced to True
        """
        # if not every battle has ended throw exception, unless forced:
        if (not all([b.hasWinner() for b in self.battles])) and (not forced):
            raise Exception("The round is still ongoing")
        # clear out the battles & matchups
        self.battles = []
        self.matchups = []
        # continue to next round
        self.round += 1
    
    

# TESTCODE
"""
e = Event(file="example.event")

print(e.name, e.round, e.competitors)
e.saveToFile("alex.event")"""
"""
c1 = Competitor("Click")
c2 = Competitor("Alex")
c3 = Competitor("Jaice")

c2.win()
c3.win()

c2.addsolve(50)
c3.addsolve(15)

e = Event("3x3", [c2, c3, c1])

e.createMatchups()
e.startRound()

print([str(i) for i in e.battles], e.battles[0].hasWinner())

e.endRound(forced=True)
print([str(i) for i in e.battles])
"""