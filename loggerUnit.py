#! /usr/bin/env python
"""!
This module is used as a wrapper for all devices to be used within pyLogger.
This module will provide a common interface between the processStates,GUI and
the different types of hardware device to be used in the system
"""
__author__ = "Ben Johnston"
__revision__ = "0.2"
__date__ = "Mon Sep  8 08:36:23 EST 2014"
__copyright__ = "Company Confidential. Copyright (c) ResMed Ltd 201[[3]."

##IMPORTS#####################################################################
from TSI.TSIMeasure import TSIMeasure
from AFG.AFGMeasure import AFGMeasure
from stdtoolbox.logging import logger
import sys
#Used to test program with "Dev" unit type
import random
import time
##############################################################################

##@var UNIT_TYPES
#This variable is a list of all devices available for use in the system
UNIT_TYPES = ["--None--", "Mecmesin Force Gauge", "TSI 4000 Flow Meter",
              "Dev",
              ]

##@var NO_TYPE
#Flag for not type selected
NO_TYPE = 0

##@var AFG
#Type for the mecmesin force gauge
AFG = 1

##@var TSI
#Type for the TSI flow meter
TSI = 2

##@var DEV_TYPE
#Flag for the development type
DEV_TYPE = 3

##@var CONNECTION_TYPES
#This variable stores a list of all connection types available to serial
#devices
CONNECTION_TYPES = ["Not Connected", "Connected", "Error"]

##@var NOT_CONNECTED
#Not connected flag
NOT_CONNECTED = 0

##@var CONNECTED
#Connected flag
CONNECTED = 1

##@var ERROR
#Error flag
ERROR = 2


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
                 unit_type=UNIT_TYPES[NO_TYPE],
                 debug_level=0,
                 ):
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
            self.sleep = 0
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
        ##@var error_logger
        #An error logging unit for the class
        #Hard coded debug level to ensure logging to file
        self.error_logger = logger('error.log', debug_level=2)

        #Create the device object
        if unit_type == UNIT_TYPES[NO_TYPE]:
            ##@var device
            #The handle for the logging device
            #If no type is selected a handle of None is used
            self.device = None
            ##@var connected
            #A connection status flag for the object
            self.connected = CONNECTION_TYPES[NOT_CONNECTED]
            ##@var results_types
            #An array of valid results types for the object
            self.results_types = None
        elif unit_type == UNIT_TYPES[AFG]:
            #The force gauge device handle
            self.connected = CONNECTION_TYPES[NOT_CONNECTED]
            self.results_types = ['force/torque']
        elif unit_type == UNIT_TYPES[TSI]:
            #The flow meter device handle
            self.connected = CONNECTION_TYPES[NOT_CONNECTED]
            self.results_types = ['flow', 'temp', 'press']
        elif unit_type == UNIT_TYPES[DEV_TYPE]:
            #Debbuging unit type
            self.device = None
            self.connected = CONNECTION_TYPES[NOT_CONNECTED]
            self.results_types = ['random']

    def connect(self):
        """!
        This method is used to connect to the device being used
        """
        if self.unit_type == UNIT_TYPES[DEV_TYPE]:
            self.info_logger.info('%s: Connected' % self.unit_type)
            #If the none object is being used, do nothing
            self.connected = CONNECTION_TYPES[CONNECTED]
            return
        elif self.unit_type == UNIT_TYPES[NO_TYPE]:
            #If None is selected do nothing
            pass
        else:
            try:
                if self.unit_type == UNIT_TYPES[AFG]:
                    #Use the force gauge type
                    self.device = AFGMeasure(self.serial_port,
                                             self.debug_level)
                elif self.unit_type == UNIT_TYPES[TSI]:
                    #Use the flow meter
                    self.device = TSIMeasure(self.serial_port,
                                             self.debug_level)
                #Connect to the device
                if self.device.port is not None:
                    self.connected = CONNECTION_TYPES[CONNECTED]
                else:
                    self.connected = CONNECTION_TYPES[NOT_CONNECTED]
            except Exception, e:
                #Raise an exception if an error occured.  Wrap in loggerunit
                #exception class
                self.connected = CONNECTION_TYPES[ERROR]
                msg = '<' + type(self).__name__ + '.' + \
                    sys._getframe().f_code.co_name + \
                    '> ' + str(e)
                self.error_logger.info(msg, date_time_flag=True)
                raise loggerUnitException(msg)

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
        if self.connected == CONNECTION_TYPES[NO_TYPE]:
            #If the device is not connected return nothing
            return (None, None)

        #If the device is connected
        return_result = {}
        if self.unit_type == UNIT_TYPES[DEV_TYPE]:
            #If the selected device is the development device
            #Return a random number
            return_result['random'] = \
                round(random.randrange(1, 100) + random.random(), 2)
            self.info_logger.info('Measurement from %s: %0.2f' %
                                  (self.unit_type, return_result['random'])
                                  )
            time.sleep(self.sleep)
            return (return_result, return_result['random'])

        elif self.unit_type == UNIT_TYPES[NO_TYPE]:
            #If the none object is being used, do nothing
            return (None, None)
        else:
            try:
                if self.unit_type == UNIT_TYPES[AFG]:
                    #Use the force gauge type
                    #Take a single reading
                    return_result['force/torque'] = \
                        self.device.get_measurement()
                    display_result = return_result['force/torque']
                    return (return_result, display_result)
                elif self.unit_type == UNIT_TYPES[TSI]:
                    #Use the flow meter
                    #Take a single reading
                    return_result = {}
                    result = self.device.measure_FTP()
                    for key in result.keys():
                        return_result[key] = result[key][0]
                    display_result = return_result['flow']
                    return (return_result, display_result)
                else:
                    return (None, None)
            except Exception, e:
                #Raise an exception if an error occured.  Wrap in loggeruni
                #exception class
                msg = '<' + type(self).__name__ + '.' + \
                    sys._getframe().f_code.co_name + \
                    '> ' + str(e)
                self.error_logger.info(msg, date_time_flag=True)
                raise loggerUnitException(msg)

    def close_port(self):
        """!
        Close the port of the device
        @param self The pointer for the object
        """
        if (self.unit_type != UNIT_TYPES[NO_TYPE] and
                self.unit_type != UNIT_TYPES[DEV_TYPE]):
            self.device.device.close()
