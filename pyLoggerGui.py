#! /usr/bin/env python
"""!

"""
__author__ = "Ben Johnston"
__revision__ = "0.3"
__date__ = "Fri Sep  5 17:52:56 EST 2014"
__license__ = "GPL"

##IMPORTS#####################################################################
from stdtoolbox.stdGUI import stdGUI, StdLabelFrame, StdLabel
from stdtoolbox.stdGUI import StdFrame, StdEntry
from pyLoggerWidgets import pyLoggerButton
from stdtoolbox import __revision__ as std_rev
from stdtoolbox.logging import logger
from loggerUnit import UNIT_TYPES, CONNECTION_TYPES
from Tkinter import Menu, StringVar, OptionMenu, Toplevel, CENTER, LEFT
from Tkinter import Image as tkImage
import tkMessageBox
import tkFont
import Queue
import os
import sys
import time
#Hardware imports
from TSI import __revision__ as TSI_rev
from AFG import __revision__ as AFG_rev
#If the system is a Windows OS import required packages
if os.name == 'nt':
    import subprocess
##############################################################################

##@var MAX_WIDGET_WIDTH
#Define the maximum width of a widget
MAX_WIDGET_WIDTH = 30

##@var ERROR_TIME
#The time limit used to prevent multiple errors occurring within quick
#succession (in seconds)
ERROR_TIME = 1


class pyLoggerGui(stdGUI):
    """!
    This class defines the graphical user interface for the pyLogger project
    """

