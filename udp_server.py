import socket
import struct
import pyaudio


UDP_IP = "192.168.1.17"
UDP_PORT = 8000
sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP, UDP_PORT))
# print("listening...")
subtract_value = 64


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


def read_udp_data_indefinite(num):
    udp_data = list()
    print("%s Listening on %d" % (UDP_IP, UDP_PORT))
    while num > 0:
        data = sock.recv(1000).decode()
        # data = data.split('AX: ')[1].split(' ')[0]
        data = data.split("AX:")[1].lstrip().split(' ')[0]
        udp_data.append(data)
        num -= 1
        # print(len(data))
        # for dat in range(0, len(data), 2):
        #     new = data[dat]
        #     new = (new << 8) | data[dat+1]
        #     # new = struct.unpack('B', data[dat])[0]
        #     # new = (new << 8) | data[dat]
        #     # dat += 1
        #     # serial_data.append(new - subtract_value)
        #     # print(dat - subtract_value)
        #     print(new, end=' ')
        # print("done")
    return udp_data

# if __name__ == '__main__':
#     print(read_udp_data_indefinite(1000))
#     exit(0)
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
