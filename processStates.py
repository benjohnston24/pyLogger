#! /usr/bin/env python
"""

"""
__author__ = "Ben Johnston"
__revision__ = "0.1"
__date__ = "Wed Sep 10 07:55:51 EST 2014"
__license__ = "GPL"

##IMPORT#####################################################################
from stdtoolbox.stateMachine import state, StateMachine
from stdtoolbox.logging import csvLogger
from loggerUnit import loggerUnit
import pdb
#############################################################################


##Functions for states######################################################

def system_setup(**kwargs):
    """!
    This function is used to initialise the system
    @param kwargs A pointer to the structure passed to the function
    @return A pointer to the structure passed to the function, containing
    updated data.
    """
    #Collect the user input
    file_name = kwargs['gui_object'].file_name.get()
    #Construct the data logging object
    kwargs['data_logger'] = csvLogger(file_name,
                                      debug_level=kwargs['debug_level'])

    #Construct the device objects
    kwargs['devices'] = [None, None]
    i = 0
    for device in (kwargs['gui_object'].unit_frame_dict):
        unit = loggerUnit(unit_type=device['unit'].get(),
                          debug_level=kwargs['debug_level'])
        kwargs['devices'][i] = unit
        i += 1
    #Connect the devices
    i = 0
    kwargs['queue_data']['status'] = [None, None]
    for device in kwargs['devices']:
        device.connect()
        kwargs['queue_data']['status'][i] = device.connected
        i += 1
        #Update the display
        kwargs['queue'].put(kwargs['queue_data'])
    kwargs['exit_status'] = state._SUCCESS
    return kwargs


def take_reading(**kwargs):
    kwargs['results'] = []
    kwargs['queue_data']['readings'] = [None, None]
    i = 0
    for device in kwargs['devices']:
        (result, display) = device.retrieve_measurement()
        kwargs['results'].append(result)
        kwargs['queue_data']['readings'][i] = display
        i += 1
        kwargs['queue'].put(kwargs['queue_data'])
    kwargs['exit_status'] = state._SUCCESS
    return kwargs


def finalise_test(**kwargs):
    kwargs['exit_status'] = state._SUCCESS
    return kwargs


def handle_error(**kwargs):
    return kwargs
##Construct the states#####################################################
system_setup_state = state(system_setup, "Setup System")
measure_state = state(take_reading, "Complete Measurement")
process_state = state(finalise_test, "Analysis")
complete_state = state(finalise_test, StateMachine._COMPLETE_STATE)
error_state = state(handle_error, StateMachine._ERROR_STATE)
