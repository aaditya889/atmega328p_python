# from __future__ import print_function
import sys
import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from mpu_read import *
from generic_serial_read import *
# this is the function that returns the values to plot
serial_read_function = temp_serial_read
X_UPPER_LIMIT = 100
X_LOWER_LIMIT = 0
Y_UPPER_LIMIT = 1024
Y_LOWER_LIMIT = -1024


fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'r', animated=False)

# first value is the starting offset on x-axis, from where the values will be written
# second is the number of points that will be written
# third is the ending offset for the values on x axis
f = np.linspace(0, X_UPPER_LIMIT, X_UPPER_LIMIT)


def init():
    ax.set_xlim(X_LOWER_LIMIT, X_UPPER_LIMIT)
    ax.set_ylim(Y_LOWER_LIMIT, Y_UPPER_LIMIT)
    ln.set_data(xdata,ydata)
    return ln,


def update(frame):
    
    global xdata, ydata
    # try:
    # if len(xdata) >= 100 or len(ydata) >= 100:
    # xdata = []
    # ydata = []
    # except:
    # pass
    data_value = serial_read_function()
    xdata.append(frame)
    ydata.append(data_value)
    ln.set_data(xdata, ydata)

    # print "printing xdata and ydata"
    # print xdata, ydata
    # print len(xdata), len(ydata)
    if len(xdata) >= X_UPPER_LIMIT + 1 or len(ydata) >= Y_UPPER_LIMIT + 1:
        xdata = []
        ydata = []
        xdata.append(frame)
        ydata.append(data_value)
        ln.set_data(xdata, ydata)

    return ln,


# serial_read_function()

ani = animation.FuncAnimation(fig, update, frames=f, init_func=init, blit=True, interval=1, repeat=True)

plt.show()            
