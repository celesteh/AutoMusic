# Authors: Shane Moon, Jeffrey Atkinson
# Software Design
# InvadingTheRealmOfTheArts
# April 28, 2010
# File: Song.py
# Defines the Song class, stores a list of Chords and peripheral information

from Chord import *

class Song:

    def __init__(self, title = 'Untitled', chords = []):
        """
            title   :  title of the song <str>
            chords  :  <list> of <Chord>s
        """
        self.title = title
        self.chords = chords


    def __str__(self):
        s = "Song <" + self.getTitle() + \
                   "> composed of following chords: " + "\n"
        for chord in self.chords:
            s = s + "time: " + str(chord.getTime()) + ', ' + \
                    "notes: " + str(chord.getNotesAsInts()) + '\n'
        return s


    def sort(self):
        """
            Sort the song by the time at which chords are played.
            It uses Insertion Sort mechanism.
        """
        
        for i in range(1, len(self.chords)):
            j = i
            while(j >= 1 and self.chords[j-1].time > self.chords[j].time):
                temp_chord = self.chords[j]
                self.chords[j] = self.chords[j-1]
                self.chords[j-1] = temp_chord
                j -= 1


    def getTitle(self):         return self.title                
    def getChords(self):        return self.chords


    def setTitle(self, title = ''):
        self.title = title

        
    def setChords(self, chords = None):
        self.chords = chords

    def reset(self):
        self.setTitle('Untitled')
        self.setChords([])


    def findChord(self, time):
        """ Return <Chord> played at the given <time> """
        for chord in self.chords:
            if chord.getTime() == time: return chord
        return Chord([], time)


    def addChord(self, chord):
        """
            Add <Chord> to a <Song>. If <Song> previously has a
            <Chord> at which the input <Chord> is played,
            it adds <Note>s to that <Chord>.
        """
        if self.hasTime(chord.time):
            self.findChord(chord.time).addNote(chord.Notes)
        else: self.chords.append(chord)


    def addChords(self, chords):
        """ Add multiple <Chord>s to a <Song> """
        for chord in chords:
            self.addChord(chord)


    def appendChords(self, chords):
        """ Append multiple <Chord>s to a <Song> """
        self.sort()
        time_end = self.chords[len(self.chords)-1].time
        for chord in chords:
            chord.setTime(chord.getTime() + time_end)
            self.addChord(chord)


    def replaceChords(self, song):
        """
            Replace 'chords' of a self object to the 'chords' of
            the input song, if 'time' of the self object conflicts.
        """

        for chord in song.getChords():
            if self.hasTime(chord.getTime()) == True:
                self.findChord(chord.getTime()).replaceChord(chord)
            else:
                self.addChord(chord)
        

    def hasTime(self, time = 0):
        """ return whether a song has any <Chord> at a given <time> """
        if self.chords == []: return False

        for chord in self.chords:
            if chord.getTime() == time: return True
        return False


    def shiftTimes(self, time):
        """ Shift 'time's of the <Chord>s by the input 'time' """
        for chord in self.chords:
            chord.time += time

    
    def wrapNotesAndTimes(self, Notes = [], times = []):
        """
            (Massive) Wrapper Method
            - Wrap a <list> of <Note>s and <list> of <time>s,
              and return a <list> of <Chord>s.
            - Every <Chord> gets only one <Note> and <time>,
            - 'Notes' and 'times' are assumed to have the same length
        """
        if len(Notes) != len(times): raise IndexError
        chords = []

        for i in range(len(Notes)):
            chords.append(Chord([Notes[i]], times[i]))
        self.addChords(chords)

    def importMidi(self, inFile):
        """
            Import the input MIDI file, and convert it to a
            <Song> object.
        """
        midiText = MidiInFile(MidiToText(), inFile)
        textNotes = midiText.read().replace('None', ' ').split()
        
        Notes = []
        
        for note in textNotes:
            Notes.append(int(note))
            
        Notes = wrapNote(Notes)
        times = constant_times(Notes, 2, 48)
        
        self.wrapNotesAndTimes(Notes, times)
        

    def exportMidi(self, channel, outFile, beat = 24):
        """
            Export the input <Song> to MIDI file,
            on 'channel' <int>, named as 'outFile' <str>
        """
        
        midi = MidiOutFile(str(outFile))
        midi.header(0)
        midi.start_of_track()
        midi.tempo(750000)
        midi.time_signature(4, 2, beat, 8)

        self.writeMidi(midi, channel)
        
        midi.update_time(0)
        midi.end_of_track()

        midi.eof()


    def writeMidi(self, midi, channel):
        """ Write a midi file, based on the input 'chords' """
        
        self.sort()
        
        for i in range(len(self.getChords()) - 1):
            
            midi.update_time(0)
            for note in self.chords[i].getNotes():
                midi.note_on(channel, note = int(note.getPitch()))

            midi.update_time((self.chords[i+1].getTime() -      \
                              self.chords[i].getTime()) /       \
                              len(self.chords[i].getNotes()))
            for note in self.chords[i].getNotes():
                midi.note_off(channel, note = int(note.getPitch()))
        

if __name__ == '__main__':
    """
        song = Song('Test Song')

        # One example way of appending a <Song>
        notes = wrapNote([50, 51, 52, 53])
        times = [10, 0, 30, 20]
        song.wrapNotesAndTimes(notes, times)

        # Another example of appending a <Song>
        chords = [Chord([Note(50)], 0), Chord([Note(72), Note(44)], 10)]
        song.addChords(chords)
        song.sort()
        song.exportMidi(1, 'TEST.mid')

        song = Song()
        song.importMidi("river flows in you.mid")
        print song
        song.exportMidi(1, "exported song.mid")
    """
    pass
