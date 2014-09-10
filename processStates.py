#! /usr/bin/env python
"""

"""
__author__ = "Ben Johnston"
__revision__ = "0.1"
__date__ = "Wed Sep 10 07:55:51 EST 2014"
__license__ = "GPL"

##IMPORT#####################################################################
from stdtoolbox.stateMachine import state, StateMachine
#############################################################################


##Functions for states######################################################

def system_setup(**kwargs):
    """!
    This function is used to initialise the system
    @param kwargs A pointer to the structure passed to the function
    @return A pointer to the structure passed to the function, containing
    updated data.
    """
    #Wait for user input
    kwargs['exit_status'] = state._SUCCESS
    return kwargs


def take_reading(**kwargs):
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
