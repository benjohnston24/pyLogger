#! /usr/bin/env python
"""!
Utility functions for processStates.py
"""
__author__ = "Ben Johnston"
__revision__ = "0.1"
__date__ = ""
__license__ = "GPL"
__copyright__ = "Company Confidential. Copyright (c) Ti2 Pty Ltd 2014."

##IMPORTS#####################################################################
from stdtoolbox.logging import csvLogger
import time
##############################################################################


def measurement_thread(thread_id, device, queue):
    result_dict = {}
    measure_log = csvLogger('measure_log.csv')
    start = time.time()
    result_dict[thread_id] = []
    try:
        result_dict[thread_id] = device.retrieve_measurement()
        queue.put(result_dict)
        finish = time.time()
        measure_log.write_line('%s,%0.2f' % (device.unit_type, finish - start))
    except:
        result_dict[thread_id]['error'] = 1
