#! /usr/bin/env python
"""!
This module is used as a wrapper for all devices to be used within pyLogger.
This module will provide a common interface between the processStates,GUI and
the different types of hardware device to be used in the system
"""
__author__ = "Ben Johnston"
__revision__ = "0.1"
__date__ = "Mon Sep  8 08:36:23 EST 2014"
__copyright__ = "Company Confidential. Copyright (c) ResMed Ltd 2014."

##IMPORTS#####################################################################
from TSI.TSIMeasure import TSIMeasure
from AFG.AFGMeasure import AFGMeasure
from stdtoolbox.logging import logger
import pdb
##############################################################################

##@var UNIT_TYPES
#This variable is a list of all devices available for use in the system
UNIT_TYPES = ["--None--", "Mecmesin Force Gauge", "TSI 4000 Flow Meter"]

##@var CONNECTION_TYPES
#This variable stores a list of all connection types available to serial
#devices
CONNECTION_TYPES = ["Not Connected", "Connected", "Error"]


#Define an exception class
class loggerUnitException(Exception):
    """!
    Class to handle exceptions within the loggerUnit
    """
    def __init__(self, msg=None):
        """!
        The constructor for the class.
        @param self The pointer for the object
        @param msg The message to be displayed within the exception
        """
        Exception.__init__(self, msg)
        ##@var msg
        #The message to report for the exception
        self.msg = msg

    def __str__(self):
        """!
        This method provides a string representation of the exception
        @param self The pointer for the object
        @return A string representation of the exceptions
        """
        return self.msg


class loggerUnit(object):
    """!
    Wrapper class used to contain logging device interfaces
    """
    def __init__(self,
                 serial_port=None,
                 unit_type=UNIT_TYPES[0],
                 debug_level=0):
        """!
        The constructor for the class
        @param self The pointer for the object
        @param serial_port The serial port used by the device.  If None is
        provided the serial port will be found automatically
        @param unit_type Is used to select what type of device is to be used
        for the object.  The available selections are stored within the list
        TSI.UNIT_TYPES
        @param debug_level Set to 0 for no debugging options, 1 for activity
        logged to stdout and 2 for logging activity to stdout and info.log.
        """
        ##@var serial_port
        #Store the serial port for the object
        self.serial_port = serial_port
        #Check the unit type is valid
        if unit_type in UNIT_TYPES:
            ##@var unit_type
            #Store the unit type for the object
            self.unit_type = unit_type
        else:
            #The unit type is invalid
            #raise an exception
            loggerUnitException('Invalid unit_type selected')
        ##@var debug_level
        #Store the debug level for the object
        self.debug_level = debug_level
        ##@var info_logger
        #A logging object for the class
        self.info_logger = logger('info.log', debug_level=self.debug_level)

        #Create the device object
        if unit_type is UNIT_TYPES[0]:
            ##@var device
            #The handle for the logging device
            #If no type is selected a handle of None is used
            self.device = None
            ##@var connected
            #A connection status flag for the object
            self.connected = None
        elif unit_type is UNIT_TYPES[1]:
            #The force gauge device handle
            self.connected = False
        elif unit_type is UNIT_TYPES[2]:
            #The flow meter device handle
            self.connected = False

    def connect(self):
        """!
        This method is used to connect to the device being used
        """
        if self.unit_type is UNIT_TYPES[0]:
            #If the none object is being used, do nothing
            return
        else:
            try:
                if self.unit_type is UNIT_TYPES[1]:
                    #Use the force gauge type
                    self.device = AFGMeasure(self.serial_port,
                                             self.debug_level)
                elif self.unit_type is UNIT_TYPES[2]:
                    #Use the flow meter
                    self.device = TSIMeasure(self.serial_port,
                                             self.debug_level)
                #Connect to the device
                if self.device.port is not None:
                    self.connected = True
                else:
                    self.connected = False
            except Exception, e:
                #Raise an exception if an error occured.  Wrap in loggerunit
                #exception class
                raise loggerUnitException(e.__str__())

    def configure_device(self):
        """!
        Method used to configure the device
        @param self The pointer for the object
        """
        pass

    def retrieve_measurement(self):
        """!
        Method used to retrieve a measurement from the device and provide a
        consistent return
        @param self The pointer for the object
        @return A dictionary containing each of the results.  The key is an
        indicator to the measurement type
        """
        return_result = {}
        if self.unit_type is UNIT_TYPES[0]:
            #If the none object is being used, do nothing
            return
        else:
            try:
                if self.unit_type is UNIT_TYPES[1]:
                    #Use the force gauge type
                    #Take a single reading
                    return_result['force/torque'] = \
                        self.device.get_measurement()
                elif self.unit_type is UNIT_TYPES[2]:
                    #Use the flow meter
                    #Take a single reading
                    return_result = self.device.measure_FTP()
            except Exception, e:
                #Raise an exception if an error occured.  Wrap in loggerunit
                #exception class
                raise loggerUnitException(e.__str__())
