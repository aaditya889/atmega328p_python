# from __future__ import print_function
import sys
import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from mpu_read import *

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'r', animated=True)
f = np.linspace(0, 100, 100)


# this is the function that returns the values to plot
def read_values():

    return get_mpu_values()


def init():
    ax.set_xlim(0, 100)
    ax.set_ylim(-91, 91)
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
    mpu_val = read_values()
    xdata.append(frame)
    ydata.append(mpu_val)
    ln.set_data(xdata, ydata)

    # print "printing xdata and ydata"
    # print xdata, ydata
    # print len(xdata), len(ydata)
    if len(xdata) >= 101 or len(ydata) >= 101:
        xdata = []
        ydata = []
        xdata.append(frame)
        ydata.append(mpu_val)
        ln.set_data(xdata, ydata)

    return ln,


read_values()

ani = animation.FuncAnimation(fig, update, frames=f, init_func=init, blit=True, interval = 50, repeat=True)

plt.show()            
