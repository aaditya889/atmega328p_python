import serial
import sys
import time
from constants import *


def serial_read():
    ports = USB_SERIAL_PORT

    max_port = 100

    ser = serial.Serial()
    ser.baudrate = SERIAL_BAUD_RATE

    while True:
        try:
            # print ("Ready for a new connection...")

            while not ser.is_open:
                # print ser.is_open
                for num in range(max_port + 1):
                    try:
                        # print "trying for %s" %(port)
                        port = ports + str(num)
                        ser.port = port
                        ser.open()
                        # print ("status for - ", port, str(ser.is_open))
                        break
                    except Exception as e:
                        pass

            while True:
                serial_data = ser.readline().decode()
                return serial_data

        except Exception as e:
            print("disconnection reason - ", str(e))
            ser.is_open = False
            print("disconnected, waiting...")
            pass