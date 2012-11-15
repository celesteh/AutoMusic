# Authors: Shane Moon, Jeffrey Atkinson, Tom Lamar
# Software Design
# InvadingTheRealmOfTheArts
# April 28, 2010
# File: Note.py
# Changelog: 
# updated 4/25 by Tom
# corrected bugs in __init__ and setRest
# Defines the Note class, stores a musical pitch

from MidiOutStream import MidiOutStream
from MidiOutFile import MidiOutFile
from modified_MidiToText import MidiToText
from modified_MidiInFile import MidiInFile

from RawOutstreamFile import RawOutstreamFile
from constants import *
from DataTypeConverters import fromBytes, writeVar
from MusicalReference import *
from musicGeneration import *

import sys
import random
import string

class Note:

    def __init__(self, pitch = 0, rest = False):
        """
            pitch :  <int> (0 - 127) that represents pitch of a note
            rest  :  <boolean> whether a note is rest or not.
        """
        self.pitch = pitch
        self.rest = rest

    def __str__(self):
        return "Pitch: %.d" %(self.pitch)
        
    def getPitch(self):       return self.pitch
    def getRest(self):        return self.rest

    def setPitch(self, pitch):
        self.pitch = pitch

    def setRest(self, rest = True):
        self.rest = rest

    def transpose(self, transpose = 0):
        """ Transpose the pitch of Note by the input interval, and return it """
        return Note(self.pitch + transpose)

    def octave(self, octave = 0):
        """ Transpose the pitch of Note by the input octave, and return it """
        return Note(self.pitch + octave * 12)

    def selectPitch(self, key, mode, Range = [0, 127]):
        """
            Randomly select a pitch of a Note, in the input 'key',
            among the input musical 'mode', within the input 'Range.'

            i.e. Lydian Mode in C Key is: [C, D, E, F, G, A, B]
                             in D Key is: [D, E, F#, G, A, B, C#]                             
        """
        pitchList = []
        
        for note in range(Range[0], Range[1]):
            if (note - key) % 12 in mode: pitchList.append(note)

        return Note(random.choice(pitchList))
	
	


def wrapNote(notes):
    """
        Wrapper method
        - converts <int>, <list> or <tuple> of <int>s to <Note> objects
    """
    if type(notes) == int:
        return Note(notes)
    
    elif type(notes) == list:
        Notes = []
        for note in notes:
            Notes.append(Note(note))
        return Notes

    elif type(notes) == tuple:
        Notes = ()
        for note in notes:
            Notes += (Note(note),)
        return Notes

    else: raise TypeError
	


if __name__ == '__main__':
    note = Note(60)
    print note.transpose(8)
    print note.getPitch()
