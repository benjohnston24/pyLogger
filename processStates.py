#! /usr/bin/env python
"""

"""
__author__ = "Ben Johnston"
__revision__ = "0.1"
__date__ = "Wed Sep 10 07:55:51 EST 2014"
__license__ = "GPL"

##IMPORT#####################################################################
from stdtoolbox.stateMachine import state
#############################################################################


##Functions for states######################################################

def system_setup(**kwargs):
    """!
    This function is used to initialise the system
    @param kwargs A pointer to the structure passed to the function
    @return A pointer to the structure passed to the function, containing
    updated data.
    """
    btn_activated = kwargs['gui_object'].start_button.get_btn_status()
    if btn_activated:
        kwargs['exit_status'] = state._SUCCESS
    else:
        kwargs['exit_status'] = state._FIRST_BRANCH
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
complete_state = state(finalise_test, "Complete State")
error_state = state(handle_error, "Error State")
