# Authors: Shane Moon
# Software Design
# InvadingTheRealmOfTheArts
# April 28, 2010
# File: AutoComposeSong.py
# Inherits from Song, adds methods for compostion from music theory

from Song import *

class AutoComposeSong(Song):

    def __init__(self, title = 'Untitled', chords =[]):
        Song.__init__(self, title, chords)


    def __str__(self):
        s = "Auto-composed Song <" + self.getTitle() + \
                                 "> composed of following chords: " + "\n"
        for chord in self.chords:
            s = s + "time: " + str(chord.getTime()) + ', ' + \
                    "notes: " + str(chord.getNotesAsInts()) + '\n'
        return s


    def setup(self, genre, key, mode, chordProgression, numPhrase, beat, userInput):
        """
            Compose a song based on the input controls:
            - Genre
                : This determines the genre of the song. This controls
                  the general tempo / beat compositions of the song.
            - key
                : Key determines the kinds of chord progressions available
            - Chord Progression
                : This determines the chord progression throughout the song.
            - Number of Phrases
        """
        # Make a melody line of a song
        self.generate_melody(genre, key, chordProgression, mode, numPhrase, beat, userInput)

        # Make a base line of a song
        self.generate_base(genre, key, chordProgression, numPhrase, beat)



    def generate_melody(self, genre, key, chordProgression, mode, numPhrase, beat = 48, userInput = []):
        """
            Generate melody of different genres
            - chordProgression: i.e. 'F-G-Am-G'
            - numPhrase : number of phrases to be played in a song
            - beat : One beat always refers to a quater note.
                    
        """
        
        # Different styles of tempo
        ts = [[1],
             [1, 2, 3],
             [1, 2, 3, 4],
             [1, 3, 3.25],
             [1, 1.5, 2.0, 3.5],
             [0.5, 1, 1.5],
             [0.5, 1, 1.5, 2, 2.5, 3],
             [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]]

        if genre == 'New Age':
            # New Age Style Melody
            tempoStyles = [ts[0], ts[6]]
            beat_measure = beat * 4

        elif genre == 'Waltz':
            # Waltz Style (3/4) Melody
            tempoStyles = [ts[0], ts[5]]
            beat_measure = beat * 3

        elif genre == 'Pop':
            # Pop Style Melody
            tempoStyles = [ts[5], ts[6], ts[7]]
            beat_measure = beat * 4

        beat_phrase =  beat_measure * len(chordProgression.split('-'))

        """
            Generate melody, following the unique tempo style of each genre.
            Its notes are specially selected so that it follows the music theory
            
            * See 'selectPitch' method from Note class,
              for the detailed musical background.
        """
        
        for m in range(numPhrase):
            n = 0
            for chord in chordProgression.split('-'):
                tempoStyle = random.choice(tempoStyles)
                for k in tempoStyle:
                    note = Note().selectPitch(key, mode, [62, 74])
                    self.addChord(Chord([note],
                            m * beat_phrase + n * beat_measure + int(k * beat)))
                n += 1

        """
            Insert the user input melody, if there's any.
            
            * It would be really great if there were a mechanism
            to generate 'variation' of the input melodies,
            but that alone can be another big project. For now, it plays
            the input melody at some point during a song.
        """

        if userInput != []:
            self.replaceChords(userInput)
                
        self.sort()


    def generate_base(self, genre, key, chordProgression, numPhrase, beat = 48):
        """
            Generate base melodies of different genres.
            - chordProgression: i.e. 'F-G-Am-G'
            - numPhrase : number of phrases to be played in a song
            - beat : One beat always refers to a quater note.
            
        """

        if genre == 'New Age':
            # New Age Music Style Base
            
            beat_measure = beat * 4
            beat_phrase =  beat_measure * len(chordProgression.split('-'))
            
            for m in range(numPhrase):
                n = 0
                for chord in chordProgression.split('-'):
                    notes = SymbolToChord(chord, 4)
                    """
                        It follows the pattern of the general Arpeggio
                        that many New Age songs use.

                        * It plays the root, major 5th, and an octave-root
                          of a chord.
                    """
                    self.addChord((Chord([notes[0]],
                                m * beat_phrase + n * beat_measure + beat)))
                    self.addChord((Chord([notes[2]],
                                m * beat_phrase + n * beat_measure + beat * 2)))
                    self.addChord((Chord([notes[0].octave(1)],
                                m * beat_phrase + n * beat_measure + beat * 3)))
                    self.addChord((Chord([notes[2]],
                                m * beat_phrase + n * beat_measure + beat * 4)))
                    n += 1


        elif genre == 'Waltz':
            # Waltz Style (3/4) Base

            beat_measure = beat * 3
            beat_phrase =  beat_measure * len(chordProgression.split('-'))
            
            for m in range(numPhrase):
                n = 0
                for chord in chordProgression.split('-'):
                    """
                        It follows the general pattern that many Waltz songs
                        use. 

                        * It plays the root for the first beat, and
                          3rd and 5th of a chord for the remaining two beats.
                    """
                    notes = SymbolToChord(chord, 4)
                    self.addChord((Chord([notes[0]],
                                m * beat_phrase + n * beat_measure + beat)))
                    self.addChord((Chord([notes[1],notes[2]],
                                m * beat_phrase + n * beat_measure + beat * 2)))
                    self.addChord((Chord([notes[1], notes[2]],
                                m * beat_phrase + n * beat_measure + beat * 3)))
                    n += 1


        elif genre == 'Pop':
            # Pop Style Base

            beat_measure = beat * 4
            beat_phrase =  beat_measure * len(chordProgression.split('-'))


            for m in range(numPhrase):
                n = 0
                for chord in chordProgression.split('-'):
                    """
                        It follows the general pattern that many Pop songs
                        use for base guitars.

                        * It repeats playing every note in a chord
                    """
                    
                    notes = SymbolToChord(chord, 4)
                    for k in range(1,5):
                        self.addChord((Chord(notes,
                                m * beat_phrase + n * beat_measure + k * beat)))
                    n += 1
                    
        self.sort()



