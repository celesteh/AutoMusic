# Authors: Rui Wang, Jeffrey Atkinson, Tom Lamar, Shane Moon
# Software Design
# InvadingTheRealmOfTheArts
# April 28, 2010
# File: Main.py
# Main GUI, serves as controller and view

from Tkinter import *
from PIL import Image, ImageTk
from tkFileDialog import *
import string
import tkFont
from Song import *
from convertNote import *
import math
import pygame
import sys
from MarkovSong import *
from AutoComposeSong import *

class DelayEvent:
    """
        This class is used to wrap a function and its arguments
        into an object that can be passed as a callback parameter
        and invoked later.  It is from the Python Cookbook 9.1, page 302,
        but with deprecated apply function removed.
    """
    
    def __init__(self, func, *args, **kwds):
        self.func = func
        self.args = args
        self.kwds = kwds

    def __call__(self):
        return self.func(*self.args, **self.kwds)

    def __str__(self):
        return self.func.__name__



class MusicalCanvas(Canvas):
    def __init__(self, master, *args, **options):
        Canvas.__init__(self, master, *args, **options)
        self.xLeft = 50
        self.xRight = 600
        self.pixelsPerLetter = 4 #how many pixels E-F, for example
        self.trebleFLoc = -100 #will become positive before it is used
        self.xSpacing = 20
        self.maxXLoc = 550
        self.minXLoc = 100
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
        wholeNoteDur = 8*48 #default assumption
        chords = song.getChords()
        if isinstance(chords, Chord): #if just 1
            #we can't tell the length of the final chord
            #let's assume a whole note
            self.addChord(chords, 'w')
        elif type(chords) == list: #if a list of chords
            #truncate to display just the beginning
            numChordsToParse = min(len(chords) - 1, 54)
            for i in range(numChordsToParse): #parse through all but the last
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
            print 'goign to draw a rest'
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
        self.drawEighthNote(centerX, centerY)
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
        

##   Rui Wang wrote the rest of this file, with edits by Shane.

class Functions_Provider():
    """
       Defines common functions and methods that will be used by
       the widgets in the GUI. Menubar Object and all Pages are
       inherited from this class because all of them are
       function providers.
    """
    def file_open(self, parent, page_type, loadpic, waitpic,
                  incontainer, outcontainer, records, music):
        filename = askopenfilename(filetypes=[("midifiles","*.mid")],
                                  initialdir = 'Input Midis')

        if filename !='':
            filename = filename.split('/')
            self.page_factory(parent, 'DisplayMusic', loadpic, waitpic,
                              incontainer, outcontainer, records, filename[-1])
        

