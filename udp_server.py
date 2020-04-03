import socket

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
        data, addr = sock.recvfrom(100)
        # print("received message:", [dat for dat in data])
        for dat in range(1, len(data)-1, 2):
            new = data[dat+1]
            new = (new << 8) | data[dat]
            dat += 1
            serial_data.append(new - subtract_value)
            filled += 1
    return serial_data


def read_udp_data_indefinite():

    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        # print("received message:", [dat for dat in data])
        for dat in range(1, len(data)-1, 2):
            new = data[dat+1]
            new = (new << 8) | data[dat]
            dat += 1
            # serial_data.append(new - subtract_value)
            print(new)


if __name__ == '__main__':
    print("listening...")
    read_udp_data_indefinite()
