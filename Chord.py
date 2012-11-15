# Authors: Shane Moon
# Software Design
# InvadingTheRealmOfTheArts
# April 28, 2010
# File: Chord.py
# Defines the Chord class, stores a list of Notes and duration

from Note import *

class Chord:
    def __init__(self, Notes = [], time = 0):
        """
            Notes :  <list> of <Note>s
            time  :  <int> time at which Notes are played
        """
        
        self.Notes = Notes
        self.time = time

    def __str__(self):
        s = "Chord played at time %d with notes: " % (self.time)
        for note in self.Notes:
            s = s + ('%s, ' % (note.__str__() ) )
        return s

    def getNotes(self):        return self.Notes
    def getTime(self):         return self.time

    def getNotesAsInts(self):
        
        l = []
        for note in self.Notes:
            l.append(note.getPitch())
        return l

    def setNotes(self, Notes = []):
        self.Notes = Notes

    def setTime(self, time = 0):
        self.time = time

    def addNote(self, notes):
        if type(notes) == list:
            for note in notes:
                self.Notes.append(note)
        else: self.Notes.append(notes)

    def addTime(self, time):
        self.time += time

    def replaceChord(self, chord):
        self.time = chord.time
        self.Notes = chord.Notes


if __name__ == '__main__':
    notes = [Note(50), Note(72), Note(44)]
    chord = Chord(notes, 100)
    chord.addNote([Note(200), Note(150)])
    
    print chord
    print chord.getNotes()
    print chord.getNotesAsInts()