##    Redundant since the program can autosave
    def file_save(self):
        filename = asksaveasfile(filetypes=[("midifiles","*.mid")])

    def about_generator(self):
        about_window = Toplevel()
        Label(about_window, text =
              "Made by Shane, Rui, Tom and Jeffkinson.").pack()        

    def page_factory(self, parent, page_type, loadpic, waitpic,
                     incontainer, outcontainer, record, music):
        """
           parent = self.root
           page_type = page to be made/load
           loadpic & waitpic = jpeg files
           incontainer = existing page, bound by a tk Label
           outcontainer = Label holding the incontainer
           record = dictionary of the pages made and their names
           music = music made by clicking the 'Generate' button
        
           Makes a new page if it does not already exist. Else,
           loads the existing page.
   
           First, try to hide the current page (incontainer).
           Attribute error occurs when the program first loads and
           there is not a current page to hide. This is passed.

           All page_types except 'display music' are made only once
           and the same page is loaded everytime the page name is
           called. However, 'display music' is re-made every time
           because the page is different for every piece of music.
        """
        
        try:
            incontainer.pack_forget()
            
        except:
            AttributeError

        if page_type != 'DisplayMusic':
            if page_type not in record.keys():
                new_page_type = Label(outcontainer)
                eval(page_type)(parent, loadpic, waitpic,
                       new_page_type, outcontainer, record, music)   
                record[page_type] = new_page_type
                outcontainer.pack()
                
            record[page_type].pack()
            MenuBar(parent, loadpic, waitpic, record[page_type],
                    outcontainer, record, music)


        else:
            new_page_type = Label(outcontainer)
            DisplayMusic(parent, loadpic, waitpic,
                         new_page_type, outcontainer,
                         record, music)
            new_page_type.pack()

            outcontainer.pack()
            MenuBar(parent, loadpic, waitpic, new_page_type,
                    outcontainer, record, music)

        """
           The menubar is overwritten everytime a page loads
           because it has to track which page is it currently
           on. Initially, it was meant to be updated instead of
           over-written. But error messages and time constraints
           of this project prevented that from happening :(
        """
        
    def some_function(self):
        print 'lalala'

    def highlight(self, button):
        button['bg'] = 'gray75'

    def unhighlight(self, button):
        button['bg'] = 'gray88'

    def kill(self):
        """
           Terminates the program.
        """
        try:
            pygame.mixer.quit()
        except:
            pass
        self.parent.destroy()

    def add_this(self):
        filename = askopenfilename(initialdir = 'Input Midis',
                                   filetypes=[("midifiles","*.mid")])
        file_rep = filename.split('/')[-1]
        self.listbox.insert(END, file_rep)

    def remove_this(self):
        try:
            selected = self.listbox.curselection()
            index = int(selected[0])
            self.listbox.delete(index)
        except:
            IndexError


class MenuBar(Functions_Provider):

    """
       Menubar stays the same on all pages. Contains links to
       allow the user to go to other pages when using the program.
    """
       
   
    def __init__(self, parent, loadpic, waitpic, incontainer,
                 outcontainer, records, music):

        self.parent = parent

        # Menu items and their commands
        self.menubar = Menu(parent)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.editmenu = Menu(self.menubar, tearoff=0)
        self.aboutmenu = Menu(self.menubar, tearoff=0)
        self.windowmenu = Menu(self.filemenu, tearoff=0)
        
        self.menubar.add_cascade(label = "File",
                                 menu = self.filemenu)

        self.filemenu.add_command(label = 'Launch Page',
                                  command = DelayEvent(self.page_factory,
                                  parent, 'Launch', loadpic, waitpic,
                                  incontainer, outcontainer, records, music))

        # self.filemenu.add_command(label = "Open",
        #                          command = DelayEvent(self.file_open,
        #                          parent, 'DisplayMusic', loadpic, waitpic,
        #                          incontainer, outcontainer, records, music))
        
        self.filemenu.add_command(label = "Save",
                                  command = self.file_save)


        self.filemenu.add_command(label = "Exit", command = self.kill)
        
        self.menubar.add_cascade(label = "Generate", menu = self.windowmenu)

        for page_type in ('Markov', 'Random', 'Controlled'):
            self.windowmenu.add_command(
                label=str(page_type) + ' Generation',
                command=DelayEvent(self.page_factory,
                                   parent, page_type, loadpic,
                                   waitpic, incontainer,
                                   outcontainer, records, music))
            

        self.menubar.add_cascade(label = "Help", menu = self.aboutmenu)
        self.aboutmenu.add_command(label = "About",
                                   command = self.about_generator)

        # Pack the menu
        parent.config(menu = self.menubar)


        
