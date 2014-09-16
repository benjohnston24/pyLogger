#! /usr/bin/env python
"""!
Process state machine for the pyLogger project
"""
__author__ = "Ben Johnston"
__revision__ = "0.1"
__date__ = "Wed Sep 10 07:59:13 EST 2014"
__license__ = "GPL"

##IMPORTS#####################################################################
from stdtoolbox.stateMachine import StateMachine
from processStates import system_setup_state, configure_state,\
    measure_state, process_state, log_state,\
    complete_state, error_state
##############################################################################


class processStateMachine(StateMachine):
    """!
    This class defines the state machine to be used by the pyLogger project.
    @anchor State_Machine
    \dot
        digraph example {
        node [shape=circle, fixedsize=false, fontname=Helvetica,
        fontsize=8, width=0.9];
        edge [fontsize=8];
        "start" [shape="doublecircle" color="green"];
        "end" [shape="doublecircle" color="blue"];
        "error" [shape="doublecircle" color="red"];

        "start" -> "Connect Test Hardware";
        "Connect Test Hardware" -> "Data Entry"
        [label = "Connection Successful"];
        "Connect Test Hardware" -> "Connect Test Hardware"
        [label = "Connection Unsuccessful"];
        "Data Entry" -> "Load Device";
        "Load Device" -> "Execute Connection Test";
        "Load Device" -> "Connect Test Hardware"
        [label = "Device Connection Lost"];
        "Execute Connection Test" -> "Execute Connection Test"
        [label = "Device Connection Lost"];
        "Execute Connection Test" -> "Open Test Jig";
        "Execute Connection Test" -> "error"
        [label = "Test Error"];
        "Open Test Jig" -> "Execute Cross Connection Test";
        "Execute Cross Connection Test" -> "Execute Cross Connection Test"
        [label = "Device Connection Lost"];
        "Execute Cross Connection Test" -> "Remove Device";
        "Execute Cross Connection Test" -> "error"
        [label = "Test Error"];
        "Remove Device" -> "Finalise Test";
        "Finalise Test" -> "end";
        "error" -> "Connect Test Hardware"
        [label = "Error Reset"];
        }
    \enddot
    """

    def __init__(self, debug_level=0):
        """!
        The constructor for the class
        @param self The pointer for the object
        @param debug_level Set to greater than 1 to enable debugging
        functionality.  Set to 1 to print each database command
        that is executed to the command prompt.  Set to 2 to print the
        database command to the command prompt and log the command to a file
        named <i>info.log</i>
        """
        StateMachine.__init__(self)
        ##var debug_level
        #An instance copy of the debug_level passed to the initialise
        #method.
        self.debug_level = debug_level

        #Generate the states for the process########################
        ##@var system_setup_state
        #The state used to connect the test system hardware
        self.system_setup_state = system_setup_state
        ##@var configure_state
        #The system configuration state
        self.configure_state = configure_state
        ##@var measure_state
        #The state which executes measurements
        self.measure_state = measure_state
        ##@var process_state
        #The state which processes measurements
        self.process_state = process_state
        ##@var log_state
        #The data logging state
        self.log_state = log_state
        ##@var complete_state
        #The final state for a correct execution of the state machine.
        self.complete_state = complete_state
        ##@var error_state
        #The error state for the state machine.
        self.error_state = error_state
        #Configure the process path###################################
        self.system_setup_state.set_next_state([
            self.configure_state,
            self.error_state])

        self.configure_state.set_next_state([
            self.measure_state,
            self.error_state,
            self.system_setup_state])

        self.measure_state.set_next_state([
            self.process_state,
            self.error_state])

        self.process_state.set_next_state([
            self.log_state,
            self.error_state])

        self.log_state.set_next_state([
            self.measure_state,
            self.error_state])

        self.complete_state.set_next_state([
            self.system_setup_state,
            self.error_state])

        self.error_state.set_next_state([self.complete_state,
                                         self.error_state])
        #Add the states to the stack###################################
        #The initial state
        self.add_state(self.system_setup_state)
        self.add_state(self.configure_state)
        self.add_state(self.measure_state)
        self.add_state(self.process_state)
        self.add_state(self.log_state)
        self.add_state(self.complete_state)
        self.add_state(self.error_state)

    def run(self, cargo=None):
        """!
        Run the state machine
        @param self The pointer for the object
        @param cargo A dictionary containing the data for the state machine.
        As a minimum the dictionary must contain the following items:<br />
        <table>
        <tr><th>Key</th><th>Data</th>
        <tr><td>'GUI_object'</td><td>A pyLoggerGui.pyLoggerGui instance</td>
        <tr><td>'logger'</td><td>A toolbox.logger instance</td>
        <tr><td>'hardware'</td><td>A cathRxTestHardware.cathRxTestHardware
        instance</td>
        </table>
        """
        self.stop_flag = False
        if cargo is not None:
            ##@var cargo
            #An instance copy of the data dictionary for the state machine
            self.cargo = cargo
            #If this is the first execution cycle load a blank
            #current_state into cargo
            if not ('current_state' in self.cargo):
                self.cargo['current_state'] = ''
        else:
            return
        #Run the state machine until the complete state is reached
        while self.current_state != self._COMPLETE_STATE:
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

            self.queue.put(self.cargo['queue_data'])
            if self.current_state != self._COMPLETE_STATE:
                self.current_state = self.stack[self.current_state].\
                    next_state[self.cargo['exit_status']]
            else:
                break

        self.cargo['logger'].info('Stopping State Machine')

    def reset(self):
        """!
        Reset the state machine to the initial state
        @param self The pointer for the object
        """
        ##@var current_state
        #The handle for the state currently being executed
        self.current_state = self.initial_state
        self.run(self.cargo)

    def stop(self):
        """!
        Stop the state machine
        @param self The pointer for the object
        """
        self.current_state = self._COMPLETE_STATE
