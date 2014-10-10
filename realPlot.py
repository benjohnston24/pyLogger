#! /usr/bin/env python
"""!
Module that provides real time data plotting capabilities
"""
__author__ = "Ben Johnston"
__revision__ = "0.1"
__date__ = "Thu Oct  2 08:23:39 EST 2014"
__license__ = "GPL"
__copyright__ = "Company Confidential. Copyright (c) Ti2 Pty Ltd 2014."

##IMPORTS#####################################################################
import matplotlib.pyplot as plt
import matplotlib.animation as anim
##############################################################################


class realPlot(object):
    """!
    Class to create and operate a real time plotting object
    """
    def __init__(self, number_of_lines=1):
        """!
        The constructor for the class
        @param self The pointer for the object
        @param number_of_lines Indicates the number of lines to be plotted on
        the graph
        """
        ##@var number_of_lines
        #The number of lines to be plotted on the graph
        self.number_of_lines = number_of_lines
        ##@var figure
        #The handle for the figure object for the graph
        ##@varax
        #The handle for the axis object(s) for the plot
        self.figure, self.ax = plt.subplots()
        ##@var line
        #An array containing the line objects for the plot
        self.line = []
        for i in range(self.number_of_lines):
            line = self.ax.plot([], [])
            self.line.append(line)
        #Configure the axes and grid for the plot
        self.ax.set_ylim(0, 1000)
        self.ax.set_xlim(0, 10)
        self.ax.grid()
        #Initialise the data structures
        self.xdata, self.ydata = [], []
        self.xdata2, self.ydata2 = [], []

    def add_data(self, data):
        """!
        A method used to add data to the plot
        @param self The pointer for the object
        @param data An array or tuple containing the x and y coordinates for
        the specified data point.
        @return The handle for the updated line in the graph
        """
        x, y = data
        self.xdata.append(x)
        self.ydata.append(y)
        self.xdata2.append(x)
        self.ydata2.append(y/2)
        self.xmin, self.xmax = self.ax.get_xlim()
        #Update the x axis scale if nexessary
        if x > self.xmax:
            self.ax.set_xlim(self.xmin, 2 * self.xmax)
            self.ax.figure.canvas.draw()
        self.line.set_data(self.xdata, self.ydata)
        self.line2.set_data(self.xdata2, self.ydata2)

        return self.line, self.line2

    def run(self, data_generator):
        """!
        Execute the animation
        @param self The pointer for the object
        @param data_generator The handle of the function used to collect data
        for the graph.
        """
        self.ani = anim.FuncAnimation(self.figure,
                                      self.add_data,
                                      data_generator,
                                      blit=True,
                                      interval=1,
                                      repeat=False)
        plt.show()