class Launch(Functions_Provider):
    """
       This is a welcoming page that the user sees upon running the
       program. Contains links to the 3 different kinds of
       music generation.
    """
	
    def __init__(self, parent, loadpic, waitpic,
                 incontainer, outcontainer, records, music):
        
        # bkgd = background. Just for aesthetic purposes
        self.bkgd = Label(incontainer,
                  width = parent.winfo_screenwidth(),
                  height = parent.winfo_screenheight(),
                  image = loadpic)

        # Frames / labels / font for aesthetics    
        fm = Frame(self.bkgd, borderwidth = 2, width = 350,
                   height = 800, relief = RIDGE, bg = "floralwhite")

        logo = "logo.bmp"
        logo = ImageTk.PhotoImage(Image.open(logo))     
        logoLb = Label(fm, image = logo)
        logoLb.pack(side = TOP, pady = 5)
        logoLb.image = logo

        but_font = tkFont.Font(family = "Calibri", size = 12)

        # These 3 buttons contains the links to other pages
        for button in ('Markov', 'Random', 'Controlled'):

            Button(fm, bg = "white", text = button + ' Generation',
                   font = but_font,
                   command=DelayEvent(self.page_factory, parent,
                                      button, loadpic, waitpic,
                                      incontainer, outcontainer,
                                      records, music))\
                                      .pack(side = TOP, padx = 0,
                                            pady=35)

        # Allow the user to look at existing music instead            
        # bu = Button(fm, bg = "white", text = 'Load', font = but_font,
        #            command = DelayEvent(self.file_open,
        #            parent, 'DisplayMusic', loadpic, waitpic,
        #            incontainer, outcontainer, records, music))
        
        # bu.pack(side = TOP, pady = 20)
        
        fm.pack(side = TOP, padx = 0,pady = 100)
        
        self.bkgd.pack_propagate(0) 
        self.bkgd.pack(fill = 'both', expand = 'yes')
        self.bkgd.image = loadpic

    
class Markov(Functions_Provider):

    """
       This page allows the user to use Markov Generation.
    """
	
    def __init__(self, parent, loadpic,
                 waitpic, incontainer,
                 outcontainer, records, music):
        
        # bkgd = background
        self.bkgd = Label(incontainer,
                  width = parent.winfo_screenwidth(),
                  height = parent.winfo_screenheight(),
                  image = loadpic)
    
        fm = Label(self.bkgd, borderwidth = 2, width = 350,
                   height = 400, relief = RIDGE, image = waitpic)

        label_font = tkFont.Font(family = "Calibri", size = 12)
        Label(fm, text = 'Import Music Files',
              font = label_font).pack(pady = 25)

        # Listbox Frame
        lbfm = Frame(fm)
        scroll = Scrollbar(lbfm)
        self.listbox = Listbox(lbfm, yscrollcommand = scroll.set)
        scroll.config(command = self.listbox.yview)
        scroll.pack(side = RIGHT, fill = Y)
        self.listbox.pack()
        lbfm.pack()

        # Buttons
        but_font = tkFont.Font(family = "Calibri", size = 12)

        self.addbutton = Button(fm, text = 'Add Midi File', width = 15,
                                command = DelayEvent(self.add_this))
        self.removebutton = Button(fm, text = 'Remove Midi File', width = 15,
                                   command = DelayEvent(self.remove_this))


        self.addbutton.pack(side = TOP, padx = 0, pady = 0)
        self.removebutton.pack(side = TOP, padx = 0, pady = 0)
        

        but_image = ImageTk.PhotoImage(Image.open("generate.bmp"))

        do_markov = Button(fm, image = but_image, height = 47, width = 125,
                           command = DelayEvent(self.Generate_Markov,
                                                parent, 'DisplayMusic',
                                  loadpic, waitpic, incontainer,
                                  outcontainer, records, music))
        
        do_markov.pack(side = TOP, pady = 20)
        do_markov.image = but_image

        fm.pack_propagate(0)
        fm.pack(side=TOP, padx = 0,pady = 150)
        self.bkgd.pack_propagate(0) 
        self.bkgd.pack(fill = 'both', expand = 'yes')
        self.bkgd.image = loadpic


    def Generate_Markov(self, parent, page_type, loadpic, waitpic,
                        incontainer, outcontainer, records, music):
        """
            This is a callback function for 'Generate' button.
            It takes the selected input files from the listbox,
            and executes Markov functions to output a MIDI file.
            
            * See 'MarkovSong.py' for the detailed explanation
            on how these methods work.            
        """
        sourcefiles = []
        for midfile in self.listbox.get(0, END):
            sourcefiles.append("Input Midis/" + str(midfile))

        len_prevNotes = 2
        num_notes = 40

        # Create Song
        song = MarkovSong()
        song.reset()
        song.setTitle(midfile.split('.')[0] + "_markoved")
        
        for sourcefile in sourcefiles:
            # Do markov
            notes = MarkovIt([sourcefile], len_prevNotes, num_notes)
            # Generate durations
            durations = random_times(notes)             

            song.wrapNotesAndTimes(notes, durations)

        song.sort()
        song.exportMidi(1, "Output MIDIs/" + song.getTitle() + ".mid")
        self.page_factory(parent, page_type, loadpic, waitpic,
                          incontainer, outcontainer, records,
                          song)
        
