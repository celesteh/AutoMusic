# Authors: Shane Moon, Jeffrey Atkinson
# Software Design
# InvadingTheRealmOfTheArts
# April 28, 2010
# File: convertNote.py
# Changelog: Jeffrey fixed bugs on 4/29, adding int and rectifying funcs
# Converts Notes into format used by MusicalCanvas5

#import Song

def pitchToLMO(pitch):
    """
        Convert a pitch (int 0-127) to
        letter (string), modifier (string), octave (int 1-8?)
    """
    # we consider A-G# an octave, not C-B

    pitch = int(pitch)
    #if type(pitch) == str:
    #   print pitch

    # pretend notes that are very high or very low
    # are within reasonable range
    if pitch > 80:
        pitch = 80
    if pitch < 25:
        pitch = 25

    octave = 1
    while pitch > 32:
        pitch -= 12
        octave += 1
    
    mod = '' # make modifier default to nothing
    # flats don't exist in our language
    # we only use sharps
    if pitch == 21: letter = 'A'
    if pitch == 22: letter = 'A'; mod = 'sharp'
    if pitch == 23: letter = 'B'
    if pitch == 24: letter = 'C'
    if pitch == 25: letter = 'C'; mod = 'sharp'
    if pitch == 26: letter = 'D'
    if pitch == 27: letter = 'D'; mod = 'sharp'
    if pitch == 28: letter = 'E'
    if pitch == 29: letter = 'F'
    if pitch == 30: letter = 'F'; mod = 'sharp'
    if pitch == 31: letter = 'G'
    if pitch == 32: letter = 'G'; mod = 'sharp'


    return (letter, mod, octave)

def noteToLMO(note):
    return pitchToLMO(note.getPitch())
