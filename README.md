# cubeChamp

VERSION: ALPHA 1.1

(THIS IS A WORK IN PROGRES, it remains unfinished)

## Information
cubeChamp is a matchup tool for a new format for cubing competitions, putting cubers head to head based on their amount of wins and overall mean.

It currently supports 1v1s and best of 5 battles, but the score needed to win can be altered. For example longer events would only need 2 points instead of 3.

It can also be used for 1v1v1s or 1v1v1v1s and so on, though the matchmaker does not (yet) support these formats, you can have competitors compete for a certain score.

cubeChamp does not have an internal scramble generator, to generate scramlbes for best of 5 or best of 3 it is recommended to use tNoodle.

The gui and cui currently only support best of 5, 1v1 battles.

### restrictions

The gui can only understand times in the format XXXX.XX and not XX:XX:XX.XX

## File descriptions
1. **classes.py**: this is the workings of the system. It consists of 3 main classes
    1. Competitor: Stores the solves of a single competitor, as well as who they have battled against
    2. Battle: Keeps track of an ongoing battle and decides the winner
    3. Event: A loadable and savable class that keeps track of all competitors and is in charge of matching them up
2. **example.event**: is an example of how an event file would look
3. **cui.py**: the comand user interface
4. **gui.py**: the graphical user interface

## Requirements:

- Python 3.12.7+
- tkinter (for gui)
## usage

Clone the repository and move into it
```
git clone https://github.com/Justcats12/cubeChamp
cd cubeChamp
```

### GUI
Run the gui file using python

```
python3 gui.py
```

### CUI
Run the cui file using python, it does not require tkinter
```
python3 cui.py
```

When you get a `> `-prompt, fill in the number corresponding to the option you want to do.