class Random(Functions_Provider):

    def __init__(self, parent, loadpic,
                 waitpic, incontainer,
                 outcontainer, records, music):

        
        # bkgd = background
        self.bkgd = Label(incontainer,
                  width = parent.winfo_screenwidth(),
                  height = parent.winfo_screenheight(),
                  image = loadpic)
    
        fm = Label(self.bkgd, borderwidth = 2, width = 350,
                   height = 200, relief = RIDGE, image = waitpic)

        label_font = tkFont.Font(family = "Calibri", size = 12)
        Label(fm, text = 'Generates a random piece based on \n'+
              'random selection of chords, melody types etc.',
              font = label_font, bg = "white").pack(pady = 25)

        but_image = ImageTk.PhotoImage(Image.open("generate.bmp"))

        do_random = Button(fm, image = but_image, height = 47, width = 125,
                           command = DelayEvent(self.AutoMusic, parent,
                                       'DisplayMusic', loadpic, waitpic,
                                       incontainer, outcontainer,
                                       records, music))
                   
        do_random.pack(side = TOP, pady = 20)
        do_random.image = but_image

        fm.pack_propagate(0)
        fm.pack(side=TOP, padx = 0,pady = 250)
        self.bkgd.pack_propagate(0) 
        self.bkgd.pack(fill='both', expand='yes')
        self.bkgd.image = loadpic

    def AutoMusic(self, parent, page_type, loadpic, waitpic,
                  incontainer, outcontainer, records, music):
        """
            This is a callback function for 'Generate' button.
            It takes the random inputs, make an AutoComposeSong object,
            and execute its functions to output a MIDI file.
            
            * See 'AutoComposeSong.py' for the detailed explanation
            on how these methods work.
        """

        genre = random.choice(["Waltz", "Pop", "New Age"])
        key = C
        cp = random.choice([CP3, CP4, CP5])
        title = "Randomly Generated Song"
        mode = Tonics
        numPhrase = 4
        beat = 72
        userInput = []
        
        autoSong = AutoComposeSong()
        autoSong.reset()
        autoSong.setTitle(title)
        autoSong.setup(genre, key, mode, cp, numPhrase, beat, userInput)
        autoSong.exportMidi(1, 'Output MIDIs/' + title + '.mid')
        
        self.page_factory(parent, page_type, loadpic, waitpic,
                          incontainer, outcontainer, records, autoSong)


