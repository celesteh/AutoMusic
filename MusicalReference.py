# Authors: Shane Moon
# Software Design
# InvadingTheRealmOfTheArts
# April 28, 2010
# File: MusicalReference.py

"""
    This file contains all the necessary musical definitions
"""



def getMode(key, mode, octave):
    """
        Return the notes of a given mode
    """
    notes = []
    for (note) in range (octave[0] * 12, octave[1] * 12):
        if (note - int(key)) % 12 in mode:
            notes.append(note)
    return notes


def int_to_char(notes):
    """
        Convert notes in integer into notes in characters
    """

    d = {0:'C', 1:'Db', 2:'D', 3:'Eb', 4:'E', 5:'F', 6:'Gb', 7:'G',
         8:'Ab', 9:'A', 10:'Bb', 11:'B'}

    if type(notes) == instance:
        char_notes = d[notes % 12] + str(notes / 12)
        
    elif type(notes) == list:
        char_notes = []
        for note in notes:
            char_notes.append(d[note % 12] + str(note / 12))

    return char_notes


def detect_key(notes):
    """
        Return the most-likely key of the input notes
        *** Need to be imporved ***
    """
    d = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0}
    
    for note in notes:
        d[int(note) % 12] += 1

    if   d[8] > 0: return 'A'  #  A Major : F#, C#, G#
    elif d[6] > 0: return 'D'  #  D Major : F#, C#
    elif d[1] > 0: return 'G'  #  G Major : F#
    else:          return 'C'  #  C Major



if __name__ == '__main__':
    print getMode(C, Lydian, [4,8])
    print int_to_char(minor(getChord(Gb, I)))

    example = '69 68 69 68 69 64 69 62 61 62 64' # excerpt from an A Major song
    print detect_key(example.split(' '))

