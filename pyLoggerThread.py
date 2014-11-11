#! /usr/bin/env python
"""!
Process state machine for the pyLogger project
"""
__author__ = "Ben Johnston"
__revision__ = "0.1"
__date__ = "Wed Sep 10 07:59:13 EST 2014"
__license__ = "GPL"

##IMPORTS#####################################################################
from processStateMachine import processStateMachine
from pyLoggerGui import pyLoggerGui
from stdtoolbox.logging import logger
import tkMessageBox
import Queue
import threading
import os

#import pdb
##############################################################################

##@var LOG_FOLDER
#The folder location for log files
LOG_FOLDER = os.path.join(os.getcwd(), 'dat')


#A function that provides a reduced data file
def sample_data_file(file_name=None, rate=None):
    """!
    Take a sample of data from file_name.
    @param file_name The file name of the data to sample
    @param rate The rate at which data is to be sampled.  If rate = x then
    every xth line is extraced from the file (exlcuding the header row
    @return The file name of the file containing the sampled data set.  The
    returned file will contain file_name with '_sampled' appended and inserted
    before the file extension e.g. test.csv becomes test_sampled.csv. If an
    error occurred None will be returned.
    """
    if os.path.isfile(file_name):
        if rate is None:
            return None
        else:
            #Extract file name
            (log_file_name, ext) = os.path.splitext(file_name)
            sample_name = log_file_name + '_sampled' + ext
            counter = rate + 1
            with open(file_name, 'r') as f_in:
                with open(sample_name, 'a') as f_out:
                    while True:
                        line = f_in.readline()
                        if line == '':
                            break
                        if counter > rate:
                            f_out.write(line)
                            counter = 1
                        else:
                            counter += 1
            return sample_name


class pyLoggerThread(processStateMachine):
    """!

    """
    ##@var STOP
    #Constant used to stop the state machine
    STOP = 0

    ##@var RUNNING
    #Constant used to indicate that the state machine is running
    RUNNING = 1

    ##@var RESET
    #Constant used to indicate that the statemachine is being reset
    RESET = 2

    ##@var IDLE
    #Constant used to indicate the state machine is in an idle state
    IDLE = 3

    def __init__(self,
                 root=None,
                 version=None,
                 number_of_units=2,
                 debug_level=0):
        """!
        The constructor for the class
        @param self The pointer for the object
        @param root The Tkinter Tk object for the class
        @param version The software version to be displayed
        @param number_of_units The number of logging units to be used by the
        class
        @param debug_level Set to greater than 1 to enable debugging
        functionality.  Set to 1 to print each database command
        that is executed to the command prompt.  Set to 2 to print the
        database command to the command prompt and log the command to a file
        named <i>info.log</i>
        """
        #Instantiate the parent class
        processStateMachine.__init__(self, debug_level)

        ##@var queue
        #Create the Queue object for sharing information between threads
        self.queue = Queue.Queue()

        ##@var root
        #The root window for the GUI
        self.root = root

        ##@var gui
        #The pyLoggerGui object for the class
        self.gui = pyLoggerGui(root=root,
                               queue=self.queue,
                               version=version,
                               number_of_units=number_of_units,
                               log_folder=LOG_FOLDER,
                               start_command=self.start,
                               reset_command=self.stop,
                               stop_command=self.stop,
                               debug_level=debug_level)

        ##@var run_status
        #Used to control the operation of the thread
        self.run_status = self.STOP

        ##@var cargo
        #A dictionary object used to pass data through the state machine
        self.cargo = {'gui_object': self.gui,
                      'logger': logger(debug_level=self.debug_level),
                      'error_logger': logger('error.log', debug_level=2),
                      'log_folder': LOG_FOLDER,
                      'debug_level': self.debug_level,
                      'queue': self.queue,
                      'queue_data': {'status': [None for i in
                                                range(self.gui.number_of_units)
                                                ],
                                     'readings':
                                         [None for i in
                                          range(self.gui.number_of_units)],
                                     'plot_data':
                                         [None for i in
                                          range(self.gui.number_of_units)],
                                     'file_name': None,
                                     },
                      }

        #Monitor process queue
        self.monitor()

    def run(self):
        """!
        Run the state machine
        @param self The pointer for the object
        """
        #If this is the first execution cycle load a blank
        #current_state into cargo
        if not ('current_state' in self.cargo):
            self.cargo['current_state'] = ''

        #Run the state machine until a stop signal is triggered
        while self.run_status is not self.STOP:

            #If the state has changed, log the new state
            if self.cargo['current_state'] != self.current_state:
                #Log the current state
                self.cargo['logger'].info('Change State: %s'
                                          % self.current_state)
                #Update the current state
                self.cargo['current_state'] = self.current_state
            #Execute the process of the current state and return
            #the updated cargo dictionary
            self.cargo = self.stack[self.current_state].\
                executeState(self.cargo)

            if self.current_state != self._COMPLETE_STATE:
                self.current_state = self.stack[self.current_state].\
                    next_state[self.cargo['exit_status']]
            else:
                self.run_status = self.STOP

        #Close all ports
        for log_device in self.cargo['devices']:
            log_device.close_port()

        #Provide a reduced data set log
        sample_data_file(file_name=os.path.join(LOG_FOLDER,
                                                self.cargo['log_file_name']),
                         rate=5)
        self.current_state = self.initial_state
        self.cargo['current_state'] = ''
        self.cargo['logger'].info('Stopping State Machine')

    def start(self):
        """!
        """
        if self.gui.validate_inputs():
            ##@var worker
            #A thread object to execute the worker thread
            self.worker = threading.Thread(target=self.run)
            self.run_status = self.RUNNING
            #Clear the plots
            #pdb.set_trace()
            #for line in self.cargo['gui_object'].line:
            #    line.remove()
            #Start the thread
            self.worker.start()
        else:
            tkMessageBox.showinfo('Missing Information',
                                  'Enter file name and at least one device is'
                                  ' selected',
                                  parent=self.root)

    def stop(self):
        """!
        """
        self.run_status = self.STOP

    def monitor(self):
        """!
        """
        self.gui.process_incoming()
        self.gui.root.after(500, self.monitor)
