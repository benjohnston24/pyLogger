#! /usr/bin/env python
"""!

"""
__author__ = "Ben Johnston"
__revision__ = "0.1"
__date__ = "Fri Sep  5 17:52:56 EST 2014"
__license__ = "GPL"

##IMPORTS#####################################################################
from stdtoolbox.stdGUI import stdGUI, StdLabelFrame, StdLabel, StdButton
from stdtoolbox.stdGUI import StdFrame, StdEntry
from loggerUnit import UNIT_TYPES, CONNECTION_TYPES
from Tkinter import Tk, Menu, StringVar, OptionMenu
import tkFont
import os
#If the system is a Windows OS import required packages
if os.name == 'nt':
    import subprocess
import pdb
##############################################################################

##@var MAX_WIDGET_WIDTH
#Define the maximum width of a widget
MAX_WIDGET_WIDTH = 30


class pyLoggerGui(stdGUI):
    """!
    This class defines the graphical user interface for the pyLogger project
    """

##GUI Constructor Methods####################################################

    def __init__(self, version=None, debug_level=0):
        """
        The constructor for the class
        @param self The pointer for the object
        @param version A string containing the version number of software
        @param debug_level Control debugging functionality of the class.  Is
        derived from toolbox.logger debug_level.
        """
        ##@var root
        #The root window for the GUI
        self.root = Tk()
        stdGUI.__init__(self, self.root)
        self.root.title('pyLogger')
        #Override the close window command
        #self.root.protocol('WM_DELETE_WINDOW', self._quit)
        #Prevent resizing
        #self.root.resizable(width=False, height=False)
        #Add the toolbar icon
        #self.icon = tkImage("photo", file="bird.gif")
        #self.root.tk.call("wm", "iconphoto", self.root._w, self.icon)
        ##@var debug_level
        #The debug_level object for the system
        self.debug_level = debug_level
        ##@var version
        #The version number for the system
        self.version = version
        #Create a text entry field to store the current filename for data
        self.file_name = StringVar()
        self.file_frame = StdFrame(self.root)
        StdLabel(self.file_frame,
                 text='File Name:', justify='left').\
            grid(row=0, column=0, sticky='W')

        #Add the text entry field
        self.file_entry = StdEntry(self.file_frame,
                                   textvariable=self.file_name,
                                   width=int(MAX_WIDGET_WIDTH * 1.5))
        self.file_entry.grid(row=0, column=1, sticky='W',
                             padx=10)

        #Display the file name grid
        self.file_frame.grid(row=0, columnspan=2,
                             sticky='W', pady=5)
        #Generate frames
        number_of_units = 2
        #Create arrays to store dynamic interface components for each logger
        #unit
        self.unit_frame_dict = []
        #Update the selections and status variables in self.add_unit_frame
        for i in range(number_of_units):
            self.unit_frame_dict.append(self.add_unit_frame(self.root, i + 1))
            #Append to arrays
            #Display frame
            self.unit_frame_dict[-1]['frame'].grid(row=1, column=i)

        #Add start and stop buttons
        self.start_button = StdButton(self.root, text='Start',
                                      command=self.start)
        self.stop_button = StdButton(self.root, text='Stop',
                                     command=self.start)
        self.start_button.grid(row=2, column=0, pady=5)
        self.stop_button.grid(row=2, column=1, pady=5)
        ##Add a tool bar
        self.menu_bar = Menu(self.root)
        self.menu_bar.add_command(label='Results Folder',
                                  command=self.open_results)
        #Add the about button to get information about the system
        self.menu_bar.add_command(label='About',
                                  command=self.about)
        #Add menu bar
        self.root.config(menu=self.menu_bar)

    def add_unit_frame(self, parent=None, id=1):
        """!
        Construct the frame which is contains the widgets relating to a single
        data logging unit.
        @param self The pointer for the object
        @param id An identifier for use with the frame.  This identifier can be
        an integer or string and is displayed within the label of the frame
        @param parent The parent frame/object to be used for the new frame.
        @return The data logging unit frame
        """
        #Dictionary to encapsulate information
        data_dict = {}
        data_dict['frame'] = StdLabelFrame(parent, text='Unit Frame %s' % id)
        #Create dynamic components
        data_dict['unit'] = StringVar()
        data_dict['unit'].set(UNIT_TYPES[0])
        data_dict['status'] = StringVar()
        data_dict['status'].set(CONNECTION_TYPES[0])
        data_dict['reading'] = StringVar()
        data_dict['reading'].set('%0.2f' % 0)
        #Display components
        #Unit selection
        drop_down = OptionMenu(data_dict['frame'],
                               data_dict['unit'],
                               *UNIT_TYPES)
        drop_down.configure(width=MAX_WIDGET_WIDTH,
                            bg='white',
                            borderwidth=0,
                            highlightbackground='white',
                            highlightcolor='white')
        drop_down.grid(row=0, columnspan=2)

        #Connection Status
        StdLabel(data_dict['frame'],
                 text='Connection Status: ').\
            grid(row=1, column=0)
        data_dict['status_widget'] = StdLabel(data_dict['frame'],
                                              textvariable=data_dict['status'],
                                              fg='red')
        data_dict['status_widget'].grid(row=1, column=1)

        #Measurement
        StdLabel(data_dict['frame'],
                 textvariable=data_dict['reading'],
                 font=tkFont.Font(family='Arial',
                                  size=36),
                 bg='gray').\
            grid(row=2, columnspan=2, pady=20)
        return data_dict

    def about(self, event=None):
        """!
        Display the information window for the software.
        @param self The pointer for the object
        @event The handle for the mouse click event
        """
        pass

#Functional Methods###########################################################

    def start(self, event=None):
        pass

    def stop(self, event=None):
        pass


    def open_results(self):
        """!
        """
        if os.name == 'nt':
            subprocess.Popen('explorer "{0}"'.format(os.getcwd() +
                             '\\results\\'))
