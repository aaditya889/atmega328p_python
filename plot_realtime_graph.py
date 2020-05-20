# import pyaudio
import numpy as np
# import pylab
import matplotlib.pyplot as plt
from generic_serial_read import *
from udp_server import *
# from scipy.io import wavfile
import time
import sys
MAX_POINTS = 1000
NUM_PLOTS = 1   # number of graphs to plot
SERIAL_READ_FUNCTION = read_udp_data
X_LOWER_LIMIT = 0
X_UPPER_LIMIT = MAX_POINTS
Y_LOWER_LIMIT = -520
Y_UPPER_LIMIT = 520

f, ax = plt.subplots(NUM_PLOTS)

# Prepare the Plotting Environment with random starting values
x = np.arange(MAX_POINTS)
y = np.random.randn(MAX_POINTS)

# Plot 0 is for raw data
li, = ax.plot(x, y)
ax.set_xlim(X_LOWER_LIMIT, X_UPPER_LIMIT)
ax.set_ylim(Y_LOWER_LIMIT, Y_UPPER_LIMIT)
ax.set_title("Raw Signal")

# Plot 1 is for the FFT of the audio
# li2, = ax[1].plot(x, y)
# ax[1].set_xlim(0, 5000)
# ax[1].set_ylim(-100, 100)
# ax[1].set_title("Fast Fourier Transform")

# Show the plot, but without blocking updates
plt.pause(0.01)
plt.tight_layout()

keep_going = True


def old():
    FORMAT = pyaudio.paInt16  # We use 16bit format per sample
    CHANNELS = 1
    RATE = 44100
    CHUNK = MAX_POINTS  # 1024bytes of data red from a buffer

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True)
    # Open the connection and start streaming the data
    stream.start_stream()
    print("\n+---------------------------------+")
    print("| Press Ctrl+C to Break Recording |")
    print("+---------------------------------+\n")

    # Loop so program doesn't end while the stream callback's
    # itself for new data
    while keep_going:
        plot_data(stream.read(CHUNK, exception_on_overflow=False))
        # keep_going=False
        pass

    # Close up shop (currently not used because KeyboardInterrupt
    # is the only way to close)
    stream.stop_stream()
    stream.close()

    audio.terminate()


def plot_data(in_data):
    # get and convert the data to float
    # audio_data = np.frombuffer(in_data, np.int16)
    # audio_data = [1]*MAX_POINTS
    # Fast Fourier Transform, 10*log10(abs) is to scale it to dB
    # and make sure it's not imaginary
    # dfft = 10.*np.log10(abs(np.fft.rfft(audio_data)))
    # Force the new data into the plot, but without redrawing axes.
    # If uses plt.draw(), axes are re-drawn every time
    #print audio_data[0:10]
    #print dfft[0:10]
    #print
    li.set_xdata(np.arange(len(in_data)))
    li.set_ydata(in_data)
    # li2.set_xdata(np.arange(len(dfft))*10.)
    # li2.set_ydata(dfft)

    # Show the updated plot, but without blocking
    plt.pause(0.01)


data = [0] * MAX_POINTS
while True:
    data = SERIAL_READ_FUNCTION(MAX_POINTS)
    # print(data)
    plot_data(data)