class Controlled(Functions_Provider):

    """
        This page implements modles from 'AutoComposeSong' to generate
        a music file. User can select 'genre', 'key','chord progression'
        and so on. Then it generates a song based on the inputs selected
        by its user.
        
        * For the detailed explanation on how the module works,
        see 'AutoComposeSong.py'
    """
	
    def __init__(self, parent, loadpic, waitpic,
                 incontainer, outcontainer, records, music):
        
        # bkgd = background
        self.bkgd = Label(incontainer,
                  width=parent.winfo_screenwidth(),
                  height=parent.winfo_screenheight(),
                  image=loadpic)

        # Faded Background
        fm = Label(self.bkgd, borderwidth = 2, width = 400,
                   height = 550, relief = RIDGE, image = waitpic)

        label_font = tkFont.Font(family = "Calibri", size=12)
        Label(fm, text = 'Piece Specifications',
              font = label_font).pack(pady = 25)

        # Selection Lists
        self.keyList = ["A", "B", "C", "Eb"]
        self.cpList = [CP1, CP2, CP3, CP4, CP5, CP6, CP7]
        self.genreList = ["Waltz", "New Age", "Pop"]

        
        """ Write the Title """
        title_fm = Frame(fm)
        title_lb = Label(title_fm, text = 'Write the title',
                         font = label_font, width = 30)
        title_lb.pack(side = TOP)
        
        self.title = Entry(title_fm, width = 45)
        self.title.pack(side = TOP, pady = 5)
        title_fm.pack(side = TOP, padx = 30, pady = 10)

        # Generate Button
        but_image = ImageTk.PhotoImage(Image.open("generate.bmp"))

        auto_compose = Button(fm, image=but_image, height = 27,
                              width = 125, command = DelayEvent(
                                  self.AutoMusic, parent, 'DisplayMusic',
                                  loadpic, waitpic, incontainer,
                                  outcontainer, records, music))
        
        auto_compose.pack(side = BOTTOM, pady = 30)
        auto_compose.image = but_image

        # User input field
        entry_frame = Frame(fm)
        entry_title = Label(entry_frame, text = 'Melody to be Included',
                            font = label_font)
        entry_title.pack(side = TOP)
        self.entry_field = Entry(entry_frame, width = 45)
        self.entry_field.insert(0, "66-67-68")
        self.entry_field.pack(side = TOP, pady = 5, padx = 10)
        entry_frame.pack(side=BOTTOM, pady=0)
        

        """ Select the Chord Progression """
        cp_fm = Frame(fm)
        chord_lab = Label(cp_fm, text = 'Select Chord Progression',
                          font = label_font, width = 20)
        chord_lab.pack(side = TOP)
        cp_fm.pack(side = LEFT, padx = 30)
        
        # Make a Listbox Frame        
        cp_lbfm = Frame(cp_fm)
        scroll = Scrollbar(cp_lbfm)
        self.cp_listbox = Listbox(cp_lbfm, yscrollcommand = scroll.set,
                                  height = 10, width = 25,
                                  exportselection = 0)

        # Add items to a ListBox
        for chord_progression in self.cpList:
            self.cp_listbox.insert(END, chord_progression)

        # Add Scrollbar
        scroll.config(command = self.cp_listbox.yview)
        scroll.pack(side = RIGHT, fill = Y)

        # Pack
        self.cp_listbox.pack()
        cp_lbfm.pack(side = TOP)

        
        """ Select the Key """
        key_fm = Frame(fm, width=13)
        key_label = Label(key_fm, text='Select the Key', width = 20,
                          font = label_font)
        key_label.pack(side = TOP)
        key_fm.pack(side=TOP, padx = 30, pady = 25)
        
        # Make a Listbox Frame        
        key_lbfm = Frame(key_fm)
        scroll = Scrollbar(key_lbfm)
        self.key_listbox = Listbox(key_lbfm, yscrollcommand = scroll.set,
                                   width = 20, height = 4, exportselection = 0)


        # Add items to a Listbox
        for key in self.keyList:
            self.key_listbox.insert(END, key)

        # Add Scrollbar
        scroll.config(command = self.key_listbox.yview)
        scroll.pack(side=RIGHT, fill=Y)

        # Pack
        self.key_listbox.pack()
        key_lbfm.pack(side = RIGHT)


        """ Select the Genre """
        gr_fm = Frame(fm)        
        genre_lab = Label(gr_fm, text='Select the Genre', width = 20,
                          font = label_font)
        genre_lab.pack(side = TOP)
        gr_fm.pack(side=TOP, padx = 30, pady = 0)

        # Make a Listbox Frame        
        gr_lbfm = Frame(gr_fm)
        scroll = Scrollbar(gr_lbfm)
        self.gr_listbox = Listbox(gr_lbfm, yscrollcommand = scroll.set,
                                  height = 3, exportselection = 0)

        # Add items to a ListBox
        for genre in self.genreList:
            self.gr_listbox.insert(END, genre)

        # Add Scrollbar
        scroll.config(command = self.gr_listbox.yview)
        scroll.pack(side = RIGHT, fill = Y)

        # Pack
        self.gr_listbox.pack()
        gr_lbfm.pack(side = TOP)

        fm.pack_propagate(0)
        fm.pack(side = TOP, padx = 0,pady = 80)
        self.bkgd.pack_propagate(0) 
        self.bkgd.pack(fill = 'both', expand = 'yes')
        self.bkgd.image = loadpic     

    def AutoMusic(self, parent, page_type, loadpic, waitpic,
                  incontainer, outcontainer, records, music):
        """
            This is a callback function for 'Generate' button.
            It takes the selected inputs from the listbox,
            make an AutoComposeSong object, and execute its functions
            to output a MIDI file.
            
            * See 'AutoComposeSong.py' for the detailed explanation
            on how these methods work.            
        """

        genre = self.genreList[int(self.gr_listbox.curselection()[0])]
        key = eval(self.keyList[int(self.key_listbox.curselection()[0])])
        cp = self.cpList[int(self.cp_listbox.curselection()[0])]
        title = self.title.get()
        
        mode = Tonics
        numPhrase = 4
        beat = 72

        if self.entry_field.get() == '':
            userInput = []
        else:
            userInput = Song()
            userInput.reset()
            userInputMelody = wrapNote(self.entry_field.get().split('-'))
            userInputTimes = constant_times(userInputMelody, 2, beat)
            userInput.wrapNotesAndTimes(userInputMelody, userInputTimes)
        
        autoSong = AutoComposeSong()
        autoSong.reset()
        autoSong.setTitle(title)
        autoSong.setup(genre, key, mode, cp, numPhrase, beat, userInput)
        autoSong.exportMidi(1, 'Output MIDIs/' + title + '.mid')

        self.page_factory(parent, page_type, loadpic, waitpic,
                          incontainer, outcontainer, records, autoSong)
        

