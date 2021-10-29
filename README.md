# Take Notes

Command Line notes manager powered by the `typer` python package. Also used `rich` to display tables in the command line.

## Quick Start

This package can be installed with pip by running `pip install .` in the project directory.  

With a successful install, the `notes` command will now be available. Type `notes` to begin and get prompted with following information:

<p align="center">
  <img src="images/notes-quick-start.png" height="350"/>
</p>

Create your first note and open:
```zsh
>>> notes create first-note
The note first-note was created.

>>> notes open first-note
💬 Opening first-note text file in vim
```

## File Management

All notes are stored as `.txt` files in the hidden `.notes` folder off of the home directory.


## TODO
- Allow do switch the editor (default is vim)
