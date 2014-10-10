#! /usr/bin/env python
"""!
Module used for collecting data from an Analogue to Digital converter over a
USART bus
"""
__author__ = "Ben Johnston"
__revision__ = "0.1"
__date__ = "Fri Oct 10 12:35:12 EST 2014"
__license__ = "GPL v2.0"

##IMPORTS#####################################################################
import serial
from stdtoolbox.logging import logger
import os
from glob import glob
import pdb
##############################################################################


#Define an exception class
class ADCException(Exception):
    """!
    Class to handle exceptions within the ADC module
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


class ADCProtocolLayer(object):

    def __init__(self, serial_port=None, connect=True, debug_level=0):
        """!
        The constructor for the class
        @param serial_port
        @param connect
        @param debug_level
        """
        #Create a results logger for the object
        self.debug_level = debug_level
        self.info_logger = logger(debug_level=self.debug_level)
        #Create a continuous mode flag for the object
        #Initialise the module
        #Set the communications parameters of the device
        self.port = None
        self.baudrate = 9600
        self.bytesize = serial.EIGHTBITS
        self.xonxoff = False
        self.parity = serial.PARITY_NONE
        self.stopbits = serial.STOPBITS_ONE
        self.timeout = 0.5
        self.rtscts = False
        self.dsrdtr = False
        #Create the serial object for the device
        self.device = serial.Serial(baudrate=self.baudrate,
                                    bytesize=self.bytesize,
                                    parity=self.parity,
                                    stopbits=self.stopbits,
                                    timeout=self.timeout,
                                    writeTimeout=self.timeout,
                                    xonxoff=self.xonxoff,
                                    rtscts=self.rtscts,
                                    dsrdtr=self.dsrdtr)
        if connect:
            self.connect(serial_port)

    def connect(self, serial_port=None):
        """!
        @param The pointer for the object
        """
        if serial_port is None:
            if os.name is 'nt':
                range_of_ports = []
                for i in range(255):
                    range_of_ports.append('COM%d' % i)
            elif os.name is 'posix':
                range_of_ports = glob('/dev/ttyACM*') + glob('/dev/ttyUSB*')
            #If the port is not specified, find it
            for i in range_of_ports:
                #Try and open the port
                try:
                    self.device.port = i
                    self.info_logger.info(self.device.port)
                    self.device.close()
                    self.device.open()
                    try:
                        #Get the next reading
                        reading = self.read_msg().next()
                        self.port = self.device.port
                        return
                    except ValueError:
                        self.device.close()
                except StopIteration:
                    self.device.close()
                except:
                    self.device.port = None
        else:
            self.device.port = serial_port
            self.port = self.device.port
            self.device.open()

    def send_msg(self, message):
        """!
        Send a message to the ADC device
        @param self The pointer for the object
        @param message The message to send to the ADC device
        """
        try:
            self.device.write('%s' % message)
            self.info_logger.info('To ADC@%s: %s' %
                                  (self.device.port, message))
        except Exception, e:
            raise ADCException('Unable to write to ADC: %s' % e.__str__())

    def read_msg(self):
        """!
        Read a message from the ADC device
        @param self The pointer for the object
        """
        try:
            response = self.device.readline()
            self.info_logger.info('From ADC@%s: %s' %
                                  (self.device.port, response))
            response = response.strip('\r\n').strip(' ')
            pdb.set_trace()
            yield response.strip('\r\n').strip(' ')
        except StopIteration:
            pass
        except Exception, e:
            raise ADCException('Unable to read from ADC: %s' % e.__str__())