"""
    This is a collection of modules and variables
    that provides different methods of generating music 
"""


### Root / Key
[C, Db, D, Eb, E, F, Gb, G, Ab, A, Bb, B] = [0,1,2,3,4,5,6,7,8,9,10,11]


### Triads
I   = [0, 4, 7]          # Tonic
ii  = [2, 5, 9]          # Supertonic
iii = [0]                # Mediant
IV  = [0]                # Subdominant
V   = [7, 11, 14]        # Dominant
Vi  = [0]                # Submediant
VII = [0]                # Subtonic


### Musical Modes: Authentic / Plagal
Tonics = [0, 4, 5, 7, 9]            # Most Pleasing-Sound Scale
Lydian = [0, 2, 4, 5, 7, 9, 11]
Dorian = [0, 2, 3, 5, 7, 9, 10]
Mixolydian = [0, 2, 4, 5, 7, 9, 10]


### Sample Chord Progressions

CP1 = 'Gb_m-D-A-E'  # Key : A
CP2 = 'Ab_m-E-B-Gb' # Key : B
CP3 = 'A_m-F-C-G'   # Key : C
CP4 = 'F-G-A_m-G'   # Key : C
CP5 = 'C-G-A_m-E_m-F-C-F-G' # Key : C
CP6 = 'C_m-Bb-Ab-G_m'  # Key : Eb
CP7 = 'A-Ab_maug-Gb_m-E' # Key : A


def SymbolToChord(symbol = 'C_m', octave = 3):
    """
        Return the notes of a triad chord of the given symbol
        - The first capital letter refers to the note
        - The letters followed by '_', if any, refer to chord variation
    """
    notes = []
    root = eval(symbol.split('_')[0])
    for note in I:                           # Major Tonic Triad (Default)
        notes.append(root + note + octave * 12)

    if 'm' in symbol:       notes[1] -= 1    # Minor Triad
    if 'aug' in symbol:     notes[2] += 1    # Augmented Triad
    if 'dim' in symbol:     notes[2] -= 1    # Diminished Triad        
    
    return wrapNote(notes)



if __name__ == '__main__':

    autoSong = AutoComposeSong('Test')

    # Example Inputs
    genre = 'New Age'
    key = B
    mode = Tonics
    chordProgression = CP2
    numPhrase = 80
    beat = 48

    # Excerpt from 'River Flows in You', by Yiruma
    inputNotes = wrapNote([69, 68, 69, 68, 69, 64, 69, 62])
    inputTimes = [72, 144, 216, 288, 360, 432, 504, 578]

    userInput = Song()
    userInput.wrapNotesAndTimes(inputNotes, inputTimes)
    userInput = []

    # Export the Automated Song
    autoSong.setup(genre, key, mode, chordProgression, numPhrase, beat, userInput)
    autoSong.exportMidi(1, 'TEST.mid')

    print autoSong
