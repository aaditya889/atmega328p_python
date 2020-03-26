import serial
import sys
import time
from constants import *

file_fd = None
serial_port = None


def serial_read(num):

    subtract_value = 512

    global serial_port
    if serial_port is None:
        ports = USB_SERIAL_PORT

        max_port = 100

        serial_port = serial.Serial()
        serial_port.baudrate = SERIAL_BAUD_RATE

        try:
            while not serial_port.is_open:
                for num in range(max_port + 1):
                    try:
                        port = ports + str(num)
                        serial_port.port = port
                        serial_port.open()
                        break
                    except Exception as e:
                        pass

        except Exception as e:
            print("disconnection reason - ", str(e))
            serial_port.is_open = False
            print("disconnected, waiting...")

    serial_data = list()
    for i in range(num):
        try:
            serial_data.append(int(serial_port.readline().decode()) - subtract_value)
        except UnicodeDecodeError:
            i -= 1
        except ValueError:
            i -= 1
            
    return serial_data


def temp_serial_read():

    global file_fd
    if file_fd is None:
        file_fd = open('temp_data', 'r')

    line = file_fd.readline()[:-1]

    if line is '':
        file_fd = open('temp_data', 'r')
        line = file_fd.readline()[:-1]

    return int(line) % 1024


def t2():

    return 20
# for i in range(500):
#     print(temp_serial_read())