class DisplayMusic(Functions_Provider):

    def __init__(self, parent, loadpic,
                 waitpic, incontainer, outcontainer, records, music):

        self.music = music
        
        # bkgd = background
        self.bkgd = Label(incontainer,
                  width=parent.winfo_screenwidth(),
                  height=parent.winfo_screenheight(),
                  image=waitpic)
    
        self.fm = Label(self.bkgd, width = parent.winfo_screenwidth(),
                        height=2)

        """
           A set of 5 buttons. I wanted to make them with a 'for' loop
           initially. But each of them calls a different function
           and i could not store them somehow.
           i.e.if i write: for button in [1, 2, 3]: self.button=button,
           pythons rewrite over self.button 3 times instead of saving
           self.1, self.2 and self.3
        """
        # button 1
        self.open_but = Button(self.fm, text='Open', width=15,
                               relief = FLAT, cursor = 'hand2',
                               command=DelayEvent(self.file_open,
                            parent, 'DisplayMusic', loadpic, waitpic,
                            incontainer, outcontainer, records, music))
        self.open_but.bind('<Enter>',
                      lambda ignore_event: self.highlight(self.open_but))
        self.open_but.bind('<Leave>',
                      lambda ignore_event: self.unhighlight(self.open_but))
        self.open_but.pack(side=LEFT)

        #button 2
        self.save_but = Button(self.fm, text='Save', width=15, relief = FLAT,
                               cursor = 'hand2', command = self.file_save)
        self.save_but.bind('<Enter>',
                           lambda ignore_event: self.highlight(self.save_but))
        self.save_but.bind('<Leave>',
                           lambda ignore_event: self.unhighlight(self.save_but))
        self.save_but.pack(side=LEFT)

        #button 3
        self.play_but = Button(self.fm, text='Play', width=15, relief = FLAT,
                               cursor = 'hand2', command = self.playMusic)
        self.play_but.bind('<Enter>',
                           lambda ignore_event: self.highlight(self.play_but))
        self.play_but.bind('<Leave>',
                           lambda ignore_event: self.unhighlight(self.play_but))
        self.play_but.pack(side=LEFT)

