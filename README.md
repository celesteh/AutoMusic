<h1>AutoMusic - Invading the Realm of the Arts</h1>
<b>Software Design Final Project</b>
<b>April 28, 2010</b>
Shane Moon, Jeffrey Atkinson, Rui Wang, Thomas Lamar
=========

<b>Guide to installing and running code</b>

<p>
Table of Contents:
1. Folders
2. Instructions on running code
3. Necessary files
4. Instructions on reading code
</p>

<p>
<b>1. Folders</b>
- All files are packaged into FinalCode.tar.gz
- Root: contains all files for running code
- Input Midis: contains sample Midi files
- Output MIDIs: where Midi files are written to by the program
</p>

<p>
<b>2. Instructions on running code</b>
- From the directory, run python Main.py
- Follow all links to try functions
- Add your own Midi files to /Input Midis optionally
</p>

<p>
<b>3. Necessary files</b>
- List of necessary packages
 - PIL: python-imaging-tk
 - Pygame

- List of necessary modules
 - math
 - random
 - string
 - struct
 - sys
 - tkFileDialog
 - tkFont
 - Tkinter
 - PIL
 - pygame

- List of python files written by the team
 - <b>Note.py</b>: Defines the Note class, stores a musical pitch
 - <b>Chord.py</b>: Defines the Chord class, stores a list of Notes and duration
 - <b>Song.py</b>: Defines the Song class, stores a list of Chords and peripheral information
 - <b>AutoComposeSong.py</b>: Inherits from Song, adds methods for compostion from music theory
 - <b>MarkovSong.py</b>: Inherits from Song, adds methods for Markov generation
 - <b>Main.py</b>: Main GUI, serves as controller and view
 - <b>convertNote.py</b>: Converts Notes into format used by MusicalCanvas5
 - <b>MusicalCanvas5.py</b>: Inherits from Tk Canvas, adds methods for drawing Songs, Chords, and Notes
 - <b>musicGeneration.py</b>: Provides methods for randomly generating pitch and duration for Notes

- List of other python files used unchanged or slightly modified
 - constants.py
 - DataTypeConverters.py
 - EventDispatcher.py
 - MidiInStream.py
 - MidiOutFile.py
 - MidiOutStream.py
 - modified_MidiFileParser.py
 - modified_MidiInFile.py
 - modified_MidiToText.py
 - RawInStreamFile.py
 - RawOutStreamFile.py

- List of additional files utilized
 - Music.bmp
 - Music_fade.bmp
 - generate.bmp
 - logo.bmp
</p>

<p>
<b>4. Instructions on reading the code</b>

- First, read through our class files (Note, Chord, Song, AutoComposeSong, MarkovSong) using musicGeneration and MusicalReference as references.

- Then, read Main referencing convertNote and MusicalCanvas5 when necessary.

- All other files can be referenced if their use in the code is unclear. Note that a header comment could not be included for DataTypeConverters, so a txt file is included in the folder as a comment.
</p>
