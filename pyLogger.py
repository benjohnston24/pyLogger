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
from pyLoggerThread import pyLoggerThread
from Tkinter import Tk
##############################################################################

#Process command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--log', action='store_true',
                    default=False, help="Status / Error logging")
parser.add_argument('-d', '--debug'=, action='store_true',
                    default=False, help='Enable debug messages')
args = parser.parse_args()

debug_level = 0
if args.debug:
    debug_level = 1
elif args.log:
    debug_level = 2

#Run Script
root = Tk()
pyLoggerThread(root, debug_level=debug_level)
root.mainloop()