##GUI Constructor Methods####################################################

    def __init__(self,
                 root=None,
                 queue=None,
                 version=None,
                 number_of_units=2,
                 log_folder=None,
                 start_command=None,
                 reset_command=None,
                 stop_command=None,
                 debug_level=0):
        """
        The constructor for the class
        @param self The pointer for the object
        @param root The Tkinter Tk object for the class
        @param queue The Queue object to be used by the class for dynamically
        updating widgets from a thread
        @param version A string containing the version number of software
        @param number_of_units The number of loggerUnit objects  to be used by
        the class
        @param start_command The handle for the function to be used to start
        the logging process
        @param reset_command The handle for the function to be used to restart
        the logging process
        @param stop_command The handle for the function to be used to stop the
        logging process
        @param debug_level Control debugging functionality of the class.  Is
        derived from toolbox.logger debug_level.
        """
        #Log for debugging
        self.debug_logger = logger('guiQueueData.log', debug_level=debug_level)

        ##@var root
        #The root window for the GUI
        self.root = root
        stdGUI.__init__(self, self.root)
        self.root.title('pyLogger')
        #Override the close window command
        self.root.protocol('WM_DELETE_WINDOW', self._quit)
        #Prevent resizing
        self.root.resizable(width=False, height=False)
        #Add the toolbar icon
        self.icon = tkImage("photo", file="pyLogger.gif")
        self.root.tk.call("wm", "iconphoto", self.root._w, self.icon)
        ##@var queue
        #The queue object to pass information between threads
        self.queue = queue
        ##@var error_timer
        #A timer that is used to prevent multiple errors from being displayed
        #in quick succession
        self.error_timer = time.time()
        ##@var quit_command
        #The command to stop threads
        self.quit_command = stop_command
        ##@var version
        #The version number for the system
        self.version = version
        #Create a text entry field to store the current filename for data
        self.file_name = StringVar()
        self.file_frame = StdFrame(self.root)
        ##@var number_of_units
        #The number of logging units to be used byt the class.  This variable
        #controls the number of log unit frames that are generated and
        #displayed
        self.number_of_units = number_of_units
        ##@var log_folder
        #The folder where results are stored
        self.log_folder = log_folder
        StdLabel(self.file_frame,
                 text='Test Id:', justify='left').\
            grid(row=0, column=0, sticky='W')

        #Add the text entry field
        self.file_entry = StdEntry(self.file_frame,
                                   textvariable=self.file_name,
                                   width=int(MAX_WIDGET_WIDTH * 1.5))
        self.file_entry.grid(row=0, column=1, sticky='W',
                             padx=10)

        self.log_name = StringVar()
        StdLabel(self.file_frame,
                 text='Log File Name: ', justify='left').\
            grid(row=1, column=0, sticky='W')
        StdLabel(self.file_frame,
                 textvariable=self.log_name, justify='left').\
            grid(row=1, column=1, sticky='W', padx=10)
        #Display the file name grid
        self.file_frame.grid(row=0, columnspan=2,
                             sticky='W', pady=5)
        #Create arrays to store dynamic interface components for each logger
        #unit
        self.unit_frame_dict = []
        #Update the selections and status variables in self.add_unit_frame
        for i in range(self.number_of_units):
            self.unit_frame_dict.append(self.add_unit_frame(self.root, i + 1))
            #Append to arrays
            #Display frame
            self.unit_frame_dict[-1]['frame'].grid(row=1, column=i)

        #Add help frame
        self.add_help_frame(self.root).grid(row=0,
                                            column=i + 1,
                                            rowspan=2,
                                            padx=10,
                                            pady=10,
                                            sticky='N')
        #Add start and stop buttons
        self.start_button = pyLoggerButton(self.root, text='Start',
                                           command=start_command)
        self.stop_button = pyLoggerButton(self.root, text='Stop',
                                          command=reset_command)
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
        #Centre window
        #self.centre_window(self.root)
        #Prevent resizing
        self.root.resizable(width=False, height=False)

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
        data_dict['frame'] = StdLabelFrame(parent, text='Device %s' % id)
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

    def add_help_frame(self, parent=None):
        """!
        This frame provide a simple usage instructions
        """
        normal_size = 9
        help_frame = StdFrame(parent)
        StdLabel(help_frame,
                 text='How To Use pyLogger',
                 font=tkFont.Font(family='Arial',
                                  size=14,
                                  weight='bold'),
                 ).grid(row=0, sticky='W')
        StdLabel(help_frame,
                 text='1. Connect the required USB/serial adaptors\n'
                      'and corresponding serial cables.',
                 font=tkFont.Font(family='Arial',
                                  size=normal_size),
                 justify=LEFT,
                 ).grid(row=1, sticky='W')
        StdLabel(help_frame,
                 text='2. Select the device type(s) in the drop down menus\n'
                      'that are to be used during logging.',
                 font=tkFont.Font(family='Arial',
                                  size=normal_size),
                 justify=LEFT
                 ).grid(row=2, sticky='W')
        StdLabel(help_frame,
                 text='3. Enter a file name for the log file.',
                 font=tkFont.Font(family='Arial',
                                  size=normal_size),
                 justify=LEFT
                 ).grid(row=3, sticky='W')
        StdLabel(help_frame,
                 text='4. Click Start to begin logging',
                 font=tkFont.Font(family='Arial',
                                  size=normal_size),
                 justify=LEFT
                 ).grid(row=4, sticky='W')
        StdLabel(help_frame,
                 text='5. Click Stop when done',
                 font=tkFont.Font(family='Arial',
                                  size=normal_size),
                 justify=LEFT
                 ).grid(row=5, sticky='W')
        StdLabel(help_frame,
                 text='6. Use the Results Folder tool bar option\n'
                      ' to access the log file',
                 font=tkFont.Font(family='Arial',
                                  size=normal_size),
                 justify=LEFT
                 ).grid(row=6, sticky='W')

        return help_frame

