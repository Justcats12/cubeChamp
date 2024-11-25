# cubeChamp

> THIS IS A WORK IN PROGRES, it remains unfinished

## Information
cubeChamp is a matchup tool for a new format for cubing competitions, putting cubers head to head based on their amount of wins and overall mean.

## File descriptions
Currently only 2 files exist:
1. **classes.py**: this is the workings of the system. It consists of 3 main classes
    1. Competitor: Stores the solves of a single competitor, as well as who they have battled against
    2. Battle: Keeps track of an ongoing battle and decides the winner
    3. Event: A loadable and savable class that keeps track of all competitors and is in charge of matching them up
2. **example.event**: is an example of how an event file would look