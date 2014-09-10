#! /usr/bin/env python
"""!
Mecmesin load cell data logger
"""
__author__ = "Ben Johnston"
__revision__ = "0.1"
__date__ = ""
__license__ = "GPL"

##IMPORTS#####################################################################
import argparse
from pyLoggerGui import pyLoggerGui
from processStateMachine import processStateMachine
#from AFG import AFG
##############################################################################

#Process command line arguments
parser = argparse.ArgumentParser()
#parser.add_argument('-p', '--port', help="Select COM port e.g. 3")
#parser.add_argument('-l', '--log', action='store_true',
#                    default=False, help="Enable debug / error logging")
#parser.add_argument('-b', '--beep', action='store_true',
#                    default=False, help="Enable beep on level")
#parser.add_argument('-c', '--criteria', help='Define the levels for activating'
#                    ' the beep.  Enter as integers', nargs='+')
#args = parser.parse_args()

#Run Script
stateMachine = processStateMachine(debug_level=1)
gui = pyLoggerGui(state_machine=stateMachine, debug_level=1)
gui.mainloop()
