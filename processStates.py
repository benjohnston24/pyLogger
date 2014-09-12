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
from loggerUnit import loggerUnit, CONNECTION_TYPES, ERROR,\
    UNIT_TYPES, CONNECTED, DEV_TYPE, NO_TYPE, AFG, TSI
import tkMessageBox
import os
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
    kwargs['file_name'] = kwargs['log_folder'] + \
                          kwargs['gui_object'].file_name.get() + \
                          '.csv'

    #Construct the device objects
    kwargs['devices'] = [None, None]
    i = 0
    for device in (kwargs['gui_object'].unit_frame_dict):
        unit = loggerUnit(unit_type=device['unit'].get(),
                          debug_level=kwargs['debug_level'])
        kwargs['devices'][i] = unit
        i += 1

    #Connect the devices
    try:
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

    #Handle any errors
    except:
        kwargs['queue_data']['status'][i] = CONNECTION_TYPES[ERROR]
        kwargs['queue'].put(kwargs['queue_data'])
        tkMessageBox.showerror('Connection Error:',
                               'Unable to connect to device',
                               parent=kwargs['gui_object'].root)
        kwargs['exit_status'] = state._ERROR
        return kwargs


def configure_system(**kwargs):
    """!
    """
    #Check if any of the devices are not connected
    i = 0
    for device in kwargs['devices']:
        if (device.connected != CONNECTION_TYPES[CONNECTED]) and\
                (device.unit_type != UNIT_TYPES[NO_TYPE]):
            tkMessageBox.showerror("Connection Error",
                                   "Device %d not connected" % (i + 1),
                                   parent=kwargs['gui_object'].root)
            kwargs['exit_status'] = state._FIRST_BRANCH
            return kwargs
        else:
            i += 1
    #Build the header row
    kwargs['header'] = ['Date', 'Time']
    for device in kwargs['devices']:
        if device.unit_type != UNIT_TYPES[NO_TYPE]:
            for dat_type in device.results_types:
                kwargs['header'].append(dat_type)
    #Setup the data logging object
    if os.path.isfile(kwargs['file_name']):
        #Set the write header flag
        write_header = True
    kwargs['results_log'] = csvLogger(kwargs['file_name'],
                                      debug_level=kwargs['debug_level'],
                                      header=kwargs['header'])
    if write_header:
        kwargs['results_log'].write_line(kwargs['header'],
                                         date_time_flag=False)
    kwargs['exit_status'] = state._SUCCESS
    return kwargs


def take_reading(**kwargs):
    kwargs['results'] = []
    i = 0
    try:
        for device in kwargs['devices']:
            (result, display) = device.retrieve_measurement()
            kwargs['results'].append(result)
            kwargs['queue_data']['readings'][i] = display
            i += 1
        kwargs['queue'].put(kwargs['queue_data'])
        kwargs['exit_status'] = state._SUCCESS
        return kwargs
    #Handle any errors
    except:
        kwargs['queue_data']['status'][i] = CONNECTION_TYPES[ERROR]
        kwargs['queue'].put(kwargs['queue_data'])
        tkMessageBox.showerror('Measurement Error',
                               'Device %d: Unable to take'
                               ' measurement' % i + 1,
                               parent=kwargs['gui_object'].root)
        kwargs['exit_status'] = state._ERROR
        return kwargs


def log_reading(**kwargs):
    data_to_write = []
    for result in kwargs['results']:
        if result is not None:
            keys = result.keys()
            #The order logging the data must be correct
            if 'force/torque' in keys:
                data_to_write.append(result['force/torque'])
            if 'flow' in keys:
                data_to_write.append(result['flow'])
            if 'press' in keys:
                data_to_write.append(result['press'])
            if 'temp' in keys:
                data_to_write.append(result['temp'])
            if 'random' in keys:
                data_to_write.append(result['random'])
    #Write the data
    kwargs['results_log'].write_line(data_to_write,
                                     date_time_flag=True)
    kwargs['exit_status'] = state._SUCCESS
    return kwargs


def finalise_test(**kwargs):
    return kwargs


def handle_error(**kwargs):
    kwargs['exit_status'] = state._SUCCESS
    return kwargs
##Construct the states#####################################################
system_setup_state = state(system_setup, "Setup System")
configure_state = state(configure_system, "Configure System")
measure_state = state(take_reading, "Complete Measurement")
process_state = state(log_reading, "Data Logging")
complete_state = state(finalise_test, StateMachine._COMPLETE_STATE)
error_state = state(handle_error, StateMachine._ERROR_STATE)
