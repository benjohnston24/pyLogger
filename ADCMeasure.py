#! /usr/bin/env python
"""!
Module to take measurements from the Analogue to Digital Converter
"""
__author__ = "Ben Johnston"
__revision__ = "0.1"
__date__ = "Fri Oct 17 13:31:02 EST 2014"
__license__ = "GPL v2.0"

##IMPORTS#####################################################################
from ADCProtocolLayer import ADCProtocolLayer
import pdb
##############################################################################


class ADCMeasure(ADCProtocolLayer):

    def __init__(self, serial_port=None, connect=True, debug_level=0):
        """!
        The constructor for the class
        @param serial_port
        @param connect
        @param debug_level
        """
        ADCProtocolLayer.__init__(self, serial_port, connect, debug_level)

    def get_measurement(self):
        """!
        This method returns an array of measurements from the ADC
        @param self The pointer for the object
        @return An array of measurements where the 1st element corresponds to
        the measurement taken from channel 1 and the 2nd element from ADC
        channel 2 etc.
        """
        while True:
            try:
                measurement_list = []
                key_list = []
                measurement = [0]
                measurement = self.read_msg().next().split(',')
                for data in measurement:
                    measurement_list.append(int(data.split(':')[1]))
                    key_list.append(int(data.split(':')[0]))
                return_flag = True
                for i in range(1, 6):
                    if i not in key_list:
                        return_flag = False
                if return_flag and len(measurement_list) == 6:
                    return measurement_list
            except IndexError:
                pass
            except Exception, e:
                pdb.set_trace()
