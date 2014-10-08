#! /usr/bin/env python
"""!
pyLogger is a data logging package that can be used to log data that is
received via a serial bus as well as other means.
"""
__author__ = "Ben Johnston"
__revision__ = "0.4"
__date__ = "Wed Oct  1 16:30:32 EST 2014"
__license__ = "GPL"

##IMPORTS#####################################################################
import argparse
from pyLoggerThread import pyLoggerThread
from Tkinter import Tk
from stdtoolbox.logging import crashLogger
import sys
##############################################################################
#Define the crash logger
crashlog = crashLogger()
#Re-route the exception handler to log uncaught exceptions
sys.excepthook = crashlog.log_crash

#Process command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--units', action='store', type=int,
                    default=2, help='Number of logging units')
parser.add_argument('-l', '--log', action='store_true',
                    default=False, help="Status / Error logging")
parser.add_argument('-d', '--debug', action='store_true',
                    default=False, help='Enable debug messages')
args = parser.parse_args()

debug_level = 0
if args.debug:
    debug_level = 1
elif args.log:
    debug_level = 2

#Run Script
root = Tk()
pyLoggerThread(root=root,
               version=__revision__,
               number_of_units=args.units,
               debug_level=debug_level)
root.mainloop()
