# Written by someone else

from RawInstreamFile import RawInstreamFile
from modified_MidiFileParser import MidiFileParser


class MidiInFile:

    """
    
    Parses a midi file, and triggers the midi events on the outStream 
    object.
    
    """

    def __init__(self, outStream, infile=''):
        # these could also have been mixins, would that be better? Nah!
        self.raw_in = RawInstreamFile(infile)
        self.parser = MidiFileParser(self.raw_in, outStream)


    def read(self):
        "Start parsing the file"
        p = self.parser
        p.parseMThdChunk()
        return p.parseMTrkChunks()


    def setData(self, data=''):
        "Sets the data from a plain string"
        self.raw_in.setData(data)
    
    
if __name__ == '__main__':

    # get data
    test_file = 'test/midifiles/twinkle.mid'
    
    # do parsing
    from modified_MidiToText import MidiToText
    midi_in = MidiInFile(MidiToText(), test_file)
    midi_in.read()
    
    
    
