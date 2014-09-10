#! /usr/bin/env python
"""
"""
__author__ = "Ben Johnston"
__revision__ = "0.1"
__date__ = "Wed Sep 10 17:03:10 EST 2014"
__license__ = "GPL"

##IMPORT#####################################################################
from stdtoolbox.stdGUI import StdButton
#############################################################################


class pyLoggerButton(StdButton):
    """!
    This class is used to control the operation of the buttons within the
    pyLogger system user interface.
    """

    def __init__(self, parent, **kwargs):
        """!
        A constructor for the class
        @param self The pointer for the object
        @param parent The parent object for the frame
        @param **kwargs Other arguments as accepted by ttk.Button
        """
        #Initialise the inherited class
        StdButton.__init__(self, parent, **kwargs)
        #Bind the button for a release action
        self.bind('<ButtonRelease-1>', self.__activated)
        ##@var __btn_activated
        #Private variable used to control reporting of the button's status
        #Initialise.
        self.__btn_activated = False

    def __activated(self, event=None):
        """!
        A private method that updates the __btn_activated private variable
        in response to operating the button.
        @param self The pointer for the object
        @param event The event object supplied from clicking the button
        """
        #If there is an operation event update the private variable
        if event is not None:
            self.__btn_activated = True

    def get_btn_status(self):
        """!
        A method that returns the status of the button.
        @param self The pointer for the object
        @return True if the button has been depressed since last calling this
        method <br/> False if the button has not been depressed since last
        calling this method.
        """
        if self.__btn_activated:
            self.__btn_activated = False
            return True
        else:
            return False

    def click(self, event=None):
        """!
        This method is used to simulate the button being pressed.
        @param self The pointer for the object
        """
        self.__btn_activated = True
