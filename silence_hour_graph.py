from matplotlib import pyplot as plt
import numpy as np
import math #needed for definition of pi
import time


# x = [11,12,14,14,15]
# y = [1,5,3,4,6]
# plt.plot(x,y)
fig, li = plt.subplot(1)
li.xlabel("Time")
li.ylabel("Decibels")
li.title('Silence!!')
li.pause(0.01)
time.sleep(5)
while True:

    li.set_xdata([0, 1, 2, 3,4, 5])
    li.set_ydata([3, 4, 6, 7, 8, 9])
    plt.pause(0.01)
    time.sleep(2)
    li.set_xdata([1, 2, 3, 4, 5, 6])
    li.set_ydata([4, 6, 7, 8, 9, 10])
    plt.pause(0.01)
    time.sleep(2)
    # plt.plot([2, 3, 4, 5, 6, 7], [6, 7, 8, 9, 10, 11])
    # plt.pause(0.01)
    # time.sleep(2)
    # plt.plot([3, 4, 5, 6, 7, 8], [7, 8, 9, 10, 11, 12])
    # plt.pause(0.01)
    # time.sleep(2)