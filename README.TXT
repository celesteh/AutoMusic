Invading the Realm of the Arts
Software Design Final Project
April 28, 2010
Shane Moon, Jeffrey Atkinson, Rui Wang, Thomas Lamar

Guide to installing and running code

Table of Contents:
1. Folders
2. Instructions on running code
3. Necessary files
4. Instructions on reading code

1. Folders
All files are packaged into FinalCode.tar.gz
Root: contains all files for running code
Input Midis: contains sample Midi files
Output MIDIs: where Midi files are written to by the program

2. Instructions on running code
-From the directory, run python Main.py
-Follow all links to try functions
-Add your own Midi files to /Input Midis optionally

3. Necessary files
-List of necessary packages
PIL: python-imaging-tk
Pygame

-List of necessary modules
math
random
string
struct
sys
tkFileDialog
tkFont
Tkinter
PIL
pygame

-List of python files written by the team
Note.py
- Defines the Note class, stores a musical pitch
Chord.py
- Defines the Chord class, stores a list of Notes and duration
Song.py
- Defines the Song class, stores a list of Chords and peripheral information
AutoComposeSong.py
- Inherits from Song, adds methods for compostion from music theory
MarkovSong.py
- Inherits from Song, adds methods for Markov generation
Main.py
- Main GUI, serves as controller and view
convertNote.py
- Converts Notes into format used by MusicalCanvas5
MusicalCanvas5.py
- Inherits from Tk Canvas, adds methods for drawing Songs, Chords, and Notes
musicGeneration.py
- Provides methods for randomly generating pitch and duration for Notes

-List of other python files used unchanged or slightly modified
constants.py
DataTypeConverters.py
EventDispatcher.py
MidiInStream.py
MidiOutFile.py
MidiOutStream.py
modified_MidiFileParser.py
modified_MidiInFile.py
modified_MidiToText.py
RawInStreamFile.py
RawOutStreamFile.py

-List of additional files utilized
Music.bmp
Music_fade.bmp
generate.bmp
logo.bmp

4. Instructions on reading the code

- First, read through our class files (Note, Chord, Song, AutoComposeSong, MarkovSong) using musicGeneration and MusicalReference as references.

- Then, read Main referencing convertNote and MusicalCanvas5 when necessary.

- All other files can be referenced if their use in the code is unclear. Note that a header comment could not be included for DataTypeConverters, so a txt file is included in the folder as a comment.