#Functional Methods###########################################################

    def start(self, event=None):
        pass

    def stop(self, event=None):
        pass

    def about(self, event=None):
        """!
        Display the information window for the software.
        @param self The pointer for the object
        @event The handle for the mouse click event
        """
        about_window = Toplevel(self.root, bg='white')
        about_window.title('About')
        #Add the toolbar icon
        about_window.tk.call("wm", "iconphoto", about_window._w, self.icon)
        #Create frames for use
        about_frame = StdFrame(about_window)
        version_frame = StdFrame(about_window)

        #Add information to about frame
        StdLabel(about_frame,
                 text='pyLogger',
                 font=tkFont.Font(family='Arial',
                                  size='20',
                                  weight='bold'),
                 justify=CENTER,
                 ).grid(row=0)
        description = 'pyLogger is a simple data logging application.\n\n'\
                      'pyLogger can communicate with a Mecmesin AFG \n'\
                      'series load cell or a TSI 4000 '\
                      'Series flow meter.\n\n'\
                      'Author: Ben Johnston (ext 101859)\n'\
                      'License: GNU GPL v2.0'
        StdLabel(about_frame,
                 text=description,
                 justify=LEFT).grid(row=1, padx=5, pady=5)
        StdLabel(about_frame,
                 text='Version Information:',
                 font=tkFont.Font(family='Arial',
                                  size='16',
                                  weight='bold'),
                 justify=LEFT).grid(row=2, padx=5, pady=5,
                                    sticky='W')
        StdLabel(about_frame,
                 text='pyLogger Ver: %s' % self.version,
                 justify=LEFT).grid(row=3, sticky='W')
        StdLabel(about_frame,
                 text='Standard Toolbox Ver: %s' % std_rev,
                 justify=LEFT).grid(row=4, sticky='W')
        StdLabel(about_frame,
                 text='TSI Driver Ver: %s' % TSI_rev,
                 justify=LEFT).grid(row=5, sticky='W')
        StdLabel(about_frame,
                 text='AFG Driver Ver: %s' % AFG_rev,
                 justify=LEFT).grid(row=6, sticky='W')

        #Display frames
        about_frame.grid()
        version_frame.grid()
        #Centre window
        self.centre_window(about_window)

    def open_results(self):
        """!
        This method is used to open the folder containing the results logs
        @param self The pointer for the object
        """
        if os.name == 'nt':
            self.debug_logger.info('Open Results Folder: ' + self.log_folder)
            subprocess.Popen('explorer "{0}"'.format(self.log_folder))

    def _quit(self):
        """!
        This module quits the program
        @param self The pointer for the object
        """
        self.quit_command()
        sys.exit()

    def process_incoming(self):
        """!
        Process information from the IO thread
        @param self The pointer for the object
        """
        while self.queue.qsize():
            self.debug_logger.info('Gui: Received data from threads')
            try:
                data = self.queue.get()
                #Check for errors
                if (data['error_type'] is not None) and\
                   (data['error_info'] is not None):
                    if (time.time() - self.error_timer) > ERROR_TIME:
                        #Log the error
                        self.debug_logger.info('Received error type'
                                               ' %s' % data['error_type'])
                        self.debug_logger.info('Received error info'
                                               ' %s' % data['error_info'])
                        #Display error to user
                        tkMessageBox.showerror(
                            data['error_type'],
                            data['error_info'],
                            parent=self.root)
                        self.error_timer = time.time()
                #Update the file name
                if data['file_name'] is not None:
                    #Log the receipt of file_name
                    self.debug_logger.info(
                        'Received file name: %s' % data['file_name'])
                    self.log_name.set(data['file_name'])
                #Scroll through each of the unit windows
                for i in range(len(data['status'])):
                    status = data['status'][i]
                    if status is not None:
                        #Update the connection status variable
                        self.debug_logger.info(
                            'Received connection status for device'
                            ' %d: %s' % ((i + 1), status))
                        self.unit_frame_dict[i]['status'].set(
                            status)
                        #Update the colour fo the status message
                        if status == CONNECTION_TYPES[1]:
                            status_colour = 'green'
                        else:
                            status_colour = 'red'
                        #Commit the update
                        self.unit_frame_dict[i]['status_widget'].\
                            configure(fg=status_colour)

                for i in range(len(data['readings'])):
                    #Update the reading variable
                    reading = data['readings'][i]
                    if reading is not None:
                        self.debug_logger.info('Received reading '
                                               'for device %d: %s' % ((i + 1),
                                                                      reading))
                        self.unit_frame_dict[i]['reading'].set(
                            '%0.2f' % reading)

            except Queue.Empty:
                pass
            except Exception, e:
                self.debug_logger.info(e.__str__())

    def validate_inputs(self):
        """!
        Validate the user inputs prior to starting measurements
        @param self The pointer for the object
        @return True if the inputs are valid, False if not.
        """
        #The file name cannot be blank
        if self.file_name.get() is '':
            return False
        else:
            return True
