import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from old.udp_server import *

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
MAX_POINTS = 20
SERIAL_READ_FUNCTION = read_udp_data_indefinite
udp_data = list()


def refresh_data():
    global udp_data
    udp_data = SERIAL_READ_FUNCTION(MAX_POINTS)


# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    global udp_data
    # Read temperature (Celsius) from TMP102
    # temp_c = round(tmp102.read_temp(), 2)
    # Add x and y to lists
    if len(udp_data) == 0:
        refresh_data()

    value = udp_data.pop(0)

    xs.append(dt.datetime.now().strftime('%S'))
    ys.append(value)

    # Limit x and y lists to 20 items
    xs = xs[-MAX_POINTS:]
    ys = ys[-MAX_POINTS:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('X-axis accelerometer reading')
    plt.ylabel('X Accelerometer')


# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1)
plt.show()
