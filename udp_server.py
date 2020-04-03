import socket
import struct

UDP_IP = "192.168.1.17"
UDP_PORT = 8000
sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP, UDP_PORT))
# print("listening...")
subtract_value = 512


def read_udp_data(num):
    serial_data = list()
    filled = 0
    while filled < num:
        data, addr = sock.recvfrom(1000)
        # print("received message:", [dat for dat in data])
        for dat in range(0, len(data), 2):
            new = data[dat]
            new = (new << 8) | data[dat+1]
            # dat += 1
            serial_data.append(new - subtract_value)
            # print(dat - subtract_value)
            filled += 1
    return serial_data[0:num+1]


def read_udp_data_indefinite():

    while True:
        data, addr = sock.recvfrom(1000)
        # print("received message:", [dat for dat in data])
        print(data)
        print(len(data))
        for dat in range(0, len(data), 2):
            new = data[dat]
            new = (new << 8) | data[dat+1]
            # new = struct.unpack('B', data[dat])[0]
            # new = (new << 8) | data[dat]
            # dat += 1
            # serial_data.append(new - subtract_value)
            # print(dat - subtract_value)
            print(new, end=' ')
        print("done")


if __name__ == '__main__':
    print("listening...")
    read_udp_data_indefinite()
