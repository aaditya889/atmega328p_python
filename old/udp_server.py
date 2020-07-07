import socket
import struct
import pyaudio


UDP_IP = "192.168.43.13"
UDP_PORT = 8000
sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP, UDP_PORT))
# print("listening...")
print("%s Listening on %d" % (UDP_IP, UDP_PORT))
subtract_value = 64
data_queue = list()
MAX_DATA = 2

from threading import Thread
from multiprocessing import Process

running_processes = dict()
running_threads = dict()


def multi_thread(thread_list_identifier):

    def decorator(function):

        def wrapper(*args, **kwargs):

            global running_processes

            if thread_list_identifier not in running_threads:
                running_threads[thread_list_identifier] = list()

            thread = Thread(target=function, args=args, kwargs=kwargs)
            thread.setDaemon(True)
            thread.start()

            running_threads[thread_list_identifier].append(thread)

        return wrapper

    return decorator


def read_udp_data(num):
    serial_data = list()
    filled = 0
    while filled < num:
        data = sock.recv(1201)
        # print("received message:", [dat for dat in data])
        # print(data)
        for dat in data:
            # new = data[dat]
            # new = (new << 8) | data[dat+1]
            # dat += 1
            serial_data.append(dat - subtract_value)
            # print(dat - subtract_value)
            filled += 1
    return serial_data[0:num+1]


def read_udp_data_indefinite():
    while True:
        data = sock.recv(1000).decode()
        print(data)


@multi_thread('mpu_read')
def read_udp_data_mpu():

    while True:
        # udp_data = list()
        # print("%s Listening on %d" % (UDP_IP, UDP_PORT))
        data = sock.recv(1000).decode()
        print(data)
        # data = data.split('AX: ')[1].split(' ')[0]
        try:
            data = float(data.split("YX:")[1].lstrip().split(' ')[0])
            # print(data)
            data_queue.append(data)
            if len(data_queue) >= MAX_DATA:
                data_queue.pop(0)
        except:
            pass
        # print(data)
        # udp_data.append(float(data) * 500)
        # print(float(data) * 500)
        # return float(data) * 500


if __name__ == '__main__':
    print(read_udp_data_indefinite())
    exit(0)
#
#
# if __name__ == '__main__':
#     # print("listening...")
#     # read_udp_data_indefinite()
#
#     p = pyaudio.PyAudio()
#
#     stream = p.open(format=pyaudio.paInt8,
#                     channels=1,
#                     rate=16000,
#                     output=True, frames_per_buffer=1200)
#
#     # data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
#     # filled = 0
#     # while filled < 1024:
#     # subtract_value = 512
#     udp_data = list()
#     while True:
#         # serial_data = list()
#         data = sock.recv(1024)
#
#         # print("received message:", [dat for dat in data])
#         # for dat in range(0, 1024, 2):
#         #     new = data[dat]
#         #     new = (new << 8) | data[dat+1]
#         #     dat += 1
#             # serial_data.append(new - subtract_value)
#             # print(dat - subtract_value)
#             # filled += 1
#         # print(data)
#         stream.write(data)
#
#     # stream.stop_stream()
#     # stream.close()
#
#     # p.terminate()

