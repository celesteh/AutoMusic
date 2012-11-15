# Authors: Shane Moon, Jeffrey Atkinson
# Software Design
# InvadingTheRealmOfTheArts
# April 28, 2010
# File: MarkovSong.py
# Inherits from Song, adds methods for Markov generation

from Song import *

class MarkovSong(Song):

    def __init__(self, title = 'Untitled', chords = []):
        Song.__init__(self, title, chords)


    def __str__(self):
        s = "Markoved Song <" + self.getTitle() + \
                           "> composed of following chords: " + "\n"
        for chord in self.chords:
            s = s + "time: " + str(chord.getTime()) + ', ' + \
                    "notes: " + str(chord.getNotesAsInts()) + '\n'
        return s


    def setup(self, inputFiles, tempoStyle, ):
        pass


def MarkovIt(input_files, len_prevNotes, num_notes):
    
    """
        Do Markov to the input files (MIDI), and return a <list> of <Note>s
    
        Step 1 : Generate Markov DB (dictionary) from the file inputs
        Step 2 : Generate a <list> of <Note>s based on the DB
    """
    
    DB = dict()
    
    for input_file in input_files:
        # do parsing
        midi_in = MidiInFile(MidiToText(), input_file)
    
        # Step 1
        DB = generate_DB(midi_in.read(), DB, len_prevNotes)

    # Step 2
    Notes = generate_notes(DB, num_notes)
    return Notes


    
def generate_DB(midiText, d = dict(), n = 2):
    """
        Generate and return a Markov DB (dictionary)
        - Key   : prevNote tuple (n : number of previous notes)
        - Value : nextNote tuple
        (* if DB has previosuly existed, it overwrites on the DB)
    """
        
    prevNote = tuple()
    t = wrapNote(tuple(midiText.replace('None', ' ').split()))

    # Create a dictionary of (prefix : suffix)
    for i in range(len(t) - n):
        prevNote = t[i : i+n]
        d[prevNote] = d.get(prevNote, tuple()) + (t[i+n],)

    return d


def generate_notes(DB, num_notes):
    """
        Generate a list of notes of length 'num_notes'
        based on the input dictionary DB
    """
    
    # Randomly choose prevNote from the DB
    prevNote = random.choice(DB.keys())
    notes = []

    # Repeat choosing a nextNote from DB, and append nextNote to the list
    for i in range (num_notes):
        
        # Choose nextNote randomly from prevNotes DB 
        # Sometimes the gui Markov Page listbox contains 
        # a blank element that can't be used in random.choice,
        # but is a non-fatal error. This never occurs on Windows,
        # only sometimes on Linux.
        try: nextNote = random.choice(DB.get(prevNote))
        except: TypeError

        # Add next note to the list
        notes.append(nextNote)

        # Get a new prevNote
        prevNote = shift(prevNote, nextNote)
    
    return notes



def outFileMarkovDB(files = [], fileName = '', key = 'Unknown Key'):
    """
        Take a <list> of MIDI files, do Markov analysis to
        input files, and output the final Markov DB as a text file.

        Observation indicates that it produces a bad DB when
        the input MIDI files in different keys are Markoved -
        thus, it must make sure that the input files are in the same key
    """
    #### Not yet developed ####
    
    pass



def inFileMarkovDB(fileName = ''):
    """
        Take the outFile of Markov DB, convert the text file data to
        <dict> database, and return the DB
    """
    fp = open(filename)     #Writes file to a 'file' type object
    f = fp.read()
    notelist = f.split()
    pairbank = dict()
    if len(notelist) < 3:
        return notelist
    else:
        for n in range(len(notelist)-2):
            key = (notelist[n], notelist[n+1])
            if key in pairbank:
                pairbank[key].append(notelist[n+2])   
            else:
                pairbank[key] = [notelist[n+2]]            
        return pairbank



def shift(prevNote, nextNote):
    """ Return a new prevNote tuple that contains nextNote """
    return prevNote[1:] + (nextNote,)



if __name__ == '__main__':

    # get data
    test_file1 = 'Input MIDIs/river flows in you.mid'
    test_file2 = 'Input MIDIs/river flows in you base.mid'

    # do markov
    notes1 = MarkovIt([test_file1], 2, 40)
    notes2 = MarkovIt([test_file2], 4, 40)

    # make durations
    durations1 = random_times(notes1)
    durations2 = constant_times(notes2, 2)

    # make chords
    song = MarkovSong()
    song.wrapNotesAndTimes(notes1, durations1)
    song.wrapNotesAndTimes(notes2, durations2)
    song.sort()
    print song

    # export to midi
    song.exportMidi(1, "Output MIDIs/" +
                    test_file1.split('.')[0].split('/')[1]
                    + '_markoved.mid')