##        # button 4
##        self.pause_but = Button(self.fm, text='Pause', width=15, relief = FLAT,
##                                cursor='hand2')
##        self.pause_but.bind('<Enter>',
##                            lambda ignore_event: self.highlight(self.pause_but))
##        self.pause_but.bind('<Leave>',
##                            lambda ignore_event: self.unhighlight(self.pause_but))
##        self.pause_but.pack(side=LEFT)

        # button 5
        self.stop_but = Button(self.fm, text='Stop', width=15, relief = FLAT,
                               cursor='hand2', command = self.stopMusic)
        self.stop_but.bind('<Enter>',
                           lambda ignore_event: self.highlight(self.stop_but))
        self.stop_but.bind('<Leave>',
                           lambda ignore_event: self.unhighlight(self.stop_but))
        self.stop_but.pack(side=LEFT)
        
        self.fm.pack_propagate(0)
        self.fm.pack(side=TOP)

        """ Make the musical frame to display the musical staff"""
        music_frame = Frame(self.bkgd, height = 600, width = 640)
        music_frame.pack_propagate(0) 
        music_frame.pack(side=RIGHT, padx=50)
        
        self.bkgd.pack_propagate(0) 
        self.bkgd.pack(fill='both', expand='yes')
        self.bkgd.image = loadpic


        """ Puts in the musical staff"""
        scroll = Scrollbar(music_frame)
        display = MusicalCanvas(music_frame, yscrollcommand = scroll.set,
                                bg = 'white', height = 800, width = 640)
        scroll.config(command = display.yview)
        scroll.pack(side = RIGHT, fill = Y)
        display.pack()
        #add song to canvas
        display.addSong(music)

    def playMusic(self):
        pygame.mixer.init(44100, -16, 2, 2048)
        pygame.mixer.music.load('Output MIDIs/'+ self.music.getTitle() + '.mid')
        pygame.mixer.music.play()

    def stopMusic(self):
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.quit()
        

class Gui(Functions_Provider):

    def __init__(self):

        '''
        Make Root Window. Once made, this window
        remains until Program terminates(by
        selecting exit from the file menu
        or the close window button.).
        '''
        self.root = Tk()
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.overrideredirect
        self.root.geometry("%dx%d+0+0" % (w-8, h-85))
        self.root.title('My Music Generator')

        '''
        Load all necessary graphics
        '''

        loadingimage = "Music.bmp"
        waitingimage = "Music_fade.bmp"

        loadimage = ImageTk.PhotoImage(Image.open(loadingimage))
        waitimage = ImageTk.PhotoImage(Image.open(waitingimage))

        '''
        A container contains the page object
        except the menu bar. With each page change,
        the contents of the container changes.
        '''
        self.outer_container = Label()

        '''
        Record of the page objects created. Allows old page
        objects that were created but hidden to be called up again.
        '''
        self.record = {}


        '''
        A Launch object loads by default when the program
        initialize, can be changed from buttons on the
        page and the menu bar.
        '''

        
        self.page_factory(self.root, 
                          'Launch', loadimage, waitimage,
                          None, self.outer_container,
                          self.record, None)

        
        self.root.mainloop()


if __name__ == '__main__':
    Gui()

