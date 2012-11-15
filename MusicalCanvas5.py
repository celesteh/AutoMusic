# Authors: Tom Lamar
# Software Design
# InvadingTheRealmOfTheArts
# April 28, 2010
# File: MusicalCanvas5.py
# Inherits from Tk Canvas, adds methods for drawing Songs, Chords, and Notes 

from Tkinter import *
from Song import *
from convertNote import *
import math

class MusicalCanvas(Canvas):
    def __init__(self, master, *args, **options):
        Canvas.__init__(self, master, *args, **options)
        self.xLeft = 0
        self.xRight = 400
        self.pixelsPerLetter = 4 #how many pixels E-F, for example
        self.trebleFLoc = -100 #will become positive before it is used
        self.xSpacing = 20
        self.maxXLoc = 350
        self.minXLoc = 20
        self.nextXLoc = self.maxXLoc + 1 #initial value should be invalid
        self.bigLineSpacing = 150 #spacing between big lines

    def addBigLine(self):
        y = self.trebleFLoc
        #draw treble staff
        for i in range(5):
            self.create_line(self.xLeft, y, self.xRight, y)
            y += 2 * self.pixelsPerLetter
        #skip space in middle
        for i in range(1):
            y += 2 * self.pixelsPerLetter
        #draw bass staff
        for i in range(5):
            self.create_line(self.xLeft, y, self.xRight, y)
            y += 2 * self.pixelsPerLetter
    
    def addSong(self, song):
        wholeNoteDur = 8*24 #default assumption
        chords = song.getChords()
        if isinstance(chords, Chord): #if just 1
            #we can't tell the length of the final chord
            #let's assume a whole note
            self.addChord(chords, 'w')
        elif type(chords) == list: #if a list of chords
            for i in range(len(chords)-1): #parse through all but the last
                chord = chords[i]
                timeDiff = chords[i+1].getTime() - chord.getTime()
                noteType = self.durationToNoteType(timeDiff, wholeNoteDur)
                self.addChord(chord, noteType)
            self.addChord(chords[-1], 'w')
    
    def durationToNoteType(self, duration, durationPerWholeNote):
        """
            Given the duration of a whole note
            return note type (i.e., quarter note)
        """
        ratio = durationPerWholeNote / 16.0
        index = round(math.log(duration/ratio, 2))
        if index < 0: #if less than 16th
            index = 0 #fail gracefully
            print 'Warning: note duration too small'
        if index > 4: #if longer than whole
            index = 4 #fail gracefully
            print 'Warning: note duration too big'
        listOfNoteTypes = ('s', 'e', 'q', 'h', 'w')
        return listOfNoteTypes[int(index)]

    def addChord(self, chord, noteType='q'):
        """
            add a Chord
            also makes sure there is enough space
        """
        notes = chord.getNotes()
        if isinstance(notes, Note): #if just a single note
            self.addNote(notes, noteType)
        elif type(notes) == list:
            for note in notes:
                self.addNote(note, noteType)
                self.nextXLoc -= self.xSpacing #cancel out movement
            self.nextXLoc += self.xSpacing #then actually advance
        else:
            raise TypeError

    def addNote(self, note, noteType='q'):
        if self.nextXLoc > self.maxXLoc:
            self.trebleFLoc += self.bigLineSpacing
            self.addBigLine()
            self.nextXLoc = self.minXLoc
        self.addNoteToStaff(note, noteType)

    def addNoteToStaff(self, note, noteType='q'):
        """
            Add a Note to the drawing
            y location based off of pitch
            x location is predetermined
            noteType is one of ['w', 'h', 'q', 'e', 's']
        """
        if note.getRest(): #if a rest
            if noteType == 'w': self.drawWholeRest(self.nextXLoc)
            if noteType == 'h': self.drawHalfRest(self.nextXLoc)
            if noteType == 'q': self.drawQuarterRest(self.nextXLoc)
            if noteType == 'e': self.drawEighthRest(self.nextXLoc)
            if noteType == 's': self.drawSixteenthRest(self.nextXLoc)
        else: #not a rest        
            (letter, mod, octave) = noteToLMO(note)
             #compare note to trebleHighF to determine offset
            noteOffset = ( ord(letter) - ord('F') ) + 7 * (octave - 5)
            #print noteOffset
            y = self.trebleFLoc - self.pixelsPerLetter * noteOffset

            if mod == 'sharp':
                self.drawSharp(self.nextXLoc - .5 * self.xSpacing, y)

            #draw appropriate graphic
            if noteType == 'w': self.drawWholeNote(self.nextXLoc, y)
            if noteType == 'h': self.drawHalfNote(self.nextXLoc, y)
            if noteType == 'q': self.drawQuarterNote(self.nextXLoc, y)
            if noteType == 'e': self.drawEighthNote(self.nextXLoc, y)
            if noteType == 's': self.drawSixteenthNote(self.nextXLoc, y)
        self.nextXLoc += self.xSpacing #advance to next position
    
    #drawing functions
    def drawWholeNote(self, centerX, centerY):
        #draw a whole note at specified location
        self.create_oval(centerX - 1*self.pixelsPerLetter,
                                centerY - 1*self.pixelsPerLetter,
                                centerX + 1*self.pixelsPerLetter,
                                centerY + 1*self.pixelsPerLetter,
                                fill = 'black')
        self.create_oval(centerX - .5*self.pixelsPerLetter,
                                centerY - .8*self.pixelsPerLetter,
                                centerX + .5*self.pixelsPerLetter,
                                centerY + .8*self.pixelsPerLetter,
                                fill = 'white')

    def drawHalfNote(self, centerX, centerY):
        #draw a half note at specified location
        self.create_oval(centerX - 1*self.pixelsPerLetter,
                                centerY - 1*self.pixelsPerLetter,
                                centerX + 1*self.pixelsPerLetter,
                                centerY + 1*self.pixelsPerLetter,
                                fill = 'white')
        self.create_line(centerX + 1 * self.pixelsPerLetter,
                                centerY,
                                centerX + 1 * self.pixelsPerLetter,
                                centerY - 5 * self.pixelsPerLetter)

    def drawQuarterNote(self, centerX, centerY):
        #draw a quarter note at specified location
        self.create_oval(centerX - 1*self.pixelsPerLetter,
                                centerY - 1*self.pixelsPerLetter,
                                centerX + 1*self.pixelsPerLetter,
                                centerY + 1*self.pixelsPerLetter,
                                fill = 'black')
        self.create_line(centerX + 1 * self.pixelsPerLetter,
                                centerY,
                                centerX + 1 * self.pixelsPerLetter,
                                centerY - 5 * self.pixelsPerLetter)
        
    
        
    def drawEighthNote(self, centerX, centerY):
        #draw an eigth note at specified location
        #it is a quarter note with a tail
        self.drawQuarterNote(centerX, centerY)
        self.create_line(centerX + 1 * self.pixelsPerLetter,
                                centerY - 5 * self.pixelsPerLetter,
                                centerX + 2 * self.pixelsPerLetter,
                                centerY - 3 * self.pixelsPerLetter)
                                
    def drawSixteenthNote(self, centerX, centerY):
        #draw a sixteenth note at specified location
        #it is an eigth note with another tail
        self.drawEigthNote(centerX, centerY)
        self.create_line(centerX + 1 * self.pixelsPerLetter,
                                centerY - 4 * self.pixelsPerLetter,
                                centerX + 2 * self.pixelsPerLetter,
                                centerY - 2 * self.pixelsPerLetter)


    def drawWholeRest(self, centerX):
        """
            Draws a whole rest hanging off of D5
        """
        yTop = self.trebleFLoc + 2 * self.pixelsPerLetter
        self.create_rectangle(centerX - 1 * self.pixelsPerLetter,
                                     yTop,
                                     centerX + 1 * self.pixelsPerLetter,
                                     yTop + 1 * self.pixelsPerLetter,
                                     fill='black')
        
    def drawHalfRest(self, centerX):
        """
            Draws a half rest on top of B5
        """
        yTop = self.trebleFLoc + 3 * self.pixelsPerLetter
        self.create_rectangle(centerX - 1 * self.pixelsPerLetter,
                                     yTop,
                                     centerX + 1 * self.pixelsPerLetter,
                                     yTop + 1 * self.pixelsPerLetter,
                                     fill='black')

    def drawQuarterRest(self, centerX):
        """
            Draws a quarter rest
        """
        print centerX
        yTop = self.trebleFLoc + 1 * self.pixelsPerLetter
        self.create_polygon(centerX - .5 * self.pixelsPerLetter,
                                   yTop,
                                   centerX + 1 * self.pixelsPerLetter,
                                   yTop + 2 * self.pixelsPerLetter,
                                   centerX - .5 * self.pixelsPerLetter,
                                   yTop + 4 * self.pixelsPerLetter,
                                   centerX + 1 * self.pixelsPerLetter,
                                   yTop + 6 * self.pixelsPerLetter)
        
    def drawEighthRest(self, centerX):
        """
            Draws an eigth rest
        """
        yTop = self.trebleFLoc + 2 *self.pixelsPerLetter #D5
        self.create_line(centerX + .5 * self.pixelsPerLetter,
                                yTop,
                                centerX - .5 * self.pixelsPerLetter,
                                yTop + 4 * self.pixelsPerLetter)
        self.create_oval(centerX - 1 * self.pixelsPerLetter,
                                yTop + .4 * self.pixelsPerLetter,
                                centerX - .2 * self.pixelsPerLetter,
                                yTop + 2 * self.pixelsPerLetter,
                                fill = 'black')

    def drawSixteenthRest(self, centerX):
        """
            Draws a sixteenth rest
        """
        yTop = self.trebleFLoc + 2 *self.pixelsPerLetter #D5
        self.create_line(centerX + .5 * self.pixelsPerLetter,
                                yTop,
                                centerX - .7 * self.pixelsPerLetter,
                                yTop + 6 * self.pixelsPerLetter)
        self.create_oval(centerX - 1 * self.pixelsPerLetter,
                                yTop + .4 * self.pixelsPerLetter,
                                centerX - .2 * self.pixelsPerLetter,
                                yTop + 2 * self.pixelsPerLetter,
                                fill = 'black')
        self.create_oval(centerX - 1.4 * self.pixelsPerLetter,
                                yTop + 2.4 * self.pixelsPerLetter,
                                centerX - .6 * self.pixelsPerLetter,
                                yTop + 4 * self.pixelsPerLetter,
                                fill = 'black')
    
    def drawSharp(self, centerX, centerY):
        #draw a sharp symbol at specified location
        self.create_line(centerX - .4 * self.pixelsPerLetter,
                                centerY - .7 * self.pixelsPerLetter,
                                centerX - .4 * self.pixelsPerLetter,
                                centerY + .7 * self.pixelsPerLetter)        
        self.create_line(centerX + .4 * self.pixelsPerLetter,
                                centerY - .7 * self.pixelsPerLetter,
                                centerX + .4 * self.pixelsPerLetter,
                                centerY + .7 * self.pixelsPerLetter)
        self.create_line(centerX - 1 * self.pixelsPerLetter,
                                centerY - .2 * self.pixelsPerLetter,
                                centerX + 1 * self.pixelsPerLetter,
                                centerY - .7 * self.pixelsPerLetter)
        self.create_line(centerX - 1 * self.pixelsPerLetter,
                                centerY + .4 * self.pixelsPerLetter,
                                centerX + 1 * self.pixelsPerLetter,
                                centerY + .1 * self.pixelsPerLetter)        

if __name__ == '__main__':

    master = Tk()
    frame = Frame(height=600, width=600)
    frame.pack()

    w = MusicalCanvas(frame, width=500, height=500, bg='white')
    w.pack()

    #w.drawQuarterNote(50, 50)
    #w.drawEighthNote(70, 50)
    #w.drawQuarterRest(90)

    notes = wrapNote([67, 71, 75])
    c1 = Chord([Note(72), Note(44)])
    for note in notes:
        w.addChord(Chord(note))
    for i in range(3):
        w.addChord(c1)
        

    mainloop()

